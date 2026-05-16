import sys
import cv2
import os
import time
import datetime
import requests
import threading
import torch  # 💥 新增：引入 torch 控制底层并发
from collections import Counter
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog, QDialog, QLabel, \
    QVBoxLayout, QMessageBox, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSettings, QTimer, QEvent
from PyQt5.QtGui import QImage, QPixmap, QCursor, QColor, QFont, QPainter, QBrush
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

from ultralytics import YOLO
from core.db_helper import DBHelper
from core.theme_manager import apply_theme, THEME_DARK, THEME_LIGHT
from UI.modern_ui import Ui_ModernWindow

# 全局模型初始化锁，保障多路启动时的绝对安全
GLOBAL_MODEL_LOCK = threading.Lock()


class AIChatThread(QThread):
    reply_signal = pyqtSignal(str)

    def __init__(self, user_message, role="operator", db_context=""):
        super().__init__()
        self.user_message = user_message
        self.role = role
        self.db_context = db_context
        self.api_key = "sk-c97f0269c1834b9ab2d109517b12fdd0"
        self.api_url = "https://api.deepseek.com/chat/completions"

    def run(self):
        try:
            if self.role == "admin":
                sys_prompt = "你是智慧工地管控系统的超级管理员专属 AI 助理。请以专业、宏观的视角回答问题，语气要尊贵且高效。"
            else:
                sys_prompt = "你是智慧工地管控系统的操作员专属 AI 客服。请以耐心、专业的态度指导操作员使用系统。"
                if self.db_context:
                    sys_prompt += f"""\n\n<database_result>\n{self.db_context}\n</database_result>\n\n【系统指令】：
            上方标签内是系统从数据库获取的【当前操作员自己的真实业务数据】！
            你的任务是：根据上面的真实数据回答操作员的提问。绝对禁止编造虚假数据！如果有没做过的事情，请如实回答。"""
                else:
                    sys_prompt += """\n\n【系统状态】：当前对话未触发数据库查询。
            【回答策略】：
            1. 正常交流：如果用户是在问候，或者询问系统的操作方法，请耐心解答。
            2. 拒绝幻想：只有当用户明确要求你查询具体的业务数据时才查询。
            【绝对禁令】：严禁凭空捏造任何考勤或违规数据！"""

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": self.user_message}
                ],
                "temperature": 0.1
            }
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            reply_text = result['choices'][0]['message']['content']
            self.reply_signal.emit(reply_text)

        except Exception as e:
            self.reply_signal.emit(f"⚠️ 网络异常或 AI 接口调用失败。\n(错误信息: {str(e)})")


