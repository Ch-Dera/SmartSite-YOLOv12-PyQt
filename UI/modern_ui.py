# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModernWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 750))
        MainWindow.setWindowTitle("智慧工地安全管控系统 - 操作员大厅")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setStyleSheet("""
            * { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; 
                font-size: 15px; 
            }
            QWidget#centralwidget { background-color: #131314; }
            QWidget#left_sidebar { background-color: #1E1F20; border-right: 1px solid #333537; }
            QLabel#label_main_title { font-size: 22px; font-weight: bold; color: #FFFFFF; padding-top: 30px; }
            QLabel#label_sub_title { font-size: 13px; color: #9CA3AF; padding-bottom: 25px; border-bottom: 1px solid #333537; margin-bottom: 15px; letter-spacing: 2px;}

            QPushButton[class="nav_btn"] { background-color: transparent; color: #C4C7C5; font-size: 16px; text-align: center; border: 1px solid transparent; border-radius: 24px; font-weight: normal; }
            QPushButton[class="nav_btn"]:hover { background-color: #333537; color: #FFFFFF; }
            QPushButton[class="nav_btn"]:checked { background-color: #004A77; color: #C3E7FF; font-weight: bold; border: 1px solid #004A77; border-radius: 24px; }
            QLabel[class="page_title"] { font-size: 28px; font-weight: bold; color: #E3E3E3; }

            QTableWidget { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; gridline-color: transparent; font-size: 15px; color: #E3E3E3; padding: 5px; }
            QHeaderView::section { background-color: #1E1F20; color: #9CA3AF; font-weight: bold; font-size: 15px; padding: 15px; border: none; border-bottom: 1px solid #333537; }
            QTableWidget::item { border-bottom: 1px solid #131314; padding: 8px; }
            QTableWidget::item:selected { background-color: #004A77; color: #FFFFFF; }

            QLineEdit { background-color: #131314; border: 1px solid #333537; border-radius: 6px; padding: 0px 15px; min-height: 38px; color: #E3E3E3; font-size: 15px; }
            QLineEdit:focus { border: 1px solid #66B2FF; }

            QDateEdit { background-color: #1E1F20; color: #E3E3E3; border: 1px solid #333537; border-radius: 6px; padding: 6px 10px; font-size: 15px; min-width: 120px; }
            QDateEdit:hover { border: 1px solid #004A77; }
            QComboBox { background-color: #1E1F20; color: #E3E3E3; border: 1px solid #333537; border-radius: 6px; padding: 6px 10px; font-size: 15px; }
            QComboBox:hover { border: 1px solid #004A77; }
            QComboBox QAbstractItemView { background-color: #1E1F20; color: #E3E3E3; selection-background-color: #004A77; }

            QTabWidget::pane { border: 1px solid #333537; background: #1E1F20; border-radius: 8px; top: -1px; }
            QTabBar::tab { background: #131314; color: #9CA3AF; border: 1px solid #333537; padding: 10px 25px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px; }
            QTabBar::tab:selected { background: #1E1F20; color: #66B2FF; font-weight: bold; border-bottom-color: #1E1F20; }
            QTabBar::tab:hover:!selected { background: #2D2F31; color: #E3E3E3; }
            QWidget#tab_workspace, QWidget#tab_security { background-color: #1E1F20; }
            QCheckBox { color: #E3E3E3; font-size: 15px; }
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 1px solid #333537; background-color: #131314; }
            QCheckBox::indicator:checked { background-color: #004A77; border: 1px solid #004A77; image: url(check.png); }
            QCheckBox::indicator:hover { border: 1px solid #66B2FF; }
            
            QSpinBox { background-color: #131314; color: #E3E3E3; border: 1px solid #333537; border-radius: 6px; padding: 5px 10px; min-height: 25px; font-size: 15px; }
            QSpinBox:focus, QSpinBox:hover { border: 1px solid #66B2FF; }
            QSpinBox::up-button, QSpinBox::down-button { width: 20px; background-color: transparent; border-left: 1px solid #333537; }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { background-color: #333537; }
        """)

        self.horizontalLayout_main = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_main.setSpacing(0)

        self.left_sidebar = QtWidgets.QWidget(self.centralwidget)
        self.left_sidebar.setObjectName("left_sidebar")
        self.verticalLayout_nav = QtWidgets.QVBoxLayout(self.left_sidebar)
        self.verticalLayout_nav.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_nav.setSpacing(6)

        self.label_main_title = QtWidgets.QLabel("智慧工地管控系统")
        self.label_main_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main_title.setObjectName("label_main_title")
        self.verticalLayout_nav.addWidget(self.label_main_title)

        self.label_sub_title = QtWidgets.QLabel("YOLOv12 安全帽检测平台")
        self.label_sub_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sub_title.setObjectName("label_sub_title")
        self.verticalLayout_nav.addWidget(self.label_sub_title)

        self.nav_buttons = []
        btn_names = ["系统首页", "图片检测", "视频检测", "实时监控", "历史记录", "统计中心", "个人中心", "系统设置",
                     "AI 助手"]

        for i, name in enumerate(btn_names):
            btn = QtWidgets.QPushButton(self.left_sidebar)
            btn.setProperty("class", "nav_btn")
            btn.setCheckable(True)
            btn.setText(name)
            btn.setFixedSize(210, 48)
            if i == 0: btn.setChecked(True)
            self.verticalLayout_nav.addWidget(btn, 0, QtCore.Qt.AlignHCenter)
            self.nav_buttons.append(btn)

        spacerItem_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                  QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_nav.addItem(spacerItem_bottom)
        self.horizontalLayout_main.addWidget(self.left_sidebar)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.pages = []
        for i, name in enumerate(btn_names):
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(page)
            layout.setContentsMargins(50, 50, 50, 50)

            title_label = QtWidgets.QLabel(name)
            title_label.setProperty("class", "page_title")
            layout.addWidget(title_label)

            screen_style = "QLabel { background-color: #0A0A0A; border: 1px solid #333537; border-radius: 12px; font-size: 20px; color: #4B5563; font-weight: bold; margin-top: 10px; margin-bottom: 10px; }"

            # 🏠 房间 0：系统首页
            if name == "系统首页":
                home_layout = QtWidgets.QVBoxLayout()
                home_layout.setSpacing(30)
                card_welcome = QtWidgets.QWidget()
                card_welcome.setStyleSheet(
                    "QWidget { background-color: #1E1F22; border: 1px solid #393B40; border-radius: 12px; }")
                wel_layout = QtWidgets.QHBoxLayout(card_welcome)
                wel_layout.setContentsMargins(40, 40, 40, 40)
                wel_text_layout = QtWidgets.QVBoxLayout()
                self.lbl_welcome_title = QtWidgets.QLabel("早上好，管理员")
                self.lbl_welcome_title.setStyleSheet(
                    "color: #FFFFFF; font-size: 36px; font-weight: bold; border: none;")
                self.lbl_welcome_sub = QtWidgets.QLabel("欢迎使用智慧工地安全管控平台，今天也是守护工地安全的一天。")
                self.lbl_welcome_sub.setStyleSheet("color: #9CA3AF; font-size: 16px; border: none; margin-top: 10px;")
                wel_text_layout.addWidget(self.lbl_welcome_title)
                wel_text_layout.addWidget(self.lbl_welcome_sub)

                info_bar_layout = QtWidgets.QHBoxLayout()
                info_bar_layout.setSpacing(12)
                badge_style = "background-color: #2D2F31; color: #66B2FF; padding: 8px 15px; border-radius: 6px; font-size: 14px; font-weight: bold; border: 1px solid #333537;"
                self.lbl_home_user = QtWidgets.QLabel("👤 当前用户: admin")
                self.lbl_home_user.setStyleSheet(badge_style)
                self.lbl_home_role = QtWidgets.QLabel("🛡️ 角色: 操作员")
                self.lbl_home_role.setStyleSheet(badge_style)
                self.lbl_home_model = QtWidgets.QLabel("🧠 模型: best.pt")
                self.lbl_home_model.setStyleSheet(badge_style)
                self.lbl_home_device = QtWidgets.QLabel("💻 设备: Auto")
                self.lbl_home_device.setStyleSheet(badge_style)

                info_bar_layout.addWidget(self.lbl_home_user)
                info_bar_layout.addWidget(self.lbl_home_role)
                info_bar_layout.addWidget(self.lbl_home_model)
                info_bar_layout.addWidget(self.lbl_home_device)
                info_bar_layout.addStretch()
                wel_text_layout.addLayout(info_bar_layout)

                self.lbl_realtime_clock = QtWidgets.QLabel("00:00:00")
                self.lbl_realtime_clock.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.lbl_realtime_clock.setStyleSheet(
                    "color: #66B2FF; font-size: 58px; font-weight: 900; font-family: 'Arial'; border: none; letter-spacing: 2px;")
                wel_layout.addLayout(wel_text_layout)
                wel_layout.addStretch()
                wel_layout.addWidget(self.lbl_realtime_clock)
                home_layout.addWidget(card_welcome, stretch=2)

                mid_layout = QtWidgets.QHBoxLayout()
                mid_layout.setSpacing(30)
                card_quick = QtWidgets.QWidget()
                card_quick.setStyleSheet(
                    "QWidget { background-color: #1E1F22; border: 1px solid #393B40; border-radius: 12px; }")
                quick_layout = QtWidgets.QVBoxLayout(card_quick)
                quick_layout.setContentsMargins(30, 30, 30, 30)
                lbl_quick = QtWidgets.QLabel("🚀 快捷指挥枢纽")
                lbl_quick.setStyleSheet(
                    "color: #E6E8EA; font-size: 18px; font-weight: bold; border: none; margin-bottom: 15px;")
                quick_layout.addWidget(lbl_quick)
                btn_box = QtWidgets.QHBoxLayout()
                btn_box.setSpacing(20)
                self.btn_quick_img = QtWidgets.QPushButton("🖼️ 图片识别")
                self.btn_quick_vid = QtWidgets.QPushButton("🎥 视频识别")
                self.btn_quick_rt = QtWidgets.QPushButton("🚨 实时监控")
                for b in [self.btn_quick_img, self.btn_quick_vid, self.btn_quick_rt]:
                    b.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    b.setFixedSize(160, 80)
                    b.setStyleSheet(
                        "QPushButton { background-color: #2B2D30; color: #E6E8EA; border: 1px solid #43454A; border-radius: 8px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #3574F0; border: none; color: white; }")
                    btn_box.addWidget(b)
                quick_layout.addLayout(btn_box)
                quick_layout.addStretch()
                mid_layout.addWidget(card_quick, stretch=2)

                card_punch = QtWidgets.QWidget()
                card_punch.setStyleSheet(
                    "QWidget { background-color: #1E1F22; border: 1px solid #393B40; border-radius: 12px; }")
                punch_layout = QtWidgets.QVBoxLayout(card_punch)
                punch_layout.setContentsMargins(30, 30, 30, 30)
                lbl_punch = QtWidgets.QLabel("✅ 考勤打卡")
                lbl_punch.setStyleSheet("color: #E6E8EA; font-size: 18px; font-weight: bold; border: none;")
                punch_layout.addWidget(lbl_punch, alignment=QtCore.Qt.AlignHCenter)
                self.btn_check_in = QtWidgets.QPushButton("点击签到")
                self.btn_check_in.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_check_in.setFixedSize(140, 140)
                self.btn_check_in.setStyleSheet(
                    "QPushButton { background-color: #3574F0; color: white; border-radius: 70px; font-size: 22px; font-weight: bold; border: 8px solid rgba(53, 116, 240, 0.3); } QPushButton:hover { background-color: #4682F2; } QPushButton:disabled { background-color: #10B981; border: 8px solid rgba(16, 185, 129, 0.3); color: white; font-size: 20px; }")
                self.lbl_check_in_msg = QtWidgets.QLabel("等待获取今日状态...")
                self.lbl_check_in_msg.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_check_in_msg.setStyleSheet("color: #9CA3AF; font-size: 15px; border: none; margin-top: 15px;")
                punch_layout.addStretch()
                punch_layout.addWidget(self.btn_check_in, alignment=QtCore.Qt.AlignHCenter)
                punch_layout.addWidget(self.lbl_check_in_msg)
                punch_layout.addStretch()
                mid_layout.addWidget(card_punch, stretch=1)

                home_layout.addLayout(mid_layout, stretch=3)
                layout.addLayout(home_layout)

            # 📊 历史记录
            elif name == "历史记录":
                filter_layout = QtWidgets.QHBoxLayout()
                self.label_filter_date = QtWidgets.QLabel("📅 日期:")
                self.label_filter_date.setStyleSheet("color: #9CA3AF; font-size: 15px; font-weight: bold;")
                self.date_edit_history = QtWidgets.QDateEdit()
                self.date_edit_history.setCalendarPopup(True)
                self.date_edit_history.setDate(QtCore.QDate.currentDate())
                self.label_filter_event = QtWidgets.QLabel("🗂️ 来源:")
                self.label_filter_event.setStyleSheet(
                    "color: #9CA3AF; font-size: 15px; font-weight: bold; margin-left: 15px;")
                self.combo_event_type = QtWidgets.QComboBox()
                self.combo_event_type.addItems(["全部来源", "实时监控", "视频识别", "图片识别"])
                self.btn_search_history = QtWidgets.QPushButton("🔍 筛选")
                self.btn_search_history.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_search_history.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 15px;} QPushButton:hover { background-color: #005B94; }")
                self.btn_reset_history = QtWidgets.QPushButton("🔄 显示全部")
                self.btn_reset_history.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_reset_history.setStyleSheet(
                    "QPushButton { background-color: #333537; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 10px; } QPushButton:hover { background-color: #444746; }")

                filter_layout.addWidget(self.label_filter_date)
                filter_layout.addWidget(self.date_edit_history)
                filter_layout.addWidget(self.label_filter_event)
                filter_layout.addWidget(self.combo_event_type)
                filter_layout.addStretch()
                filter_layout.addWidget(self.btn_search_history)
                filter_layout.addWidget(self.btn_reset_history)
                layout.addLayout(filter_layout, stretch=0)

                self.table_history = QtWidgets.QTableWidget(page)
                self.table_history.setObjectName("table_history")
                self.table_history.setColumnCount(4)
                self.table_history.setHorizontalHeaderLabels(["报警时间", "事件类型", "置信度", "操作"])
                self.table_history.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_history.verticalHeader().setVisible(False)
                self.table_history.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_history.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                self.table_history.setShowGrid(False)
                layout.addWidget(self.table_history, stretch=1)

            # 🌟 🖼️ 图片检测
            elif name == "图片检测":
                control_layout = QtWidgets.QHBoxLayout()
                self.btn_upload_image = QtWidgets.QPushButton("📁 选择图片")
                self.btn_upload_image.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_upload_image.setFixedHeight(40)
                self.btn_upload_image.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: #FFFFFF; font-size: 16px; font-weight: bold; border-radius: 8px; padding: 0px 20px; } QPushButton:hover { background-color: #005B94; }")
                control_layout.addWidget(self.btn_upload_image, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addSpacing(30)

                self.label_conf_image = QtWidgets.QLabel("置信度: 0.60")
                self.label_conf_image.setStyleSheet("color: #9CA3AF; font-weight: bold; font-size: 15px;")
                self.slider_conf_image = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                self.slider_conf_image.setRange(1, 100)
                self.slider_conf_image.setValue(60)
                self.slider_conf_image.setFixedWidth(150)
                control_layout.addWidget(self.label_conf_image, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addWidget(self.slider_conf_image, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addStretch()

                self.label_time_image = QtWidgets.QLabel("⏱ 检测耗时: 0.00s")
                self.label_time_image.setProperty("class", "stat_badge")
                self.label_time_image.setStyleSheet(
                    "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;")
                self.label_time_image.setFixedHeight(36)

                self.label_targets_image = QtWidgets.QLabel("🎯 检测目标: 0 个")
                self.label_targets_image.setProperty("class", "stat_badge")
                self.label_targets_image.setStyleSheet(
                    "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;")
                self.label_targets_image.setFixedHeight(36)
                control_layout.addWidget(self.label_time_image, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addSpacing(10)
                control_layout.addWidget(self.label_targets_image, alignment=QtCore.Qt.AlignVCenter)
                layout.addLayout(control_layout, stretch=0)

                # 🌟 双屏布局
                screen_layout_img = QtWidgets.QHBoxLayout()
                screen_layout_img.setSpacing(20)

                self.label_image_original = QtWidgets.QLabel("原始图片\n等待上传...")
                self.label_image_original.setAlignment(QtCore.Qt.AlignCenter)
                self.label_image_original.setStyleSheet(screen_style)
                self.label_image_original.setScaledContents(True)

                self.label_image_display = QtWidgets.QLabel("YOLO 检测结果\n等待上传...")
                self.label_image_display.setAlignment(QtCore.Qt.AlignCenter)
                self.label_image_display.setStyleSheet(screen_style)
                self.label_image_display.setScaledContents(True)

                screen_layout_img.addWidget(self.label_image_original, stretch=1)
                screen_layout_img.addWidget(self.label_image_display, stretch=1)
                layout.addLayout(screen_layout_img, stretch=7)

                self.table_image_results = QtWidgets.QTableWidget(page)
                self.table_image_results.setObjectName("table_image_results")
                self.table_image_results.setColumnCount(4)
                self.table_image_results.setHorizontalHeaderLabels(["序号", "类别", "置信度", "坐标位置 (x, y)"])
                self.table_image_results.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_image_results.verticalHeader().setVisible(False)
                self.table_image_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_image_results.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                self.table_image_results.setShowGrid(False)
                layout.addWidget(self.table_image_results, stretch=3)

            # 🌟 🎥 视频检测
            elif name == "视频检测":
                control_layout = QtWidgets.QHBoxLayout()
                self.btn_upload_video = QtWidgets.QPushButton("🎦 选择视频")
                self.btn_upload_video.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_upload_video.setFixedHeight(40)
                self.btn_upload_video.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: #FFFFFF; font-size: 16px; font-weight: bold; border-radius: 8px; padding: 0px 20px; } QPushButton:hover { background-color: #005B94; }")
                control_layout.addWidget(self.btn_upload_video, alignment=QtCore.Qt.AlignVCenter)

                self.btn_stop_video = QtWidgets.QPushButton("⏹️ 停止检测")
                self.btn_stop_video.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_stop_video.setFixedHeight(40)
                self.btn_stop_video.setStyleSheet(
                    "QPushButton { background-color: #7F1D1D; color: #FFFFFF; font-size: 16px; font-weight: bold; border-radius: 8px; padding: 0px 20px; margin-left: 10px; } QPushButton:hover { background-color: #991B1B; }")
                control_layout.addWidget(self.btn_stop_video, alignment=QtCore.Qt.AlignVCenter)

                control_layout.addSpacing(30)
                self.label_conf_video = QtWidgets.QLabel("置信度: 0.60")
                self.label_conf_video.setStyleSheet("color: #9CA3AF; font-weight: bold; font-size: 15px;")
                self.slider_conf_video = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                self.slider_conf_video.setRange(1, 100)
                self.slider_conf_video.setValue(60)
                self.slider_conf_video.setFixedWidth(150)
                control_layout.addWidget(self.label_conf_video, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addWidget(self.slider_conf_video, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addStretch()

                self.label_fps_video = QtWidgets.QLabel("⚡ FPS: 0")
                self.label_fps_video.setProperty("class", "stat_badge")
                self.label_fps_video.setStyleSheet(
                    "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;")
                self.label_fps_video.setFixedHeight(36)

                self.label_targets_video = QtWidgets.QLabel("🎯 画面目标: 0 个")
                self.label_targets_video.setProperty("class", "stat_badge")
                self.label_targets_video.setStyleSheet(
                    "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;")
                self.label_targets_video.setFixedHeight(36)
                control_layout.addWidget(self.label_fps_video, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addSpacing(10)
                control_layout.addWidget(self.label_targets_video, alignment=QtCore.Qt.AlignVCenter)
                layout.addLayout(control_layout, stretch=0)

                # 🌟 双屏布局
                screen_layout_vid = QtWidgets.QHBoxLayout()
                screen_layout_vid.setSpacing(20)

                self.label_video_original = QtWidgets.QLabel("原始视频源\n等待导入...")
                self.label_video_original.setAlignment(QtCore.Qt.AlignCenter)
                self.label_video_original.setStyleSheet(screen_style)
                self.label_video_original.setScaledContents(True)

                self.label_video_display = QtWidgets.QLabel("YOLO 检测结果\n等待导入...")
                self.label_video_display.setAlignment(QtCore.Qt.AlignCenter)
                self.label_video_display.setStyleSheet(screen_style)
                self.label_video_display.setScaledContents(True)

                screen_layout_vid.addWidget(self.label_video_original, stretch=1)
                screen_layout_vid.addWidget(self.label_video_display, stretch=1)
                layout.addLayout(screen_layout_vid, stretch=7)

                self.table_video_results = QtWidgets.QTableWidget(page)
                self.table_video_results.setObjectName("table_video_results")
                self.table_video_results.setColumnCount(4)
                self.table_video_results.setHorizontalHeaderLabels(["报警时间", "事件类型", "置信度", "操作"])
                self.table_video_results.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_video_results.verticalHeader().setVisible(False)
                self.table_video_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_video_results.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                self.table_video_results.setShowGrid(False)
                layout.addWidget(self.table_video_results, stretch=3)

            # 🚨 实时监控
            elif name == "实时监控":
                control_layout = QtWidgets.QHBoxLayout()
                self.btn_start_cams = QtWidgets.QPushButton("▶️ 启动投射监控")
                self.btn_start_cams.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_start_cams.setFixedHeight(40)
                self.btn_start_cams.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: #FFFFFF; font-size: 16px; font-weight: bold; border-radius: 8px; padding: 0px 20px; } QPushButton:hover { background-color: #005B94; }")
                control_layout.addWidget(self.btn_start_cams, alignment=QtCore.Qt.AlignVCenter)

                self.btn_stop_cams = QtWidgets.QPushButton("⏹️ 停止监控")
                self.btn_stop_cams.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_stop_cams.setFixedHeight(40)
                self.btn_stop_cams.setStyleSheet(
                    "QPushButton { background-color: #7F1D1D; color: #FFFFFF; font-size: 16px; font-weight: bold; border-radius: 8px; padding: 0px 20px; margin-left: 10px; } QPushButton:hover { background-color: #991B1B; }")
                control_layout.addWidget(self.btn_stop_cams, alignment=QtCore.Qt.AlignVCenter)

                control_layout.addSpacing(30)
                self.label_conf_rt = QtWidgets.QLabel("全局置信度: 0.60")
                self.label_conf_rt.setStyleSheet("color: #9CA3AF; font-weight: bold; font-size: 15px;")
                self.slider_conf_rt = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                self.slider_conf_rt.setRange(1, 100)
                self.slider_conf_rt.setValue(60)
                self.slider_conf_rt.setFixedWidth(150)
                control_layout.addWidget(self.label_conf_rt, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addWidget(self.slider_conf_rt, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addStretch()

                self.label_fps_cam1 = QtWidgets.QLabel("CH1 ⚡ FPS: 0")
                self.label_fps_cam1.setProperty("class", "stat_badge")
                self.label_fps_cam1.setStyleSheet(
                    "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;")
                self.label_fps_cam1.setFixedHeight(36)
                self.label_fps_cam2 = QtWidgets.QLabel("CH2 ⚡ FPS: 0")
                self.label_fps_cam2.setProperty("class", "stat_badge")
                self.label_fps_cam2.setStyleSheet(
                    "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;")
                self.label_fps_cam2.setFixedHeight(36)
                control_layout.addWidget(self.label_fps_cam1, alignment=QtCore.Qt.AlignVCenter)
                control_layout.addSpacing(5)
                control_layout.addWidget(self.label_fps_cam2, alignment=QtCore.Qt.AlignVCenter)
                layout.addLayout(control_layout, stretch=0)

                library_layout = QtWidgets.QHBoxLayout()
                library_layout.setSpacing(20)
                channel_panel = QtWidgets.QWidget()
                channel_panel.setStyleSheet(
                    "QWidget { background-color: #1A1B1D; border: 1px solid #333537; border-radius: 10px; }")
                channel_panel_layout = QtWidgets.QVBoxLayout(channel_panel)
                channel_panel_layout.setContentsMargins(15, 15, 15, 15)
                lbl_lib_title = QtWidgets.QLabel("📚 监控通道库")
                lbl_lib_title.setStyleSheet("color:#E3E3E3;font-size:16px;font-weight:bold;border:none;")
                channel_panel_layout.addWidget(lbl_lib_title)
                self.list_channel_library = QtWidgets.QListWidget()
                self.list_channel_library.setMinimumHeight(110)
                self.list_channel_library.setStyleSheet(
                    "QListWidget { background-color:#131314; border:1px solid #333537; border-radius:8px; color:#E3E3E3; padding:6px; }"
                    "QListWidget::item { padding:6px; } QListWidget::item:selected { background-color:#004A77; color:#FFFFFF; border-radius:4px; }")
                channel_panel_layout.addWidget(self.list_channel_library)
                lib_btn_layout = QtWidgets.QHBoxLayout()
                self.btn_add_rtsp = QtWidgets.QPushButton("➕ 添加 RTSP")
                self.btn_add_local_channel = QtWidgets.QPushButton("📁 添加本地视频")
                self.btn_remove_channel = QtWidgets.QPushButton("🗑️ 删除选中")
                for btn in [self.btn_add_rtsp, self.btn_add_local_channel, self.btn_remove_channel]:
                    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    btn.setStyleSheet(
                        "QPushButton { background-color: #2B2D30; color: #E3E3E3; border: 1px solid #43454A; border-radius: 6px; padding: 8px 12px; font-weight: bold; } QPushButton:hover { background-color: #3574F0; border: none; }")
                    lib_btn_layout.addWidget(btn)
                channel_panel_layout.addLayout(lib_btn_layout)
                library_layout.addWidget(channel_panel, stretch=3)

                projection_panel = QtWidgets.QWidget()
                projection_panel.setStyleSheet(
                    "QWidget { background-color: #1A1B1D; border: 1px solid #333537; border-radius: 10px; }")
                projection_layout = QtWidgets.QVBoxLayout(projection_panel)
                projection_layout.setContentsMargins(15, 15, 15, 15)
                lbl_projection_title = QtWidgets.QLabel("🎛️ 通道投射")
                lbl_projection_title.setStyleSheet("color:#E3E3E3;font-size:16px;font-weight:bold;border:none;")
                projection_layout.addWidget(lbl_projection_title)
                row_ch1 = QtWidgets.QHBoxLayout()
                row_ch1.addWidget(QtWidgets.QLabel("CH1 投射源:", styleSheet="color:#9CA3AF;border:none;"))
                self.combo_ch1_source = QtWidgets.QComboBox()
                row_ch1.addWidget(self.combo_ch1_source, stretch=1)
                projection_layout.addLayout(row_ch1)
                row_ch2 = QtWidgets.QHBoxLayout()
                row_ch2.addWidget(QtWidgets.QLabel("CH2 投射源:", styleSheet="color:#9CA3AF;border:none;"))
                self.combo_ch2_source = QtWidgets.QComboBox()
                row_ch2.addWidget(self.combo_ch2_source, stretch=1)
                projection_layout.addLayout(row_ch2)
                self.btn_apply_projection = QtWidgets.QPushButton("💾 保存投射配置")
                self.btn_apply_projection.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_apply_projection.setStyleSheet(
                    "QPushButton { background-color:#004A77; color:#FFFFFF; border-radius:6px; padding:8px 12px; font-weight:bold; margin-top:8px; } QPushButton:hover { background-color:#005B94; }")
                projection_layout.addWidget(self.btn_apply_projection)
                projection_layout.addStretch()
                library_layout.addWidget(projection_panel, stretch=2)
                layout.addLayout(library_layout, stretch=0)

                screen_layout = QtWidgets.QHBoxLayout()
                screen_layout.setSpacing(20)

                self.label_cam1_display = QtWidgets.QLabel("CH1: 监控通道一\n等待启动...")
                self.label_cam1_display.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cam1_display.setStyleSheet(screen_style)
                self.label_cam1_display.setScaledContents(True)

                self.label_cam2_display = QtWidgets.QLabel("CH2: 监控通道二\n等待启动...")
                self.label_cam2_display.setAlignment(QtCore.Qt.AlignCenter)
                self.label_cam2_display.setStyleSheet(screen_style)
                self.label_cam2_display.setScaledContents(True)

                screen_layout.addWidget(self.label_cam1_display, stretch=1)
                screen_layout.addWidget(self.label_cam2_display, stretch=1)
                layout.addLayout(screen_layout, stretch=7)

                self.table_rt_results = QtWidgets.QTableWidget(page)
                self.table_rt_results.setObjectName("table_rt_results")
                self.table_rt_results.setColumnCount(5)
                self.table_rt_results.setHorizontalHeaderLabels(["报警时间", "监控源", "事件类型", "置信度", "操作"])
                self.table_rt_results.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_rt_results.verticalHeader().setVisible(False)
                self.table_rt_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_rt_results.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                self.table_rt_results.setShowGrid(False)
                layout.addWidget(self.table_rt_results, stretch=3)

            # 📈 统计中心
            elif name == "统计中心":
                cards_layout = QtWidgets.QHBoxLayout()
                cards_layout.setSpacing(20)
                card_style = "QWidget { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; } QLabel { border: none; }"

                self.card_total = QtWidgets.QWidget()
                self.card_total.setStyleSheet(card_style)
                layout_c1 = QtWidgets.QVBoxLayout(self.card_total)
                layout_c1.setContentsMargins(20, 20, 20, 20)
                lbl_c1_title = QtWidgets.QLabel("🚨 累计违规警报")
                lbl_c1_title.setStyleSheet("color: #9CA3AF; font-size: 16px; font-weight: bold;")
                self.lbl_stat_total = QtWidgets.QLabel("0")
                self.lbl_stat_total.setStyleSheet("color: #EF4444; font-size: 38px; font-weight: 900;")
                layout_c1.addWidget(lbl_c1_title)
                layout_c1.addWidget(self.lbl_stat_total, alignment=QtCore.Qt.AlignHCenter)
                cards_layout.addWidget(self.card_total)

                self.card_today = QtWidgets.QWidget()
                self.card_today.setStyleSheet(card_style)
                layout_c2 = QtWidgets.QVBoxLayout(self.card_today)
                layout_c2.setContentsMargins(20, 20, 20, 20)
                lbl_c2_title = QtWidgets.QLabel("📅 今日新增警报")
                lbl_c2_title.setStyleSheet("color: #9CA3AF; font-size: 16px; font-weight: bold;")
                self.lbl_stat_today = QtWidgets.QLabel("0")
                self.lbl_stat_today.setStyleSheet("color: #F59E0B; font-size: 38px; font-weight: 900;")
                layout_c2.addWidget(lbl_c2_title)
                layout_c2.addWidget(self.lbl_stat_today, alignment=QtCore.Qt.AlignHCenter)
                cards_layout.addWidget(self.card_today)

                self.card_top_source = QtWidgets.QWidget()
                self.card_top_source.setStyleSheet(card_style)
                layout_c3 = QtWidgets.QVBoxLayout(self.card_top_source)
                layout_c3.setContentsMargins(20, 20, 20, 20)
                lbl_c3_title = QtWidgets.QLabel("🗂️ 最高频违规来源")
                lbl_c3_title.setStyleSheet("color: #9CA3AF; font-size: 16px; font-weight: bold;")
                self.lbl_stat_source = QtWidgets.QLabel("-")
                self.lbl_stat_source.setStyleSheet("color: #3B82F6; font-size: 28px; font-weight: 900;")
                layout_c3.addWidget(lbl_c3_title)
                layout_c3.addWidget(self.lbl_stat_source, alignment=QtCore.Qt.AlignHCenter)
                cards_layout.addWidget(self.card_top_source)
                layout.addLayout(cards_layout, stretch=1)

                charts_layout = QtWidgets.QHBoxLayout()
                charts_layout.setSpacing(20)
                self.container_pie_chart = QtWidgets.QWidget()
                self.container_pie_chart.setStyleSheet(card_style)
                self.layout_pie_chart = QtWidgets.QVBoxLayout(self.container_pie_chart)
                self.layout_pie_chart.setContentsMargins(10, 10, 10, 10)
                charts_layout.addWidget(self.container_pie_chart, stretch=1)

                self.container_bar_chart = QtWidgets.QWidget()
                self.container_bar_chart.setStyleSheet(card_style)
                self.layout_bar_chart = QtWidgets.QVBoxLayout(self.container_bar_chart)
                self.layout_bar_chart.setContentsMargins(10, 10, 10, 10)
                charts_layout.addWidget(self.container_bar_chart, stretch=2)
                layout.addLayout(charts_layout, stretch=3)

            # 👤 个人中心
            elif name == "个人中心":
                pc_layout = QtWidgets.QHBoxLayout()
                pc_layout.setSpacing(30)

                self.card_profile = QtWidgets.QWidget()
                self.card_profile.setStyleSheet(
                    "QWidget { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; }")
                profile_layout = QtWidgets.QVBoxLayout(self.card_profile)
                profile_layout.setContentsMargins(30, 40, 30, 40)

                lbl_avatar = QtWidgets.QLabel("👨‍💻")
                lbl_avatar.setAlignment(QtCore.Qt.AlignCenter)
                lbl_avatar.setStyleSheet(
                    "font-size: 80px; background-color: #2D2F31; border-radius: 60px; padding: 20px;")
                lbl_avatar.setFixedSize(120, 120)

                self.lbl_profile_name = QtWidgets.QLabel("当前用户: Dachui")
                self.lbl_profile_name.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_profile_name.setStyleSheet(
                    "color: #FFFFFF; font-size: 22px; font-weight: bold; margin-top: 15px;")

                self.lbl_profile_role = QtWidgets.QLabel("系统操作员")
                self.lbl_profile_role.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_profile_role.setStyleSheet(
                    "color: #F59E0B; font-size: 14px; font-weight: bold; background-color: rgba(245, 158, 11, 0.1); border-radius: 6px; padding: 5px;")

                info_style = "color: #9CA3AF; font-size: 14px; margin-top: 10px;"
                self.lbl_login_time = QtWidgets.QLabel("上次登录: 刚刚")
                self.lbl_login_time.setStyleSheet(info_style)
                self.lbl_login_ip = QtWidgets.QLabel("登录 IP: 127.0.0.1 (本地)")
                self.lbl_login_ip.setStyleSheet(info_style)

                profile_layout.addWidget(lbl_avatar, alignment=QtCore.Qt.AlignHCenter)
                profile_layout.addWidget(self.lbl_profile_name)
                profile_layout.addWidget(self.lbl_profile_role, alignment=QtCore.Qt.AlignHCenter)
                profile_layout.addSpacing(30)
                profile_layout.addWidget(self.lbl_login_time)
                profile_layout.addWidget(self.lbl_login_ip)
                profile_layout.addStretch()

                self.btn_logout = QtWidgets.QPushButton("🚪 退出当前账号")
                self.btn_logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_logout.setStyleSheet(
                    "QPushButton { background-color: transparent; border: 2px solid #7F1D1D; color: #EF4444; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 15px; } QPushButton:hover { background-color: #7F1D1D; color: #FFFFFF; }")
                profile_layout.addWidget(self.btn_logout)
                pc_layout.addWidget(self.card_profile, stretch=3)

                self.tab_widget = QtWidgets.QTabWidget()

                tab_workspace = QtWidgets.QWidget()
                ws_layout = QtWidgets.QVBoxLayout(tab_workspace)
                ws_layout.setContentsMargins(30, 30, 30, 30)
                ws_layout.setSpacing(20)

                self.lbl_checkin_status = QtWidgets.QLabel("✅ 今日已签到 (08:25)")
                self.lbl_checkin_status.setStyleSheet(
                    "color: #10B981; font-size: 18px; font-weight: bold; background-color: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 8px;")
                self.lbl_attendance_days = QtWidgets.QLabel("🏆 本月已全勤打卡 21 天，继续保持！")
                self.lbl_attendance_days.setStyleSheet("color: #E3E3E3; font-size: 16px; margin-top: 10px;")
                self.lbl_personal_intercept = QtWidgets.QLabel("🛡️ 累计处理违规: 128 起")
                self.lbl_personal_intercept.setStyleSheet("color: #66B2FF; font-size: 16px; margin-top: 10px;")

                ws_layout.addWidget(self.lbl_checkin_status)
                ws_layout.addWidget(self.lbl_attendance_days)
                ws_layout.addWidget(self.lbl_personal_intercept)
                ws_layout.addStretch()

                tab_security = QtWidgets.QWidget()
                sec_layout = QtWidgets.QVBoxLayout(tab_security)
                sec_layout.setContentsMargins(30, 30, 30, 30)
                sec_layout.setSpacing(20)

                lbl_sec_title = QtWidgets.QLabel("🔐 修改登录密码")
                lbl_sec_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")

                form_layout = QtWidgets.QFormLayout()
                form_layout.setSpacing(15)
                self.input_old_pwd = QtWidgets.QLineEdit()
                self.input_old_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
                self.input_old_pwd.setPlaceholderText("请输入原密码")
                self.input_new_pwd = QtWidgets.QLineEdit()
                self.input_new_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
                self.input_new_pwd.setPlaceholderText("请输入新密码")

                lbl_old = QtWidgets.QLabel("原密码:")
                lbl_old.setStyleSheet("color: #9CA3AF; font-size: 15px;")
                lbl_new = QtWidgets.QLabel("新密码:")
                lbl_new.setStyleSheet("color: #9CA3AF; font-size: 15px;")

                form_layout.addRow(lbl_old, self.input_old_pwd)
                form_layout.addRow(lbl_new, self.input_new_pwd)

                self.btn_save_pwd = QtWidgets.QPushButton("💾 更新安全密码")
                self.btn_save_pwd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_save_pwd.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 16px; margin-top: 5px;} QPushButton:hover { background-color: #005B94; }")

                sec_layout.addWidget(lbl_sec_title)
                sec_layout.addLayout(form_layout)
                sec_layout.addWidget(self.btn_save_pwd)

                line = QtWidgets.QFrame()
                line.setFrameShape(QtWidgets.QFrame.HLine)
                line.setFrameShadow(QtWidgets.QFrame.Sunken)
                line.setStyleSheet("background-color: #333537; margin-top: 15px; margin-bottom: 15px;")
                sec_layout.addWidget(line)

                lbl_email_title = QtWidgets.QLabel("📧 修改绑定邮箱")
                lbl_email_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")

                email_layout = QtWidgets.QFormLayout()
                email_layout.setSpacing(15)
                self.input_new_email = QtWidgets.QLineEdit()
                self.input_new_email.setPlaceholderText("请输入新的邮箱地址")

                lbl_email = QtWidgets.QLabel("新邮箱:")
                lbl_email.setStyleSheet("color: #9CA3AF; font-size: 15px;")
                email_layout.addRow(lbl_email, self.input_new_email)

                self.btn_save_email = QtWidgets.QPushButton("✉️ 更新绑定邮箱")
                self.btn_save_email.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_save_email.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 16px; margin-top: 5px;} QPushButton:hover { background-color: #005B94; }")

                sec_layout.addWidget(lbl_email_title)
                sec_layout.addLayout(email_layout)
                sec_layout.addWidget(self.btn_save_email)
                sec_layout.addStretch()

                self.tab_widget.addTab(tab_workspace, "📈 我的工作台")
                self.tab_widget.addTab(tab_security, "🔐 安全中心")

                pc_layout.addWidget(self.tab_widget, stretch=7)
                layout.addLayout(pc_layout)

            # ⚙️ 系统设置
            elif name == "系统设置":
                grid_layout = QtWidgets.QGridLayout()
                grid_layout.setSpacing(25)

                card_style = "QWidget { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; } QLabel { border: none; }"
                title_style = "color: #FFFFFF; font-size: 18px; font-weight: bold; margin-bottom: 10px;"
                label_style = "color: #9CA3AF; font-size: 15px;"

                card_ai = QtWidgets.QWidget()
                card_ai.setStyleSheet(card_style)
                lay_ai = QtWidgets.QVBoxLayout(card_ai)
                lay_ai.setContentsMargins(25, 25, 25, 25)
                lay_ai.setSpacing(15)
                lay_ai.addWidget(QtWidgets.QLabel("🧠 AI 算法引擎设置", styleSheet=title_style))
                lay_ai.addWidget(QtWidgets.QLabel("当前推理权重模型:", styleSheet=label_style))
                self.combo_model = QtWidgets.QComboBox()
                self.combo_model.addItems(["best.pt (默认最优)", "yolov8n.pt (轻量极速)", "yolov12_custom.pt"])
                lay_ai.addWidget(self.combo_model)
                lay_ai.addWidget(QtWidgets.QLabel("计算硬件设备 (需重启生效):", styleSheet=label_style))
                self.combo_device = QtWidgets.QComboBox()
                self.combo_device.addItems(["自动检测最优硬件 (Auto)", "GPU (CUDA)", "CPU"])
                lay_ai.addWidget(self.combo_device)
                lay_ai.addWidget(QtWidgets.QLabel("系统默认预警置信度:", styleSheet=label_style))
                conf_layout = QtWidgets.QHBoxLayout()
                self.slider_default_conf = QtWidgets.QSlider(QtCore.Qt.Horizontal)
                self.slider_default_conf.setRange(1, 100)
                self.slider_default_conf.setValue(60)
                self.lbl_default_conf_val = QtWidgets.QLabel("0.60")
                self.lbl_default_conf_val.setStyleSheet("color: #66B2FF; font-weight: bold; font-size: 16px;")
                conf_layout.addWidget(self.slider_default_conf)
                conf_layout.addWidget(self.lbl_default_conf_val)
                lay_ai.addLayout(conf_layout)
                lay_ai.addStretch()

                card_storage = QtWidgets.QWidget()
                card_storage.setStyleSheet(card_style)
                lay_storage = QtWidgets.QVBoxLayout(card_storage)
                lay_storage.setContentsMargins(25, 25, 25, 25)
                lay_storage.setSpacing(15)
                lay_storage.addWidget(QtWidgets.QLabel("💾 存储与资源管理", styleSheet=title_style))
                lay_storage.addWidget(QtWidgets.QLabel("违规抓拍图片存储路径:", styleSheet=label_style))
                path_layout = QtWidgets.QHBoxLayout()
                self.input_capture_path = QtWidgets.QLineEdit()
                self.input_capture_path.setReadOnly(True)
                self.btn_browse_path = QtWidgets.QPushButton("📂 浏览")
                self.btn_browse_path.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_browse_path.setStyleSheet(
                    "QPushButton { background-color: #333537; color: white; border-radius: 4px; padding: 8px 15px; font-weight:bold; } QPushButton:hover { background-color: #444746; }")
                path_layout.addWidget(self.input_capture_path)
                path_layout.addWidget(self.btn_browse_path)
                lay_storage.addLayout(path_layout)
                lay_storage.addWidget(QtWidgets.QLabel("系统日志与抓拍自动清理策略:", styleSheet=label_style))
                self.combo_cleanup = QtWidgets.QComboBox()
                self.combo_cleanup.addItems(
                    ["永久保留 (需手动清理)", "自动清理 30 天前的数据", "自动清理 7 天前的数据"])
                lay_storage.addWidget(self.combo_cleanup)
                lay_storage.addStretch()

                card_alert = QtWidgets.QWidget()
                card_alert.setStyleSheet(card_style)
                lay_alert = QtWidgets.QVBoxLayout(card_alert)
                lay_alert.setContentsMargins(25, 25, 25, 25)
                lay_alert.setSpacing(15)
                lay_alert.addWidget(QtWidgets.QLabel("🚨 警报与通知控制", styleSheet=title_style))
                self.check_sound_alert = QtWidgets.QCheckBox(" 开启系统侦测声音警报 (Beep)")
                self.check_sound_alert.setChecked(True)
                lay_alert.addWidget(self.check_sound_alert)
                lay_alert.addWidget(QtWidgets.QLabel("同目标重复报警冷却时间 (防止弹窗刷屏):", styleSheet=label_style))
                cd_layout = QtWidgets.QHBoxLayout()
                self.spin_cooldown = QtWidgets.QSpinBox()
                self.spin_cooldown.setRange(1, 60)
                self.spin_cooldown.setValue(5)
                self.spin_cooldown.setSuffix(" 秒")
                self.spin_cooldown.setFixedWidth(120)
                cd_layout.addWidget(self.spin_cooldown)
                cd_layout.addStretch()
                lay_alert.addLayout(cd_layout)
                lay_alert.addStretch()

                card_ui = QtWidgets.QWidget()
                card_ui.setStyleSheet(card_style)
                lay_ui = QtWidgets.QVBoxLayout(card_ui)
                lay_ui.setContentsMargins(25, 25, 25, 25)
                lay_ui.setSpacing(15)
                lay_ui.addWidget(QtWidgets.QLabel("💻 系统 UI 与交互", styleSheet=title_style))
                lay_ui.addWidget(QtWidgets.QLabel("客户端主题风格 (开发中):", styleSheet=label_style))
                self.combo_theme = QtWidgets.QComboBox()
                self.combo_theme.addItems(["深空暗黑 (Dark Theme)", "工业亮白 (Light Theme)"])
                lay_ui.addWidget(self.combo_theme)
                lay_ui.addStretch()

                grid_layout.addWidget(card_ai, 0, 0)
                grid_layout.addWidget(card_storage, 0, 1)
                grid_layout.addWidget(card_alert, 1, 0)
                grid_layout.addWidget(card_ui, 1, 1)

                layout.addLayout(grid_layout, stretch=1)

                btn_layout = QtWidgets.QHBoxLayout()
                self.btn_save_system = QtWidgets.QPushButton("💾 立即应用并保存全局系统设置")
                self.btn_save_system.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_save_system.setFixedSize(350, 50)
                self.btn_save_system.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 8px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #005B94; }")
                btn_layout.addStretch()
                btn_layout.addWidget(self.btn_save_system)
                btn_layout.addStretch()
                layout.addLayout(btn_layout)

            # 🤖 AI 客服
            elif name == "AI 助手":
                chat_layout = QtWidgets.QVBoxLayout()
                chat_layout.setSpacing(20)

                self.chat_display = QtWidgets.QTextBrowser()
                self.chat_display.setStyleSheet(
                    "QTextBrowser { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; padding: 25px; font-size: 16px; color: #E3E3E3; }")
                self.chat_display.setOpenExternalLinks(True)
                chat_layout.addWidget(self.chat_display, stretch=8)

                input_layout = QtWidgets.QHBoxLayout()
                input_layout.setSpacing(15)

                self.input_chat = QtWidgets.QLineEdit()
                self.input_chat.setPlaceholderText("请输入您的问题，按回车键发送...")
                self.input_chat.setStyleSheet(
                    "QLineEdit { background-color: #131314; border: 1px solid #333537; border-radius: 25px; padding: 10px 25px; font-size: 16px; color: #E3E3E3; } QLineEdit:focus { border: 1px solid #66B2FF; }")
                self.input_chat.setFixedHeight(50)

                self.btn_send_chat = QtWidgets.QPushButton("发送 🚀")
                self.btn_send_chat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_send_chat.setFixedSize(100, 50)
                self.btn_send_chat.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 25px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #005B94; }")

                input_layout.addWidget(self.input_chat)
                input_layout.addWidget(self.btn_send_chat)
                chat_layout.addLayout(input_layout, stretch=1)
                layout.addLayout(chat_layout)

            else:
                desc_label = QtWidgets.QLabel(f"这里是【{name}】的专属功能区，未来将在这里部署相关组件。")
                desc_label.setStyleSheet("color: #64748B; font-size: 16px;")
                layout.addWidget(desc_label)
                layout.addStretch()

            self.stackedWidget.addWidget(page)
            self.pages.append(page)

        self.horizontalLayout_main.addWidget(self.stackedWidget)
        self.horizontalLayout_main.setStretch(0, 1)
        self.horizontalLayout_main.setStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
