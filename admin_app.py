import sys
import os
import datetime
from collections import Counter
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout, QWidget, \
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal  # 引入了 QThread 方便模拟 AI 思考延迟
from PyQt5.QtGui import QCursor, QPixmap, QColor, QFont, QPainter

from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

from UI.admin_ui import Ui_AdminWindow
from core.db_helper import DBHelper


class AIChatThread(QThread):
    reply_signal = pyqtSignal(str)

    def __init__(self, user_message, role="operator", db_context=""):
        super().__init__()
        self.user_message = user_message
        self.role = role
        self.db_context = db_context

        self.api_key = "sk-c97f0269c1834b9ab2d109517b12fdd0"  # 🌟 别忘了填入你真实的 Key！
        self.api_url = "https://api.deepseek.com/chat/completions"

    def run(self):
        try:
            if self.role == "admin":
                sys_prompt = "你是智慧工地管控系统的超级管理员专属 AI 助理。请以专业、严谨的语气回答。"

                if self.db_context:
                    sys_prompt += f"""\n\n<database_result>\n{self.db_context}\n</database_result>\n\n【最高系统指令】：
            上方 <database_result> 标签内的内容是系统刚刚从后台 MySQL 数据库中实时捞取的绝对真实的底层数据！
            你的唯一任务是：根据上面的真实数据，用自然的人类语言向指挥官汇报。
            【绝对禁止】：严禁编造任何不在上面数据里的名字！严禁编造虚假的部门！如果有未打卡的人，照着上面的名单念；如果上面写了“无”，你就坚定地回答“今天所有人都已打卡”。绝对不要自己加戏！"""
                else:
                    # 🌟 核心松绑：管理端的柔性护栏！
                    sys_prompt += """\n\n【系统状态】：当前对话未触发数据库查询。
            【回答策略】：
            1. 正常交流：如果最高指挥官是在问候，或者咨询智慧工地系统的宏观管理、各板块的操作定义（如“员工管理怎么用”、“什么是置信度”），请运用你的专业知识详细解答。
            2. 拒绝幻想：只有当指挥官向你索要具体的后台数据（如“今天有多少人旷工”、“近期有多少违规”）时，你才回复：“由于权限与数据隔离，当前指令未触发后台检索。请在提问中包含‘查考勤’、‘查违规’、‘查员工’等关键字，或前往左侧大厅查看大盘数据。”
            【绝对禁令】：严禁凭空捏造任何假名字、假考勤或假违规记录！"""

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
                # 🌟 核心紧箍咒 3：把温度从 0.7 降到 0.1，彻底剥夺它的想象力！
                "temperature": 0.1
            }

            import requests
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            reply_text = result['choices'][0]['message']['content']

            self.reply_signal.emit(reply_text)

        except Exception as e:
            self.reply_signal.emit(f"⚠️ 网络异常或 AI 接口调用失败。\n(错误信息: {str(e)})")