class YOLOThread(QThread):
    send_image_signal = pyqtSignal(str, QImage, QImage)
    send_alert_signal = pyqtSignal(str, str, str, str, str)
    send_boxes_signal = pyqtSignal(str, list, float)
    finished_signal = pyqtSignal()
    send_stats_signal = pyqtSignal(int, int)

    def __init__(self, source, source_type, operator_name, camera_id, module_name="实时监控", capture_dir="抓拍图库",
                 model_path="", device_type="Auto", cooldown=5):
        super().__init__()
        self.source = source
        self.source_type = source_type
        self.operator_name = operator_name
        self.camera_id = str(camera_id)
        self.module_name = module_name
        self.capture_dir = capture_dir
        self.cooldown_seconds = cooldown
        self.model_path = model_path if model_path else r"runs\detect\train3\weights\best.pt"

        self.device = ''
        if "GPU" in device_type:
            self.device = 0
        elif "CPU" in device_type:
            self.device = 'cpu'

        self.is_running = True
        self.db = DBHelper()
        if not os.path.exists(self.capture_dir): os.makedirs(self.capture_dir)
        self.last_alert_time = datetime.datetime(2000, 1, 1)
        self.conf_threshold = 0.60

    def set_threshold(self, new_conf):
        self.conf_threshold = new_conf

    def run(self):
        try:
            with GLOBAL_MODEL_LOCK:
                # 💥 护城河 1：限制 PyTorch 的 CPU 多线程，防止矩阵全开时 CPU 爆锁！
                torch.set_num_threads(1)

                model = YOLO(self.model_path)

                if self.source_type == 'webcam':
                    # 💥 护城河 2 (极其致命)：绕开 MSMF，强制使用 DirectShow (DSHOW) 后端，彻底粉碎 0xC0000409！
                    cap = cv2.VideoCapture(int(self.source), cv2.CAP_DSHOW)
                elif self.source_type == 'video':
                    cap = cv2.VideoCapture(self.source)

                if self.source_type in ['webcam', 'video'] and not cap.isOpened():
                    raise Exception("无法打开视频源/摄像头被占用")

        except Exception as e:
            print(f"底层引擎加载崩溃 (通道 {self.camera_id}): {e}")
            self.finished_signal.emit()
            return

        if self.source_type in ['webcam', 'video']:
            while cap.isOpened() and self.is_running:
                ret, frame = cap.read()
                if not ret: break
                self.process_frame(model, frame)
                if self.source_type == 'video': QThread.msleep(30)
            cap.release()
        elif self.source_type == 'image':
            for file_path in self.source:
                if not self.is_running: break
                frame = cv2.imread(file_path)
                if frame is not None:
                    self.process_frame(model, frame)
                    if len(self.source) > 1: QThread.msleep(2000)
        self.finished_signal.emit()

    def process_frame(self, model, frame):
        start_infer_time = time.time()
        kwargs = {'verbose': False}
        if self.device != '': kwargs['device'] = self.device

        results = model(frame, **kwargs)
        annotated_frame = frame.copy()
        pure_inference_time = time.time() - start_infer_time

        alert_triggered = False
        max_conf = 0.0
        safe_count = 0
        alert_count = 0
        boxes_data_list = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                if conf > self.conf_threshold:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    if cls_id == 0:
                        alert_count += 1
                        alert_triggered = True
                        max_conf = max(max_conf, conf)
                        boxes_data_list.append({"cls": "未戴安全帽", "conf": conf, "coords": (x1, y1, x2, y2)})
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.putText(annotated_frame, f"NO HELMET {conf:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
                    elif cls_id == 1:
                        safe_count += 1
                        boxes_data_list.append({"cls": "佩戴安全帽", "conf": conf, "coords": (x1, y1, x2, y2)})
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(annotated_frame, f"SAFE {conf:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

        self.send_boxes_signal.emit(self.camera_id, boxes_data_list, pure_inference_time)
        self.send_stats_signal.emit(safe_count, alert_count)

        if alert_triggered:
            now = datetime.datetime.now()
            if (now - self.last_alert_time).total_seconds() >= self.cooldown_seconds:
                self.last_alert_time = now
                time_str = now.strftime('%H:%M:%S')
                db_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
                img_path = os.path.join(self.capture_dir, f"抓拍_{now.strftime('%Y%m%d_%H%M%S')}_{self.camera_id}.jpg")
                cv2.imwrite(img_path, annotated_frame)
                event_str = f"{self.module_name}-未戴安全帽"
                self.db.insert_record(db_time_str, event_str, f"{max_conf:.2f}", img_path, self.operator_name)
                self.send_alert_signal.emit(self.camera_id, time_str, event_str, f"{max_conf:.2f}", img_path)

        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888).copy()
        orig_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        orig_qt_image = QImage(orig_rgb.data, w, h, ch * w, QImage.Format_RGB888).copy()

        self.send_image_signal.emit(self.camera_id, orig_qt_image, qt_image)


class MainApp(QMainWindow, Ui_ModernWindow):
    def __init__(self, current_username="TestUser"):
        super().__init__()
        self.current_username = current_username
        self.db = DBHelper()
        self.setupUi(self)

        self.settings = QSettings("SmartSite", "YOLOv12Platform")
        self.current_theme = THEME_DARK
        self.custom_capture_path = os.path.join(os.getcwd(), "抓拍图库")

        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))

        self.current_mode = None
        self.yolo_thread_1 = None

        self.rt_threads = {}
        self.rt_labels = {}
        # 🌟 全屏状态管理
        self.fullscreen_state = {"active": False, "cam_id": None, "dialog": None, "label": None}

        self.timer_clock = QTimer(self)
        self.timer_clock.timeout.connect(self.update_realtime_clock)
        self.timer_clock.start(1000)
        self.update_realtime_clock()

        if hasattr(self, 'btn_check_in'): self.btn_check_in.clicked.connect(self.handle_check_in)
        if hasattr(self, 'btn_quick_img'): self.btn_quick_img.clicked.connect(lambda: self.switch_page(1))
        if hasattr(self, 'btn_quick_vid'): self.btn_quick_vid.clicked.connect(lambda: self.switch_page(2))
        if hasattr(self, 'btn_quick_rt'): self.btn_quick_rt.clicked.connect(lambda: self.switch_page(3))

        if hasattr(self, 'slider_default_conf'):
            self.slider_default_conf.valueChanged.connect(
                lambda v: self.lbl_default_conf_val.setText(f"{v / 100.0:.2f}"))

        self.load_system_settings()

        # 🌟 加载并应用保存的主题
        saved_theme = self.settings.value(f"{self.current_username}_theme", THEME_DARK)
        self.current_theme = saved_theme
        if hasattr(self, 'combo_theme'):
            idx = self.combo_theme.findText(saved_theme)
            self.combo_theme.setCurrentIndex(idx if idx >= 0 else 0)
        apply_theme(self, saved_theme)

        if hasattr(self, 'btn_upload_image'): self.btn_upload_image.clicked.connect(self.start_image)
        if hasattr(self, 'slider_conf_image'): self.slider_conf_image.valueChanged.connect(self.update_image_slider)

        if hasattr(self, 'btn_upload_video'): self.btn_upload_video.clicked.connect(self.start_video)
        if hasattr(self, 'btn_stop_video'): self.btn_stop_video.clicked.connect(self.stop_detection)
        if hasattr(self, 'slider_conf_video'): self.slider_conf_video.valueChanged.connect(self.update_video_slider)

        if hasattr(self, 'btn_browse_rt'): self.btn_browse_rt.clicked.connect(self.browse_rt_file)
        if hasattr(self, 'btn_add_rt'): self.btn_add_rt.clicked.connect(self.add_rt_channel)
        if hasattr(self, 'btn_remove_rt'): self.btn_remove_rt.clicked.connect(self.remove_rt_channel)
        if hasattr(self, 'btn_start_cams'): self.btn_start_cams.clicked.connect(self.start_rt_matrix)
        if hasattr(self, 'btn_stop_cams'): self.btn_stop_cams.clicked.connect(self.stop_detection)
        if hasattr(self, 'slider_conf_rt'): self.slider_conf_rt.valueChanged.connect(self.update_rt_slider)

        if hasattr(self, 'btn_search_history'): self.btn_search_history.clicked.connect(self.filter_history)
        if hasattr(self, 'btn_reset_history'): self.btn_reset_history.clicked.connect(self.reset_history)
        if hasattr(self, 'btn_browse_path'): self.btn_browse_path.clicked.connect(self.select_capture_dir)
        if hasattr(self, 'btn_save_system'): self.btn_save_system.clicked.connect(self.save_system_settings)

        if hasattr(self, 'btn_logout'): self.btn_logout.clicked.connect(self.logout)
        if hasattr(self, 'btn_save_pwd'): self.btn_save_pwd.clicked.connect(self.change_password)
        if hasattr(self, 'btn_save_email'): self.btn_save_email.clicked.connect(self.change_email)

        if hasattr(self, 'btn_send_chat'):
            self.btn_send_chat.clicked.connect(self.send_chat_message)
            self.input_chat.returnPressed.connect(self.send_chat_message)
            self.chat_history = []
            welcome_html = '''
                    <table width="100%" border="0" cellspacing="0" cellpadding="8">
                        <tr>
                            <td width="45" valign="top" align="center"><span style="font-size: 28px;">🤖</span></td>
                            <td align="left" valign="top">
                                <div style="background-color: #333537; color: #E3E3E3; padding: 12px 18px; border-radius: 8px; font-size: 16px; font-family: 'Microsoft YaHei'; display: inline-block;">
                                    您好！我是智慧工地 AI 助手，请问有什么可以帮您的？
                                </div>
                            </td>
                        </tr>
                    </table>
                    '''
            self.chat_history.append(welcome_html)
            self.chat_display.setHtml("".join(self.chat_history))

        self.init_charts()
        self.records_data = []
        self.load_history()
        self.refresh_attendance_ui()
        self.auto_cleanup_captures()

    def update_realtime_clock(self):
        now = datetime.datetime.now()
        if hasattr(self, 'lbl_realtime_clock'): self.lbl_realtime_clock.setText(now.strftime('%H:%M:%S'))
        if hasattr(self, 'lbl_welcome_title'):
            hour = now.hour
            greeting = "早上好" if 5 <= hour < 12 else "下午好" if 12 <= hour < 18 else "晚上好"
            self.lbl_welcome_title.setText(f"{greeting}，{self.current_username}")

    def handle_check_in(self):
        success, msg = self.db.add_check_in(self.current_username)
        if success:
            QMessageBox.information(self, "打卡成功", "✅ 您已成功完成今日签到！")
            self.refresh_attendance_ui()
        else:
            QMessageBox.warning(self, "提示", msg)

    def refresh_attendance_ui(self):
        check_time = self.db.get_today_check_in(self.current_username)
        days = self.db.get_attendance_days(self.current_username)
        if check_time:
            time_str = check_time.strftime('%H:%M:%S') if isinstance(check_time, datetime.datetime) else \
            str(check_time).split()[-1]
            if hasattr(self, 'btn_check_in'):
                self.btn_check_in.setText("已签到")
                self.btn_check_in.setEnabled(False)
            if hasattr(self, 'lbl_check_in_msg'):
                self.lbl_check_in_msg.setText(f"打卡时间：{time_str}")
                self.lbl_check_in_msg.setStyleSheet(
                    "color: #10B981; font-weight: bold; font-size: 15px; border: none; margin-top: 15px;")
            if hasattr(self, 'lbl_checkin_status'):
                self.lbl_checkin_status.setText(f"✅ 今日已签到 ({time_str})")
                self.lbl_checkin_status.setStyleSheet(
                    "color: #10B981; font-size: 18px; font-weight: bold; background-color: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 8px;")
        else:
            if hasattr(self, 'btn_check_in'):
                self.btn_check_in.setText("立即签到")
                self.btn_check_in.setEnabled(True)
            if hasattr(self, 'lbl_check_in_msg'):
                self.lbl_check_in_msg.setText("今日尚未打卡")
                self.lbl_check_in_msg.setStyleSheet(
                    "color: #EF4444; font-weight: bold; font-size: 15px; border: none; margin-top: 15px;")
            if hasattr(self, 'lbl_checkin_status'):
                self.lbl_checkin_status.setText("❌ 今日未签到，请前往首页打卡！")
                self.lbl_checkin_status.setStyleSheet(
                    "color: #EF4444; font-size: 18px; font-weight: bold; background-color: rgba(239, 68, 68, 0.1); padding: 15px; border-radius: 8px;")
        if hasattr(self, 'lbl_attendance_days'):
            self.lbl_attendance_days.setText(f"🏆 本月已累计全勤打卡 {days} 天，继续保持！")

    def send_chat_message(self):
        text = self.input_chat.text().strip()
        if not text: return
        user_html = f'''<table width="100%" border="0" cellspacing="0" cellpadding="8" style="margin-top: 10px;"><tr><td align="right" valign="top"><div style="background-color: #004A77; color: #FFFFFF; padding: 12px 18px; border-radius: 8px; font-size: 16px; font-family: 'Microsoft YaHei'; display: inline-block; text-align: left;">{text}</div></td><td width="45" valign="top" align="center"><span style="font-size: 28px;">👨‍💻</span></td></tr></table>'''
        self.chat_history.append(user_html)
        self.input_chat.clear()
        think_html = '<div align="center" style="color: #9CA3AF; font-size: 14px; margin-top: 15px; margin-bottom: 15px;"><i>✨ AI 正在云端思考中，请稍候...</i></div>'
        self.chat_display.setHtml("".join(self.chat_history) + think_html)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
        QApplication.processEvents()

        context_data = ""
        check_text = text.lower()
        if "考勤" in check_text or "打卡" in check_text or "签到" in check_text:
            try:
                today_str = datetime.datetime.now().strftime('%Y-%m-%d')
                check_time = self.db.get_today_check_in(self.current_username)
                days = self.db.get_attendance_days(self.current_username)
                status_str = f"已签到 (打卡时间: {check_time.strftime('%H:%M:%S') if isinstance(check_time, datetime.datetime) else str(check_time).split()[-1]})" if check_time else "未签到"
                context_data = f"当前操作员账号：{self.current_username}\n今日 ({today_str}) 本人打卡状态：{status_str}\n本月累计全勤打卡天数：{days} 天"
                self.chat_history.append(
                    '<div align="center" style="color: #10B981; font-size: 13px; margin-top: 5px;"><i>[系统提示: 已成功截获考勤关键字，正在向大模型投喂您的个人打卡记录...]</i></div>')
                self.chat_display.setHtml("".join(self.chat_history) + think_html)
                QApplication.processEvents()
            except Exception as e:
                context_data = f"考勤查询失败：{e}"
        elif "违规" in check_text or "抓拍" in check_text or "处理" in check_text:
            try:
                records = self.db.get_records_by_user(self.current_username)
                today_str = datetime.datetime.now().strftime('%Y-%m-%d')
                today_records = [r for r in records if (
                    r['alert_time'].strftime('%Y-%m-%d') if isinstance(r['alert_time'], datetime.datetime) else
                    str(r['alert_time']).split(' ')[0]) == today_str]
                context_data = f"当前账号：{self.current_username}\n由本人历史累计处理违规：{len(records)} 起\n今日由本人处理违规：{len(today_records)} 起\n"
                recent_records = list(reversed(records))[:5]
                if recent_records:
                    context_data += "\n最新5条详情：\n"
                    for r in recent_records:
                        t = r['alert_time'].strftime('%m-%d %H:%M') if hasattr(r['alert_time'], 'strftime') else str(
                            r['alert_time'])
                        context_data += f"- [{t}] 事件:{r['event_type']}, 置信度:{r['confidence']}\n"
                self.chat_history.append(
                    '<div align="center" style="color: #10B981; font-size: 13px; margin-top: 5px;"><i>[系统提示: 已成功截获违规关键字，正在向大模型投喂您的业务记录...]</i></div>')
                self.chat_display.setHtml("".join(self.chat_history) + think_html)
                QApplication.processEvents()
            except Exception as e:
                context_data = f"违规数据查询失败：{e}"

        self.ai_thread = AIChatThread(text, role="operator", db_context=context_data)
        self.ai_thread.reply_signal.connect(self.receive_ai_reply)
        self.ai_thread.start()

    def receive_ai_reply(self, reply_text):
        html_text = reply_text.replace('\n', '<br>')
        ai_html = f'''<table width="100%" border="0" cellspacing="0" cellpadding="8" style="margin-top: 10px;"><tr><td width="45" valign="top" align="center"><span style="font-size: 28px;">🤖</span></td><td align="left" valign="top"><div style="background-color: #333537; color: #E3E3E3; padding: 12px 18px; border-radius: 8px; font-size: 16px; font-family: 'Microsoft YaHei'; line-height: 1.6; display: inline-block;">{html_text}</div></td></tr></table>'''
        self.chat_history.append(ai_html)
        self.chat_display.setHtml("".join(self.chat_history))
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def update_image_slider(self, value):
        self.current_conf_image = value / 100.0
        if hasattr(self, 'label_conf_image'): self.label_conf_image.setText(f"置信度: {self.current_conf_image:.2f}")
        if self.current_mode == 'image' and self.yolo_thread_1 and self.yolo_thread_1.isRunning():
            self.yolo_thread_1.set_threshold(self.current_conf_image)

    def update_video_slider(self, value):
        self.current_conf_video = value / 100.0
        if hasattr(self, 'label_conf_video'): self.label_conf_video.setText(f"置信度: {self.current_conf_video:.2f}")
        if self.current_mode == 'video' and self.yolo_thread_1 and self.yolo_thread_1.isRunning():
            self.yolo_thread_1.set_threshold(self.current_conf_video)

    def update_rt_slider(self, value):
        self.current_conf_rt = value / 100.0
        if hasattr(self, 'label_conf_rt'): self.label_conf_rt.setText(f"全局报警置信度: {self.current_conf_rt:.2f}")
        if self.current_mode == 'rt':
            for t in self.rt_threads.values():
                if t.isRunning(): t.set_threshold(self.current_conf_rt)

    # ─── 双击全屏/还原 ─────────────────────────────────────────────
    def eventFilter(self, obj, event):
        """捕获网格 QLabel 和全屏 QLabel 的双击事件"""
        if event.type() == QEvent.MouseButtonDblClick:
            role = obj.property("role") or ""
            cam_id = obj.property("cam_id") or ""
            if role == "rt_grid":
                # 网格双击 → 进入全屏
                if self.fullscreen_state["active"] and self.fullscreen_state["cam_id"] == cam_id:
                    # 已是当前通道的全屏，忽略
                    return True
                self._enter_fullscreen(cam_id)
                return True
            elif role == "fs_label":
                # 全屏画面双击 → 退出全屏
                self._exit_fullscreen()
                return True
        return super().eventFilter(obj, event)

    def _enter_fullscreen(self, cam_id):
        """将指定通道的画面弹出到独立全屏窗口"""
        if self.fullscreen_state["active"]:
            self._exit_fullscreen()

        dialog = QDialog(self)
        dialog.setWindowTitle(f"通道 {cam_id} - 全屏监控")
        dialog.setStyleSheet("background-color: #000000;")
        # 无边框全屏窗口
        dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)

        big_label = QLabel()
        big_label.setAlignment(Qt.AlignCenter)
        big_label.setStyleSheet("background-color: #000000;")
        big_label.setScaledContents(True)
        big_label.setProperty("role", "fs_label")
        big_label.setProperty("cam_id", cam_id)
        big_label.installEventFilter(self)
        big_label.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(big_label)

        self.fullscreen_state = {
            "active": True,
            "cam_id": cam_id,
            "dialog": dialog,
            "label": big_label,
        }

        dialog.showFullScreen()

    def _exit_fullscreen(self):
        """关闭全屏窗口，恢复网格显示"""
        if not self.fullscreen_state["active"]:
            return
        try:
            dialog = self.fullscreen_state["dialog"]
            if dialog:
                dialog.close()
                dialog.deleteLater()
        except Exception:
            pass
        self.fullscreen_state = {"active": False, "cam_id": None, "dialog": None, "label": None}

    def change_password(self):
        old_pwd, new_pwd = self.input_old_pwd.text(), self.input_new_pwd.text()
        if not old_pwd or not new_pwd: return QMessageBox.warning(self, "警告", "密码均不能为空！")
        if old_pwd == new_pwd: return QMessageBox.warning(self, "警告", "新密码不能相同！")
        try:
            success, msg = self.db.update_user_password(self.current_username, old_pwd, new_pwd)
            if success:
                QMessageBox.information(self, "成功", "密码修改成功！下次登录请使用新密码。")
                self.input_old_pwd.clear();
                self.input_new_pwd.clear()
            else:
                QMessageBox.warning(self, "失败", f"修改失败：{msg}")
        except:
            pass

    def change_email(self):
        new_email = self.input_new_email.text()
        if not new_email or "@" not in new_email: return QMessageBox.warning(self, "错误", "邮箱格式不正确！")
        try:
            success, msg = self.db.update_user_email(self.current_username, new_email)
            if success:
                self.settings.setValue(f"{self.current_username}_email", new_email)
                QMessageBox.information(self, "成功", f"绑定邮箱已同步！当前：{new_email}")
                self.input_new_email.clear()
        except:
            pass

    def scan_available_models(self):
        if not hasattr(self, 'combo_model'): return
        self.combo_model.clear()
        self.model_path_map = {}
        default_path = os.path.join(os.getcwd(), "runs", "detect", "train3", "weights", "best.pt")
        if os.path.exists(default_path):
            self.combo_model.addItem("best.pt (默认最优)")
            self.model_path_map["best.pt (默认最优)"] = default_path
        models_dir = os.path.join(os.getcwd(), "models")
        if not os.path.exists(models_dir): os.makedirs(models_dir)
        for file in os.listdir(models_dir):
            if file.endswith((".pt", ".engine", ".onnx")):
                name = f"{file} (本地模型)"
                self.combo_model.addItem(name)
                self.model_path_map[name] = os.path.join(models_dir, file)
        if self.combo_model.count() == 0:
            self.combo_model.addItem("⚠️ 未找到模型")
            self.model_path_map["⚠️ 未找到模型"] = default_path

    def load_system_settings(self):
        self.scan_available_models()
        saved_conf = self.settings.value(f"{self.current_username}_conf", 60, type=int)
        self.current_conf_image = self.current_conf_video = self.current_conf_rt = saved_conf / 100.0
        if hasattr(self, 'slider_default_conf'): self.slider_default_conf.setValue(saved_conf)
        if hasattr(self, 'slider_conf_image'): self.slider_conf_image.setValue(saved_conf)
        if hasattr(self, 'slider_conf_video'): self.slider_conf_video.setValue(saved_conf)
        if hasattr(self, 'slider_conf_rt'): self.slider_conf_rt.setValue(saved_conf)
        if hasattr(self, 'lbl_default_conf_val'): self.lbl_default_conf_val.setText(f"{saved_conf / 100.0:.2f}")

        self.custom_capture_path = self.settings.value(f"{self.current_username}_capture_path",
                                                       self.custom_capture_path)
        if hasattr(self, 'input_capture_path'): self.input_capture_path.setText(self.custom_capture_path)

        saved_model = self.settings.value(f"{self.current_username}_model", "best.pt (默认最优)")
        if hasattr(self, 'combo_model'):
            idx = self.combo_model.findText(saved_model)
            self.combo_model.setCurrentIndex(idx if idx >= 0 else 0)

        saved_device = self.settings.value(f"{self.current_username}_device", "自动检测最优硬件 (Auto)")
        if hasattr(self, 'combo_device'): self.combo_device.setCurrentText(saved_device)

        saved_cleanup = self.settings.value(f"{self.current_username}_cleanup", "永久保留 (需手动清理)")
        if hasattr(self, 'combo_cleanup'): self.combo_cleanup.setCurrentText(saved_cleanup)

        self.sound_alert_enabled = self.settings.value(f"{self.current_username}_sound", True, type=bool)
        if hasattr(self, 'check_sound_alert'): self.check_sound_alert.setChecked(self.sound_alert_enabled)

        self.alert_cooldown = self.settings.value(f"{self.current_username}_cooldown", 5, type=int)
        if hasattr(self, 'spin_cooldown'): self.spin_cooldown.setValue(self.alert_cooldown)
        if hasattr(self, 'lbl_profile_name'): self.lbl_profile_name.setText(f"当前用户: {self.current_username}")

        saved_channels = self.settings.value(f"{self.current_username}_rt_channels", [])
        if hasattr(self, 'list_channels'):
            self.list_channels.clear()
            if isinstance(saved_channels, str):
                saved_channels = [saved_channels]
            for ch in saved_channels:
                if ch: self.list_channels.addItem(ch)

        if hasattr(self, 'lbl_home_user'):
            self.lbl_home_user.setText(f"👤 当前用户: {self.current_username}")
            role_display = "👨‍🔧 操作员"
            conn = self.db.connect()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT role FROM users WHERE username=%s", (self.current_username,))
                        res = cursor.fetchone()
                        if res and res['role'] == 'admin': role_display = "👑 超级管理员"
                except:
                    pass
                finally:
                    conn.close()
            self.lbl_home_role.setText(f"🛡️ 角色: {role_display}")
            self.lbl_home_model.setText(f"🧠 模型: {self.combo_model.currentText().split()[0]}")
            self.lbl_home_device.setText(f"💻 设备: {saved_device.split()[0]}")

    def save_system_settings(self):
        if hasattr(self, 'slider_default_conf'):
            new_conf = self.slider_default_conf.value()
            self.settings.setValue(f"{self.current_username}_conf", new_conf)
            self.current_conf_image = self.current_conf_video = self.current_conf_rt = new_conf / 100.0
            self.slider_conf_image.setValue(new_conf)
            self.slider_conf_video.setValue(new_conf)
            self.slider_conf_rt.setValue(new_conf)
        if hasattr(self, 'input_capture_path'):
            self.custom_capture_path = self.input_capture_path.text()
            self.settings.setValue(f"{self.current_username}_capture_path", self.custom_capture_path)
        if hasattr(self, 'combo_model'): self.settings.setValue(f"{self.current_username}_model",
                                                                self.combo_model.currentText())
        if hasattr(self, 'combo_device'): self.settings.setValue(f"{self.current_username}_device",
                                                                 self.combo_device.currentText())
        if hasattr(self, 'combo_cleanup'): self.settings.setValue(f"{self.current_username}_cleanup",
                                                                  self.combo_cleanup.currentText())
        if hasattr(self, 'check_sound_alert'):
            self.sound_alert_enabled = self.check_sound_alert.isChecked()
            self.settings.setValue(f"{self.current_username}_sound", self.sound_alert_enabled)
        if hasattr(self, 'spin_cooldown'):
            self.alert_cooldown = self.spin_cooldown.value()
            self.settings.setValue(f"{self.current_username}_cooldown", self.alert_cooldown)
        if hasattr(self, 'combo_theme'):
            selected_theme = self.combo_theme.currentText()
            self.settings.setValue(f"{self.current_username}_theme", selected_theme)
            self.current_theme = selected_theme
            apply_theme(self, selected_theme)

        QMessageBox.information(self, "应用成功", "全局系统设置已保存！\n主题已即时生效。")
        self.load_system_settings()
        self.auto_cleanup_captures()

    def auto_cleanup_captures(self):
        cleanup_strategy = self.settings.value(f"{self.current_username}_cleanup", "永久保留 (需手动清理)")
        if "永久" in cleanup_strategy: return
        days_to_keep = 7 if "7 天" in cleanup_strategy else 30
        if not os.path.exists(self.custom_capture_path): return
        current_time = time.time()
        for filename in os.listdir(self.custom_capture_path):
            file_path = os.path.join(self.custom_capture_path, filename)
            if os.path.isfile(file_path):
                if (current_time - os.path.getctime(file_path)) / (24 * 3600) > days_to_keep:
                    try:
                        os.remove(file_path)
                    except:
                        pass

    def select_capture_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择路径", self.custom_capture_path)
        if dir_path: self.input_capture_path.setText(dir_path)

    def logout(self):
        self.stop_detection()
        self.close()
        from login_app import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()

    def browse_rt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择视频或摄像头流", "", "视频流文件 (*.mp4 *.avi)")
        if file_path:
            self.input_rtsp.setText(file_path)

    def add_rt_channel(self):
        url = self.input_rtsp.text().strip()
        if not url: return
        self.list_channels.addItem(url)
        self.input_rtsp.clear()
        self.save_rt_channels()

    def remove_rt_channel(self):
        row = self.list_channels.currentRow()
        if row >= 0:
            self.list_channels.takeItem(row)
            self.save_rt_channels()

    def save_rt_channels(self):
        if not hasattr(self, 'list_channels'): return
        channels = []
        for i in range(self.list_channels.count()):
            channels.append(self.list_channels.item(i).text())
        self.settings.setValue(f"{self.current_username}_rt_channels", channels)

    def start_rt_matrix(self):
        self.stop_detection()

        if self.list_channels.count() == 0:
            QMessageBox.warning(self, "提示", "请先在左侧通道库中添加至少一个监控视频流！")
            return

        self.current_mode = 'rt'
        if hasattr(self, 'table_rt_results'): self.table_rt_results.setRowCount(0)

        curr_model_name = self.combo_model.currentText() if hasattr(self, 'combo_model') else ""
        exact_model_path = getattr(self, 'model_path_map', {}).get(curr_model_name,
                                                                   r"runs\detect\train3\weights\best.pt")
        curr_device = self.combo_device.currentText() if hasattr(self, 'combo_device') else "Auto"
        curr_cd = self.alert_cooldown

        cols = 2
        for i in range(self.list_channels.count()):
            url = self.list_channels.item(i).text()
            source = int(url) if url.isdigit() else url
            source_type = 'webcam' if url.isdigit() else 'video'
            cam_id = f"CH_{i + 1}"

            cell_container = QtWidgets.QWidget()
            cell_container.setStyleSheet("background-color: #131314; border: 1px solid #333537; border-radius: 8px;")
            # 💥 物理枷锁 1：强制锁死每个监控格子的总高度！
            # 无论传进来的是 4K 还是 8K 视频，格子高度死死钉在 320 像素！
            cell_container.setFixedHeight(320)

            cell_layout = QtWidgets.QVBoxLayout(cell_container)
            cell_layout.setContentsMargins(10, 10, 10, 10)

            top_bar = QtWidgets.QHBoxLayout()
            lbl_title = QtWidgets.QLabel(f"📹 {cam_id}: {url[:25]}{'...' if len(url) > 25 else ''}")
            lbl_title.setStyleSheet("color: #E3E3E3; font-size: 14px; font-weight: bold; border: none;")
            lbl_fps = QtWidgets.QLabel("⚡ FPS: 0")
            lbl_fps.setStyleSheet("color: #10B981; font-size: 14px; font-weight: bold; border: none;")
            top_bar.addWidget(lbl_title)
            top_bar.addStretch()
            top_bar.addWidget(lbl_fps)

            lbl_display = QtWidgets.QLabel("正在加载引擎...")
            lbl_display.setAlignment(QtCore.Qt.AlignCenter)
            lbl_display.setStyleSheet("background-color: #000000; border-radius: 6px;")
            lbl_display.setScaledContents(True)
            # 🌟 安装事件过滤器以支持双击全屏
            lbl_display.setProperty("cam_id", cam_id)
            lbl_display.setProperty("role", "rt_grid")
            lbl_display.installEventFilter(self)
            lbl_display.setCursor(QCursor(Qt.PointingHandCursor))

            # 💥 物理枷锁 2：修改控件的尺寸策略为 Ignored
            # 彻底剥夺 QLabel 向父布局索要空间的权利，让它乖乖听从 Grid 的安排压缩图片
            from PyQt5.QtWidgets import QSizePolicy
            lbl_display.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

            cell_layout.addLayout(top_bar)
            cell_layout.addWidget(lbl_display, stretch=1)

            row = i // cols
            col = i % cols
            self.matrix_layout.addWidget(cell_container, row, col)

            self.rt_labels[cam_id] = {"display": lbl_display, "fps": lbl_fps}

            thread = YOLOThread(source, source_type, self.current_username, camera_id=cam_id,
                                module_name="实时监控", capture_dir=self.custom_capture_path,
                                model_path=exact_model_path, device_type=curr_device, cooldown=curr_cd)
            thread.set_threshold(self.current_conf_rt)
            thread.send_image_signal.connect(self.update_frame)
            thread.send_boxes_signal.connect(self.update_rt_stats)
            thread.send_alert_signal.connect(self.add_rt_alert_to_table)

            self.rt_threads[cam_id] = thread
            thread.start()

    def start_image(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "图片文件 (*.jpg *.png)")
        if file_paths: self.run_detection(source1=file_paths, mode='image')

    def start_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择视频", "", "视频文件 (*.mp4 *.avi)")
        if file_path:
            if hasattr(self, 'table_video_results'): self.table_video_results.setRowCount(0)
            self.run_detection(source1=file_path, mode='video')

    def run_detection(self, source1, source2=None, mode='image'):
        self.stop_detection()
        self.current_mode = mode
        curr_model_name = self.combo_model.currentText() if hasattr(self, 'combo_model') else ""
        exact_model_path = getattr(self, 'model_path_map', {}).get(curr_model_name,
                                                                   r"runs\detect\train3\weights\best.pt")
        curr_device = self.combo_device.currentText() if hasattr(self, 'combo_device') else "Auto"
        curr_cd = self.alert_cooldown

        source_type_1 = 'webcam' if isinstance(source1, int) or (isinstance(source1, str) and source1.isdigit()) else (
            'image' if mode == 'image' else 'video')
        module_name_1 = "图片识别" if mode == 'image' else "视频识别"

        self.yolo_thread_1 = YOLOThread(source1, source_type_1, self.current_username, camera_id="1",
                                        module_name=module_name_1, capture_dir=self.custom_capture_path,
                                        model_path=exact_model_path, device_type=curr_device, cooldown=curr_cd)

        if mode == 'image':
            self.yolo_thread_1.set_threshold(self.current_conf_image)
            self.yolo_thread_1.send_image_signal.connect(self.update_frame)
            self.yolo_thread_1.send_boxes_signal.connect(self.update_image_table)
            self.yolo_thread_1.start()
        elif mode == 'video':
            self.yolo_thread_1.set_threshold(self.current_conf_video)
            self.yolo_thread_1.send_image_signal.connect(self.update_frame)
            self.yolo_thread_1.send_boxes_signal.connect(self.update_video_stats)
            self.yolo_thread_1.send_alert_signal.connect(self.add_video_alert_to_table)
            self.yolo_thread_1.start()

    def update_frame(self, cam_id, orig_qt_img, qt_img):
        try:
            pixmap_orig = QPixmap.fromImage(orig_qt_img) if orig_qt_img else None
            pixmap_anno = QPixmap.fromImage(qt_img)

            if self.current_mode == 'image':
                if hasattr(self, 'label_image_original'): self.label_image_original.setPixmap(pixmap_orig)
                if hasattr(self, 'label_image_display'): self.label_image_display.setPixmap(pixmap_anno)
            elif self.current_mode == 'video':
                if hasattr(self, 'label_video_original'): self.label_video_original.setPixmap(pixmap_orig)
                if hasattr(self, 'label_video_display'): self.label_video_display.setPixmap(pixmap_anno)
            elif self.current_mode == 'rt':
                if cam_id in self.rt_labels:
                    self.rt_labels[cam_id]["display"].setPixmap(pixmap_anno)
                # 🌟 如果该通道正在全屏显示，同步更新全屏标签
                if self.fullscreen_state["active"] and self.fullscreen_state["cam_id"] == cam_id:
                    try:
                        self.fullscreen_state["label"].setPixmap(pixmap_anno)
                    except Exception:
                        pass
        except Exception as e:
            pass

    def update_image_table(self, cam_id, boxes_data_list, inference_time):
        if self.current_mode != 'image' or not hasattr(self, 'table_image_results'): return
        if hasattr(self, 'label_time_image'): self.label_time_image.setText(f"⏱ 检测耗时: {inference_time:.3f}s")
        if hasattr(self, 'label_targets_image'): self.label_targets_image.setText(
            f"🎯 检测目标: {len(boxes_data_list)} 个")
        self.table_image_results.setRowCount(0)
        for idx, box in enumerate(boxes_data_list):
            row_count = self.table_image_results.rowCount()
            self.table_image_results.insertRow(row_count)
            item_id = QTableWidgetItem(str(idx + 1))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table_image_results.setItem(row_count, 0, item_id)
            cls_text = "⚠️ " + box['cls'] if "未戴" in box['cls'] else "✅ " + box['cls']
            item_cls = QTableWidgetItem(cls_text)
            item_cls.setTextAlignment(Qt.AlignCenter)
            self.table_image_results.setItem(row_count, 1, item_cls)
            item_conf = QTableWidgetItem(f"{box['conf']:.2f}")
            item_conf.setTextAlignment(Qt.AlignCenter)
            self.table_image_results.setItem(row_count, 2, item_conf)
            x1, y1, x2, y2 = box['coords']
            item_coords = QTableWidgetItem(f"[{x1}, {y1}] - [{x2}, {y2}]")
            item_coords.setTextAlignment(Qt.AlignCenter)
            self.table_image_results.setItem(row_count, 3, item_coords)

    def update_video_stats(self, cam_id, boxes_data_list, inference_time):
        if self.current_mode != 'video': return
        fps = int(1.0 / inference_time) if inference_time > 0 else 0
        if hasattr(self, 'label_fps_video'): self.label_fps_video.setText(f"⚡ FPS: {fps}")
        if hasattr(self, 'label_targets_video'): self.label_targets_video.setText(
            f"🎯 画面目标: {len(boxes_data_list)} 个")

    def add_video_alert_to_table(self, cam_id, time_str, event_type, conf_str, img_path):
        if self.current_mode != 'video' or not hasattr(self, 'table_video_results'): return
        if self.sound_alert_enabled: self.trigger_system_beep()
        row_count = self.table_video_results.rowCount()
        self.table_video_results.insertRow(row_count)
        for col, text in enumerate([time_str, f"⚠️ {event_type}", conf_str]):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table_video_results.setItem(row_count, col, item)
        btn = self.create_view_button(img_path)
        self.table_video_results.setCellWidget(row_count, 3, btn)
        self.table_video_results.scrollToBottom()

    def update_rt_stats(self, cam_id, boxes_data_list, inference_time):
        try:
            if self.current_mode != 'rt': return
            fps = int(1.0 / inference_time) if inference_time > 0 else 0
            if cam_id in self.rt_labels:
                self.rt_labels[cam_id]["fps"].setText(f"⚡ FPS: {fps}")
        except Exception as e:
            pass

    def add_rt_alert_to_table(self, cam_id, time_str, event_type, conf_str, img_path):
        try:
            if self.current_mode != 'rt' or not hasattr(self, 'table_rt_results'): return
            if self.sound_alert_enabled: self.trigger_system_beep()
            row_count = self.table_rt_results.rowCount()
            self.table_rt_results.insertRow(row_count)
            texts = [time_str, f"🔗 {cam_id}", f"⚠️ {event_type}", conf_str]
            for col, text in enumerate(texts):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QBrush(QColor(255, 0, 0)))
                self.table_rt_results.setItem(row_count, col, item)
            btn = self.create_view_button(img_path)
            self.table_rt_results.setCellWidget(row_count, 4, btn)
            self.table_rt_results.scrollToBottom()
        except Exception as e:
            pass

    def update_personal_dashboard(self):
        records = self.db.get_records_by_user(self.current_username)
        total_intercepts = len(records)
        today_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        today_count = 0
        for r in records:
            alert_time = r['alert_time']
            date_str = alert_time.strftime('%Y-%m-%d') if isinstance(alert_time, datetime.datetime) else \
            str(alert_time).split(' ')[0]
            if date_str == today_date_str: today_count += 1
        if hasattr(self, 'lbl_personal_intercept'):
            self.lbl_personal_intercept.setText(f"🛡️ 累计处理违规: {total_intercepts} 起 (今日: {today_count} 起)")

    def trigger_system_beep(self):
        QApplication.beep()

    def show_snapshot(self, img_path):
        if not img_path or not os.path.exists(img_path): return QMessageBox.warning(self, "错误", "图片已丢失！")
        dialog = QDialog(self)
        dialog.setWindowTitle("违规抓拍详情与证据")
        dialog.resize(800, 600)
        dialog.setStyleSheet("background-color: #1E1F20;")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setPixmap(QPixmap(img_path))
        label.setScaledContents(True)
        layout.addWidget(label)
        dialog.exec_()

    def create_view_button(self, path):
        btn = QPushButton("🖼️ 查看抓拍")
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setStyleSheet(
            "QPushButton { background-color: #004A77; color: white; border-radius: 4px; padding: 5px; font-weight: bold; } QPushButton:hover { background-color: #005B94; }")
        btn.clicked.connect(lambda ch, p=path: self.show_snapshot(p))
        return btn

    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons): btn.setChecked(i == index)
        page_name = self.nav_buttons[index].text()
        if page_name == "历史记录":
            self.reset_history()
        elif page_name == "统计中心":
            self.update_statistics()
        elif page_name == "个人中心":
            self.update_personal_dashboard()

    def filter_history(self):
        if not hasattr(self, 'date_edit_history') or not hasattr(self, 'combo_event_type'): return
        self.load_history(filter_date=self.date_edit_history.date().toString('yyyy-MM-dd'),
                          filter_source=self.combo_event_type.currentText())

    def reset_history(self):
        if hasattr(self, 'combo_event_type'): self.combo_event_type.setCurrentIndex(0)
        self.load_history()

    def load_history(self, filter_date=None, filter_source="全部来源"):
        if not hasattr(self, 'table_history'): return
        records = self.db.get_records_by_user(self.current_username)
        self.table_history.setRowCount(0)
        for row in records:
            alert_time = row['alert_time']
            time_str = alert_time.strftime('%Y-%m-%d %H:%M:%S') if isinstance(alert_time, datetime.datetime) else str(
                alert_time)
            record_date_str = alert_time.strftime('%Y-%m-%d') if isinstance(alert_time, datetime.datetime) else \
            str(alert_time).split(' ')[0]
            event_type = row['event_type']
            conf = row['confidence']
            img_path = row.get('image_path', '')
            if filter_date and record_date_str != filter_date: continue
            if filter_source != "全部来源" and filter_source not in event_type: continue
            row_count = self.table_history.rowCount()
            self.table_history.insertRow(row_count)
            for col, text in enumerate([time_str, f"⚠️ {event_type}", conf]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if "未戴" in event_type: item.setForeground(QBrush(QColor(255, 0, 0)))
                self.table_history.setItem(row_count, col, item)
            btn = self.create_view_button(img_path)
            self.table_history.setCellWidget(row_count, 3, btn)
        if records: self.table_history.scrollToBottom()

    def init_charts(self):
        if not hasattr(self, 'layout_pie_chart'): return
        self.pie_chart = QChart()
        self.pie_chart.setTitle("违规来源分布")
        self.pie_chart.setTitleBrush(QColor("#E3E3E3"))
        self.pie_chart.setTitleFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.pie_chart.setBackgroundBrush(QColor("#1E1F20"))
        self.pie_chart.legend().setAlignment(Qt.AlignBottom)
        self.pie_chart.legend().setLabelBrush(QColor("#C4C7C5"))
        self.pie_view = QChartView(self.pie_chart)
        self.pie_view.setRenderHint(QPainter.Antialiasing)
        self.layout_pie_chart.addWidget(self.pie_view)

        self.bar_chart = QChart()
        self.bar_chart.setTitle("近7天违规趋势")
        self.bar_chart.setTitleBrush(QColor("#E3E3E3"))
        self.bar_chart.setTitleFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.bar_chart.setBackgroundBrush(QColor("#1E1F20"))
        self.bar_chart.legend().setVisible(False)
        self.bar_view = QChartView(self.bar_chart)
        self.bar_view.setRenderHint(QPainter.Antialiasing)
        self.layout_bar_chart.addWidget(self.bar_view)

    def update_statistics(self):
        if not hasattr(self, 'lbl_stat_total'): return
        records = self.db.get_records_by_user(self.current_username)
        total_alerts = len(records)
        today_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        today_alerts = 0
        sources_list = []
        for r in records:
            alert_time = r['alert_time']
            date_str = alert_time.strftime('%Y-%m-%d') if isinstance(alert_time, datetime.datetime) else \
            str(alert_time).split(' ')[0]
            if date_str == today_date_str: today_alerts += 1
            evt = r['event_type']
            source_name = "实时监控"
            if "图片识别" in evt:
                source_name = "图片识别"
            elif "视频识别" in evt:
                source_name = "视频识别"
            sources_list.append(source_name)
        source_counts = Counter(sources_list)
        top_source = source_counts.most_common(1)[0][0] if source_counts else "-"
        self.lbl_stat_total.setText(str(total_alerts))
        self.lbl_stat_today.setText(str(today_alerts))
        self.lbl_stat_source.setText(top_source)

        self.pie_chart.removeAllSeries()
        pie_series = QPieSeries()
        colors = {"实时监控": "#EF4444", "视频识别": "#F59E0B", "图片识别": "#3B82F6"}
        for source, count in source_counts.items():
            slice = pie_series.append(f"{source} ({count})", count)
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("#FFFFFF"))
            if source in colors: slice.setBrush(QColor(colors[source]))
        self.pie_chart.addSeries(pie_series)

        self.bar_chart.removeAllSeries()
        dates_last_7 = [(datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%m-%d') for i in
                        range(6, -1, -1)]
        date_counts = {d: 0 for d in dates_last_7}
        for r in records:
            alert_time = r['alert_time']
            d_str = alert_time.strftime('%m-%d') if isinstance(alert_time, datetime.datetime) else \
            str(alert_time).split(' ')[0][-5:]
            if d_str in date_counts: date_counts[d_str] += 1
        bar_set = QBarSet("违规次数")
        bar_set.setColor(QColor("#3B82F6"))
        for d in dates_last_7: bar_set.append(date_counts[d])
        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_series.setLabelsVisible(True)
        bar_series.setLabelsPosition(QBarSeries.LabelsOutsideEnd)
        self.bar_chart.addSeries(bar_series)

        for axis in self.bar_chart.axes(): self.bar_chart.removeAxis(axis)
        axisX = QBarCategoryAxis()
        axisX.append(dates_last_7)
        axisX.setLabelsColor(QColor("#9CA3AF"))
        axisX.setLinePenColor(QColor("#333537"))
        axisX.setGridLineVisible(False)
        self.bar_chart.addAxis(axisX, Qt.AlignBottom)
        bar_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%d")
        axisY.setLabelsColor(QColor("#9CA3AF"))
        axisY.setLinePenColor(QColor("#333537"))
        axisY.setGridLineColor(QColor("#333537"))
        max_val = max(date_counts.values()) if date_counts else 0
        axisY.setRange(0, max_val + max(2, int(max_val * 0.2)))
        self.bar_chart.addAxis(axisY, Qt.AlignLeft)
        bar_series.attachAxis(axisY)

    def stop_detection(self):
        # 🌟 停止检测时自动退出全屏模式
        self._exit_fullscreen()
        if hasattr(self, 'yolo_thread_1') and self.yolo_thread_1 and self.yolo_thread_1.isRunning():
            self.yolo_thread_1.is_running = False
            self.yolo_thread_1.wait()
            self.yolo_thread_1 = None

        if hasattr(self, 'rt_threads'):
            for t in list(self.rt_threads.values()):
                if t.isRunning():
                    t.is_running = False
                    t.wait()
            self.rt_threads.clear()

        if hasattr(self, 'label_image_display'):
            if hasattr(self, 'label_image_original'):
                self.label_image_original.clear()
                self.label_image_original.setText("原始图片\n等待上传...")
            self.label_image_display.clear()
            self.label_image_display.setText("YOLO 检测结果\n等待上传...")
            if hasattr(self, 'label_time_image'): self.label_time_image.setText("⏱ 检测耗时: 0.00s")
            if hasattr(self, 'label_targets_image'): self.label_targets_image.setText("🎯 检测目标: 0 个")

        if hasattr(self, 'label_video_display'):
            if hasattr(self, 'label_video_original'):
                self.label_video_original.clear()
                self.label_video_original.setText("原始视频源\n等待导入...")
            self.label_video_display.clear()
            self.label_video_display.setText("YOLO 检测结果\n等待导入...")
            if hasattr(self, 'label_fps_video'): self.label_fps_video.setText("⚡ FPS: 0")
            if hasattr(self, 'label_targets_video'): self.label_targets_video.setText("🎯 画面目标: 0 个")

        if hasattr(self, 'matrix_layout'):
            while self.matrix_layout.count():
                item = self.matrix_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
            self.rt_labels.clear()


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    app = QApplication(sys.argv)
    window = MainApp("dachui")
    window.showMaximized()
    sys.exit(app.exec_())