class UserDialog(QDialog):
    def __init__(self, parent=None, user_data=None):
        super().__init__(parent)
        self.is_edit_mode = user_data is not None
        self.setWindowTitle("编辑员工信息" if self.is_edit_mode else "下发新员工账号")
        self.resize(400, 380)

        self.setStyleSheet("""
            QDialog { background-color: #1E1F20; color: #E3E3E3; }
            QLabel { font-size: 14px; font-weight: bold; color: #9CA3AF; }
            QLineEdit { background-color: #131314; border: 1px solid #333537; border-radius: 6px; padding: 10px; color: #E3E3E3; font-size: 14px;}
            QLineEdit:focus { border: 1px solid #004A77; }
            QComboBox { background-color: #131314; border: 1px solid #333537; border-radius: 6px; padding: 8px; color: #E3E3E3; font-size: 14px;}
            QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 14px;}
            QPushButton:hover { background-color: #005B94; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        self.inp_username = QLineEdit()
        self.inp_username.setPlaceholderText("系统账号 (如: zhangsan)")

        self.inp_pwd = QLineEdit()
        self.inp_pwd.setEchoMode(QLineEdit.Password)
        self.inp_pwd.setPlaceholderText("登录密码 (编辑时留空则不修改)" if self.is_edit_mode else "初始登录密码")

        self.inp_email = QLineEdit()
        self.inp_email.setPlaceholderText("密保邮箱 (必须包含 @)")

        self.combo_role = QComboBox()
        self.combo_role.addItems(["👨‍🔧 操作员 (operator)", "👑 超级管理员 (admin)"])

        layout.addWidget(QLabel("系统账号 (一旦创建不可修改):" if self.is_edit_mode else "系统账号:"))
        layout.addWidget(self.inp_username)
        layout.addWidget(QLabel("安全密码:"))
        layout.addWidget(self.inp_pwd)
        layout.addWidget(QLabel("密保邮箱:"))
        layout.addWidget(self.inp_email)
        layout.addWidget(QLabel("身份权限指派:"))
        layout.addWidget(self.combo_role)

        layout.addStretch()

        btn_box = QHBoxLayout()
        self.btn_save = QPushButton("💾 应用保存")
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setStyleSheet("background-color: #333537; color: white;")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

        btn_box.addWidget(self.btn_cancel)
        btn_box.addWidget(self.btn_save)
        layout.addLayout(btn_box)

        if self.is_edit_mode:
            self.inp_username.setText(user_data['username'])
            self.inp_username.setReadOnly(True)
            self.inp_username.setStyleSheet("background-color: #2D2F31; color: #64748B; border: 1px solid #333537;")
            self.inp_email.setText(user_data['email'])
            if user_data['role'] == 'admin':
                self.combo_role.setCurrentIndex(1)


class AdminWindow(QMainWindow, Ui_AdminWindow):
    def __init__(self, admin_username="admin"):
        super().__init__()
        self.admin_username = admin_username
        self.setupUi(self)
        self.db = DBHelper()

        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))

        self.btn_admin_logout.clicked.connect(self.logout)

        if hasattr(self, 'btn_profile_logout'):
            self.btn_profile_logout.clicked.connect(self.logout)
        if hasattr(self, 'btn_save_pwd'):
            self.btn_save_pwd.clicked.connect(self.change_password)
        if hasattr(self, 'btn_save_email'):
            self.btn_save_email.clicked.connect(self.change_email)

        self.btn_search_global.clicked.connect(self.filter_global_history)
        self.btn_reset_global.clicked.connect(self.reset_global_history)
        self.input_global_operator.returnPressed.connect(self.filter_global_history)

        self.btn_add_user_dialog.clicked.connect(self.handle_add_user)
        self.btn_search_user.clicked.connect(self.filter_users)
        self.btn_reset_user.clicked.connect(self.reset_users)
        self.input_search_user.returnPressed.connect(self.filter_users)

        self.btn_search_att.clicked.connect(self.load_attendance)

        # 🌟 绑定特权 AI 客服的大脑神经
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
                                    炒鸡管理员您好！我是您的专属 AI 大数据助理。您可以向我下达查询考勤、汇总违规记录等管理指令。
                                </div>
                            </td>
                        </tr>
                    </table>
                    '''
            self.chat_history.append(welcome_html)
            self.chat_display.setHtml("".join(self.chat_history))

        self.init_global_charts()
        self.init_attendance_charts()

        self.timer_clock = QTimer(self)
        self.timer_clock.timeout.connect(self.update_realtime_clock)
        self.timer_clock.start(1000)
        self.update_realtime_clock()

        self.update_admin_dashboard()
        self.load_all_records()
        self.load_users()
        self.load_attendance()

    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

        if index == 0:
            self.update_admin_dashboard()
        elif index == 1:
            self.load_all_records()
        elif index == 2:
            self.update_global_statistics()
        elif index == 3:
            self.reset_users()
        elif index == 4:
            self.load_attendance()

    # ==========================================
    # 🌟 AI 客服：上帝特供智能体
    # ==========================================
    def send_chat_message(self):
        text = self.input_chat.text().strip()
        if not text: return

        user_html = f'''
        <table width="100%" border="0" cellspacing="0" cellpadding="8" style="margin-top: 10px;">
            <tr>
                <td align="right" valign="top">
                    <div style="background-color: #004A77; color: #FFFFFF; padding: 12px 18px; border-radius: 8px; font-size: 16px; font-family: 'Microsoft YaHei'; display: inline-block; text-align: left;">
                        {text}
                    </div>
                </td>
                <td width="45" valign="top" align="center"><span style="font-size: 28px;">👑</span></td>
            </tr>
        </table>
        '''
        self.chat_history.append(user_html)
        self.input_chat.clear()

        think_html = '<div align="center" style="color: #9CA3AF; font-size: 14px; margin-top: 15px; margin-bottom: 15px;"><i>✨ 全知全能助理正在分析中...</i></div>'
        self.chat_display.setHtml("".join(self.chat_history) + think_html)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
        QApplication.processEvents()

        context_data = ""
        check_text = text.lower()

        # 1. 拦截【考勤】指令
        if "考勤" in check_text or "打卡" in check_text or "签到" in check_text:
            try:
                today_str = datetime.datetime.now().strftime('%Y-%m-%d')
                all_att = self.db.get_all_attendance()
                ops = [u['username'] for u in self.db.get_all_users() if u['role'] != 'admin']

                checked_in = []
                for a in all_att:
                    time_val = a['check_time']
                    time_str = time_val.strftime('%Y-%m-%d') if hasattr(time_val, 'strftime') else str(time_val)
                    if time_str.startswith(today_str):
                        checked_in.append(a['username'])

                not_checked_in = [op for op in ops if op not in checked_in]

                context_data = f"日期：{today_str}\n"
                context_data += f"系统注册的应到操作员：{len(ops)}人。实到：{len(checked_in)}人。未到：{len(not_checked_in)}人。\n"
                context_data += f"已完成打卡的员工账号：{', '.join(checked_in) if checked_in else '无'}\n"
                context_data += f"今日【旷工/未打卡】的员工账号：{', '.join(not_checked_in) if not_checked_in else '无'}"

                # 🌟 界面视觉反馈：明确告诉你底层已经去查库了！
                self.chat_history.append(
                    '<div align="center" style="color: #10B981; font-size: 13px; margin-top: 5px;"><i>[系统提示: 已成功截获考勤关键字，正在向大模型投喂最新数据库记录...]</i></div>')
                self.chat_display.setHtml("".join(self.chat_history) + think_html)
                QApplication.processEvents()

            except Exception as e:
                context_data = f"系统内部数据库查询异常：{e}"

        # 2. 拦截【违规】指令
        elif "违规" in check_text or "抓拍" in check_text or "安全帽" in check_text:
            try:
                all_records = self.db.get_all_records()
                today_str = datetime.datetime.now().strftime('%Y-%m-%d')

                # 🌟 Python 提前帮 AI 算好今天的数据总盘
                today_records = [r for r in all_records if str(r['alert_time']).startswith(today_str)]
                today_no_helmet = sum(
                    1 for r in today_records if "未戴安全帽" in r['event_type'] or "未佩戴安全帽" in r['event_type'])

                context_data = f"截至目前，系统历史累计记录了 {len(all_records)} 条违规。\n"
                context_data += f"重点注意：今日（{today_str}）共发生 {len(today_records)} 起违规抓拍，其中明确包含 {today_no_helmet} 起【未佩戴安全帽】事件！\n"

                # 依然附带最新的 10 条详情供 AI 举例用
                recent_records = all_records[:10]
                if recent_records:
                    context_data += "\n近期最新 10 条详情如下：\n"
                    for r in recent_records:
                        t = r['alert_time'].strftime('%m-%d %H:%M') if hasattr(r['alert_time'], 'strftime') else str(
                            r['alert_time'])
                        context_data += f"- [{t}] 经手人:{r['operator_name']}, 事件:{r['event_type']}, 置信度:{r['confidence']}\n"
                else:
                    context_data += "\n近期暂无违规明细。"

                self.chat_history.append(
                    '<div align="center" style="color: #10B981; font-size: 13px; margin-top: 5px;"><i>[系统提示: 已成功截获违规关键字，正在向大模型投喂今日违规统计与最新监控记录...]</i></div>')
                self.chat_display.setHtml("".join(self.chat_history) + think_html)
                QApplication.processEvents()

            except Exception as e:
                context_data = f"查询失败：{e}"

        # 把真实数据传给 AI
        self.ai_thread = AIChatThread(text, role="admin", db_context=context_data)
        self.ai_thread.reply_signal.connect(self.receive_ai_reply)
        self.ai_thread.start()

    def receive_ai_reply(self, reply_text):
        html_text = reply_text.replace('\n', '<br>')
        ai_html = f'''
        <table width="100%" border="0" cellspacing="0" cellpadding="8" style="margin-top: 10px;">
            <tr>
                <td width="45" valign="top" align="center"><span style="font-size: 28px;">🤖</span></td>
                <td align="left" valign="top">
                    <div style="background-color: #333537; color: #E3E3E3; padding: 12px 18px; border-radius: 8px; font-size: 16px; font-family: 'Microsoft YaHei'; line-height: 1.6; display: inline-block;">
                        {html_text}
                    </div>
                </td>
            </tr>
        </table>
        '''
        self.chat_history.append(ai_html)

        self.chat_display.setHtml("".join(self.chat_history))
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    # ==========================================
    # 🏠 首页大盘与全局同步
    # ==========================================
    def update_realtime_clock(self):
        now = datetime.datetime.now()
        if hasattr(self, 'lbl_realtime_clock'):
            self.lbl_realtime_clock.setText(now.strftime('%H:%M:%S'))

        if hasattr(self, 'lbl_admin_welcome'):
            hour = now.hour
            greeting = "早上好" if 5 <= hour < 12 else "下午好" if 12 <= hour < 18 else "晚上好"
            self.lbl_admin_welcome.setText(f"{greeting}，{self.admin_username}")

    def update_admin_dashboard(self):
        if hasattr(self, 'lbl_home_user'):
            self.lbl_home_user.setText(f"👤 当前用户: {self.admin_username}")

        if hasattr(self, 'lbl_profile_name'):
            self.lbl_profile_name.setText(f"当前用户: {self.admin_username}")

        users = self.db.get_all_users()
        self.lbl_total_users.setText(str(len(users)))

        records = self.db.get_all_records()
        self.lbl_total_alerts.setText(str(len(records)))

        att_data = self.db.get_all_attendance()
        today_str = datetime.datetime.now().strftime('%Y-%m-%d')
        today_count = sum(1 for a in att_data if str(a['check_time']).startswith(today_str))
        self.lbl_today_att.setText(str(today_count))

    # ==========================================
    # 🌍 历史记录 (原天眼)
    # ==========================================
    def filter_global_history(self):
        selected_date = self.date_edit_global.date().toString('yyyy-MM-dd')
        selected_op = self.input_global_operator.text().strip()
        self.load_all_records(filter_date=selected_date, filter_operator=selected_op)

    def reset_global_history(self):
        self.input_global_operator.clear()
        self.load_all_records()

    def load_all_records(self, filter_date=None, filter_operator=""):
        records = self.db.get_all_records()
        self.table_all_records.setRowCount(0)

        for r in records:
            alert_time = r['alert_time']
            time_str = alert_time.strftime('%Y-%m-%d %H:%M:%S') if hasattr(alert_time, 'strftime') else str(alert_time)
            record_date_str = time_str.split(' ')[0]
            operator = r['operator_name']

            if filter_date and record_date_str != filter_date:
                continue
            if filter_operator and filter_operator.lower() not in operator.lower():
                continue

            row_count = self.table_all_records.rowCount()
            self.table_all_records.insertRow(row_count)

            evt = r['event_type']
            conf = r['confidence']
            img_path = r['image_path']

            for col, text in enumerate([time_str, f"👨‍🔧 {operator}", f"⚠️ {evt}", conf]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 2: item.setForeground(QColor("#EF4444"))
                if col == 1: item.setForeground(QColor("#66B2FF"))
                self.table_all_records.setItem(row_count, col, item)

            btn = QPushButton("🖼️ 查看全局抓拍")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(
                "background-color: #004A77; color: white; border-radius: 4px; padding: 5px; font-weight: bold;")
            btn.clicked.connect(lambda ch, p=img_path: self.show_snapshot(p))

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            self.table_all_records.setCellWidget(row_count, 4, widget)

    def show_snapshot(self, img_path):
        if not img_path or not os.path.exists(img_path):
            QMessageBox.warning(self, "错误", "抓拍图片文件已被删除或丢失！")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("全局违规证据追溯")
        dialog.resize(800, 600)
        dialog.setStyleSheet("background-color: #1E1F20;")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        pixmap = QPixmap(img_path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        layout.addWidget(label)
        dialog.exec_()

        # ==========================================

    # 📈 统计中心
    # ==========================================
    def init_global_charts(self):
        self.global_pie = QChart()
        self.global_pie.setTitle("全站操作员违规捕获占比")
        self.global_pie.setTitleBrush(QColor("#E3E3E3"))
        self.global_pie.setTitleFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.global_pie.setBackgroundBrush(QColor("#1E1F20"))
        self.global_pie.legend().setAlignment(Qt.AlignBottom)
        self.global_pie.legend().setLabelBrush(QColor("#9CA3AF"))
        self.pie_view = QChartView(self.global_pie)
        self.pie_view.setRenderHint(QPainter.Antialiasing)
        self.layout_global_pie.addWidget(self.pie_view)

        self.global_bar = QChart()
        self.global_bar.setTitle("全站近7天违规预警大盘走势")
        self.global_bar.setTitleBrush(QColor("#E3E3E3"))
        self.global_bar.setTitleFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.global_bar.setBackgroundBrush(QColor("#1E1F20"))
        self.global_bar.legend().setVisible(False)
        self.bar_view = QChartView(self.global_bar)
        self.bar_view.setRenderHint(QPainter.Antialiasing)
        self.layout_global_bar.addWidget(self.bar_view)

    def update_global_statistics(self):
        records = self.db.get_all_records()
        operator_list = [r['operator_name'] for r in records]
        op_counts = Counter(operator_list)

        self.global_pie.removeAllSeries()
        pie_series = QPieSeries()
        colors = ["#004A77", "#66B2FF", "#10B981", "#F59E0B", "#EF4444"]
        for i, (op, count) in enumerate(op_counts.items()):
            slice = pie_series.append(f"{op} ({count})", count)
            slice.setLabelVisible(True)
            slice.setLabelColor(QColor("#E3E3E3"))
            slice.setBrush(QColor(colors[i % len(colors)]))
        self.global_pie.addSeries(pie_series)

        self.global_bar.removeAllSeries()
        dates_last_7 = []
        for i in range(6, -1, -1):
            d = datetime.datetime.now() - datetime.timedelta(days=i)
            dates_last_7.append(d.strftime('%m-%d'))

        date_counts = {d: 0 for d in dates_last_7}
        for r in records:
            alert_time = r['alert_time']
            d_str = alert_time.strftime('%m-%d') if hasattr(alert_time, 'strftime') else str(alert_time).split(' ')[0][
                -5:]
            if d_str in date_counts:
                date_counts[d_str] += 1

        bar_set = QBarSet("全站违规次数")
        bar_set.setColor(QColor("#66B2FF"))
        for d in dates_last_7: bar_set.append(date_counts[d])

        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_series.setLabelsVisible(True)
        bar_series.setLabelsPosition(QBarSeries.LabelsOutsideEnd)
        self.global_bar.addSeries(bar_series)

        for axis in self.global_bar.axes(): self.global_bar.removeAxis(axis)

        axisX = QBarCategoryAxis()
        axisX.append(dates_last_7)
        axisX.setLabelsColor(QColor("#9CA3AF"))
        axisX.setLinePenColor(QColor("#333537"))
        axisX.setGridLineVisible(False)
        self.global_bar.addAxis(axisX, Qt.AlignBottom)
        bar_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%d")
        axisY.setLabelsColor(QColor("#9CA3AF"))
        axisY.setLinePenColor(QColor("#333537"))
        axisY.setGridLineColor(QColor("#333537"))
        max_val = max(date_counts.values()) if date_counts else 0
        axisY.setRange(0, max_val + max(2, int(max_val * 0.2)))
        self.global_bar.addAxis(axisY, Qt.AlignLeft)
        bar_series.attachAxis(axisY)

    # ==========================================
    # 👥 员工管理
    # ==========================================
    def filter_users(self):
        keyword = self.input_search_user.text().strip().lower()
        self.load_users(keyword)

    def reset_users(self):
        self.input_search_user.clear()
        self.load_users()

    def load_users(self, search_keyword=""):
        users = self.db.get_all_users()
        self.table_users.setRowCount(0)

        for u in users:
            uid = str(u['id'])
            username = u['username']
            role = "👑 超级管理员" if u['role'] == 'admin' else "👨‍🔧 操作员"
            email = u['email']

            if search_keyword:
                if search_keyword not in uid and search_keyword not in username.lower():
                    continue

            row_count = self.table_users.rowCount()
            self.table_users.insertRow(row_count)

            for col, text in enumerate([uid, username, role, email]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if u['role'] == 'admin': item.setForeground(QColor("#F59E0B"))
                self.table_users.setItem(row_count, col, item)

            if username == 'admin':
                item_protect = QTableWidgetItem("🛡️ 根账号不可操作")
                item_protect.setTextAlignment(Qt.AlignCenter)
                item_protect.setForeground(QColor("#9CA3AF"))
                self.table_users.setItem(row_count, 4, item_protect)
            else:
                btn_edit = QPushButton("✏️ 编辑")
                btn_edit.setCursor(QCursor(Qt.PointingHandCursor))
                btn_edit.setStyleSheet(
                    "background-color: #004A77; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold;")
                btn_edit.clicked.connect(lambda ch, user_data=u: self.handle_edit_user(user_data))

                btn_del = QPushButton("❌ 开除")
                btn_del.setCursor(QCursor(Qt.PointingHandCursor))
                btn_del.setStyleSheet(
                    "background-color: #E11D48; color: white; border-radius: 4px; padding: 5px 12px; font-weight: bold;")
                btn_del.clicked.connect(lambda ch, target=username: self.delete_operator(target))

                widget = QWidget()
                layout = QHBoxLayout(widget)
                layout.setContentsMargins(10, 2, 10, 2)
                layout.setSpacing(15)
                layout.addWidget(btn_edit)
                layout.addWidget(btn_del)
                layout.setAlignment(Qt.AlignCenter)
                self.table_users.setCellWidget(row_count, 4, widget)

    def handle_add_user(self):
        dialog = UserDialog(self)
        if dialog.exec_():
            user = dialog.inp_username.text().strip()
            pwd = dialog.inp_pwd.text().strip()
            email = dialog.inp_email.text().strip()
            role_text = dialog.combo_role.currentText()
            role = 'admin' if 'admin' in role_text else 'operator'

            if not user or not pwd or not email:
                QMessageBox.warning(self, "警告", "所有字段均为必填项！")
                return
            if "@" not in email:
                QMessageBox.warning(self, "警告", "邮箱格式不合法！")
                return

            success = self.db.register_user(user, pwd, email, role)
            if success:
                QMessageBox.information(self, "下发成功", f"员工账号 {user} 已成功创建！")
                self.load_users()
                self.update_admin_dashboard()
            else:
                QMessageBox.warning(self, "失败", "该系统账号可能已存在！")

    def handle_edit_user(self, user_data):
        dialog = UserDialog(self, user_data)
        if dialog.exec_():
            uid = user_data['id']
            new_pwd = dialog.inp_pwd.text().strip()
            new_email = dialog.inp_email.text().strip()
            role_text = dialog.combo_role.currentText()
            new_role = 'admin' if 'admin' in role_text else 'operator'

            if not new_email or "@" not in new_email:
                QMessageBox.warning(self, "警告", "请填入合法的邮箱地址！")
                return

            success, msg = self.db.edit_user(uid, new_role, new_email, new_pwd)
            if success:
                QMessageBox.information(self, "更新成功", "员工信息已保存至数据库！")
                self.load_users()
            else:
                QMessageBox.warning(self, "更新失败", msg)

    def delete_operator(self, username):
        reply = QMessageBox.question(self, '终极警告',
                                     f"⚠️ 危险操作！\n\n确定要永久开除员工【{username}】并销毁其所有凭证吗？此操作不可逆！",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            success, msg = self.db.delete_user(username)
            if success:
                QMessageBox.information(self, "裁决成功", msg)
                self.load_users()
                self.update_admin_dashboard()
            else:
                QMessageBox.warning(self, "裁决失败", msg)

    # ==========================================
    # 📅 考勤中心
    # ==========================================
    def init_attendance_charts(self):
        self.att_pie = QChart()
        self.att_pie.setTitle("当日签到率透视")
        self.att_pie.setTitleBrush(QColor("#E3E3E3"))
        self.att_pie.setTitleFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.att_pie.setBackgroundBrush(QColor("#1E1F20"))
        self.att_pie.legend().setAlignment(Qt.AlignBottom)
        self.att_pie.legend().setLabelBrush(QColor("#9CA3AF"))
        self.att_pie_view = QChartView(self.att_pie)
        self.att_pie_view.setRenderHint(QPainter.Antialiasing)
        self.layout_att_pie.addWidget(self.att_pie_view)

        self.att_bar = QChart()
        self.att_bar.setTitle("全站近 7 天签到走势")
        self.att_bar.setTitleBrush(QColor("#E3E3E3"))
        self.att_bar.setTitleFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.att_bar.setBackgroundBrush(QColor("#1E1F20"))
        self.att_bar.legend().setVisible(False)
        self.att_bar_view = QChartView(self.att_bar)
        self.att_bar_view.setRenderHint(QPainter.Antialiasing)
        self.layout_att_bar.addWidget(self.att_bar_view)

    def load_attendance(self):
        target_date_str = self.date_edit_att.date().toString('yyyy-MM-dd')
        all_users = self.db.get_all_users()
        ops = [u for u in all_users if u['role'] != 'admin']
        total_ops = len(ops)

        all_att = self.db.get_all_attendance()
        att_map = {}
        for a in all_att:
            ctime = a['check_time']
            time_str = ctime.strftime('%Y-%m-%d %H:%M:%S') if hasattr(ctime, 'strftime') else str(ctime)
            d_str = time_str.split(' ')[0]
            if d_str == target_date_str:
                att_map[a['username']] = time_str

        self.table_attendance.setRowCount(0)
        checked_in_count = 0

        for op in ops:
            uname = op['username']
            role_str = "👨‍🔧 操作员"
            row_count = self.table_attendance.rowCount()
            self.table_attendance.insertRow(row_count)

            if uname in att_map:
                status = "✅ 已签到"
                time_display = att_map[uname]
                checked_in_count += 1
            else:
                status = "❌ 未签到"
                time_display = "-"

            for col, text in enumerate([uname, role_str, status, time_display]):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 2:
                    item.setForeground(QColor("#10B981") if "已" in status else QColor("#EF4444"))
                    item.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
                self.table_attendance.setItem(row_count, col, item)

        self.att_pie.removeAllSeries()
        pie_series = QPieSeries()

        if total_ops > 0:
            slice1 = pie_series.append(f"已签到 ({checked_in_count})", checked_in_count)
            slice1.setBrush(QColor("#004A77"))
            slice1.setLabelColor(QColor("#E3E3E3"))
            slice1.setLabelVisible(True)

            not_checked = total_ops - checked_in_count
            if not_checked > 0:
                slice2 = pie_series.append(f"未签到 ({not_checked})", not_checked)
                slice2.setBrush(QColor("#EF4444"))
                slice2.setLabelColor(QColor("#E3E3E3"))
                slice2.setLabelVisible(True)
        self.att_pie.addSeries(pie_series)

        target_date_obj = datetime.datetime.strptime(target_date_str, '%Y-%m-%d')
        dates_last_7 = [(target_date_obj - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

        daily_counts = {d: 0 for d in dates_last_7}
        for a in all_att:
            ctime = a['check_time']
            time_str = ctime.strftime('%Y-%m-%d %H:%M:%S') if hasattr(ctime, 'strftime') else str(ctime)
            d_str = time_str.split(' ')[0]
            if d_str in daily_counts:
                daily_counts[d_str] += 1

        self.att_bar.removeAllSeries()
        bar_set = QBarSet("当日签到总人数")
        bar_set.setColor(QColor("#10B981"))
        for d in dates_last_7:
            bar_set.append(daily_counts[d])

        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_series.setLabelsVisible(True)
        bar_series.setLabelsPosition(QBarSeries.LabelsOutsideEnd)
        self.att_bar.addSeries(bar_series)

        for axis in self.att_bar.axes(): self.att_bar.removeAxis(axis)

        axisX = QBarCategoryAxis()
        axisX.append([d[-5:] for d in dates_last_7])
        axisX.setLabelsColor(QColor("#9CA3AF"))
        axisX.setLinePenColor(QColor("#333537"))
        axisX.setGridLineVisible(False)
        self.att_bar.addAxis(axisX, Qt.AlignBottom)
        bar_series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%d")
        axisY.setLabelsColor(QColor("#9CA3AF"))
        axisY.setLinePenColor(QColor("#333537"))
        axisY.setGridLineColor(QColor("#333537"))
        max_val = max(daily_counts.values()) if daily_counts else 0
        axisY.setRange(0, max_val + max(2, int(max_val * 0.2)))
        self.att_bar.addAxis(axisY, Qt.AlignLeft)
        bar_series.attachAxis(axisY)

    # ==========================================
    # 👤 个人中心
    # ==========================================
    def change_password(self):
        old_pwd = self.input_old_pwd.text()
        new_pwd = self.input_new_pwd.text()
        if not old_pwd or not new_pwd:
            QMessageBox.warning(self, "警告", "原密码和新密码均不能为空！")
            return
        if old_pwd == new_pwd:
            QMessageBox.warning(self, "警告", "新密码不能与原密码相同！")
            return
        success, msg = self.db.update_user_password(self.admin_username, old_pwd, new_pwd)
        if success:
            QMessageBox.information(self, "成功", "密码修改成功！下次登录请使用新密码。")
            self.input_old_pwd.clear()
            self.input_new_pwd.clear()
        else:
            QMessageBox.warning(self, "失败", f"密码修改失败：{msg}")

    def change_email(self):
        new_email = self.input_new_email.text()
        if not new_email or "@" not in new_email:
            QMessageBox.warning(self, "格式错误", "请输入有效的邮箱地址！")
            return
        success, msg = self.db.update_user_email(self.admin_username, new_email)
        if success:
            QMessageBox.information(self, "绑定成功", f"绑定邮箱已成功同步至数据库！\n当前邮箱为：{new_email}")
            self.input_new_email.clear()
        else:
            QMessageBox.warning(self, "失败", f"邮箱写入数据库失败：{msg}")

    # ==========================================
    # 🚪 回退到登录大门
    # ==========================================
    def logout(self):
        reply = QMessageBox.question(self, '退出', "确定要离开管理员大厅吗？", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            from login_app import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AdminWindow()
    win.show()
    sys.exit(app.exec_())