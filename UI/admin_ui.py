# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdminWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 750))
        MainWindow.setWindowTitle("智慧工地安全管控系统 - 管理员大厅")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 🌟 核心升级：更换为顶级现代 Web 字体栈，全局字号加大，抗锯齿拉满
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
        """)

        self.horizontalLayout_main = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_main.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_main.setSpacing(0)

        self.left_sidebar = QtWidgets.QWidget(self.centralwidget)
        self.left_sidebar.setObjectName("left_sidebar")
        self.verticalLayout_nav = QtWidgets.QVBoxLayout(self.left_sidebar)
        self.verticalLayout_nav.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_nav.setSpacing(6)

        self.label_main_title = QtWidgets.QLabel("管理员大厅")
        self.label_main_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_main_title.setObjectName("label_main_title")
        self.verticalLayout_nav.addWidget(self.label_main_title)

        self.label_sub_title = QtWidgets.QLabel("SUPER ADMIN")
        self.label_sub_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sub_title.setObjectName("label_sub_title")
        self.verticalLayout_nav.addWidget(self.label_sub_title)

        self.nav_buttons = []
        btn_names = ["系统首页", "历史记录", "统计中心", "员工管理", "考勤中心", "个人中心", "AI 助手"]
        for i, name in enumerate(btn_names):
            btn = QtWidgets.QPushButton(name)
            btn.setProperty("class", "nav_btn")
            btn.setCheckable(True)
            btn.setFixedSize(210, 48)
            if i == 0: btn.setChecked(True)
            self.verticalLayout_nav.addWidget(btn, 0, QtCore.Qt.AlignHCenter)
            self.nav_buttons.append(btn)

        spacerItem_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                  QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_nav.addItem(spacerItem_bottom)

        self.btn_admin_logout = QtWidgets.QPushButton("退出管理端")
        self.btn_admin_logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_admin_logout.setFixedSize(180, 45)
        self.btn_admin_logout.setStyleSheet(
            "QPushButton { background-color: transparent; border: 2px solid #7F1D1D; color: #EF4444; border-radius: 6px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #7F1D1D; color: #FFFFFF; }")
        self.verticalLayout_nav.addWidget(self.btn_admin_logout, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_nav.addSpacing(30)

        self.horizontalLayout_main.addWidget(self.left_sidebar)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.pages = []
        for i, name in enumerate(btn_names):
            page = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(page)
            layout.setContentsMargins(50, 50, 50, 50)
            layout.setSpacing(20)

            title_label = QtWidgets.QLabel(name)
            title_label.setProperty("class", "page_title")
            layout.addWidget(title_label)

            card_style = "QWidget { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; }"

            # 房间 0：系统首页
            if i == 0:
                card_welcome = QtWidgets.QWidget()
                card_welcome.setStyleSheet(card_style)
                wel_layout = QtWidgets.QHBoxLayout(card_welcome)
                wel_layout.setContentsMargins(40, 40, 40, 40)

                wel_text = QtWidgets.QVBoxLayout()
                self.lbl_admin_welcome = QtWidgets.QLabel("早上好，admin")
                self.lbl_admin_welcome.setStyleSheet(
                    "color: #FFFFFF; font-size: 36px; font-weight: bold; border: none;")
                self.lbl_admin_sub = QtWidgets.QLabel("上帝视角已开启，全局数据一切尽在掌握。")
                self.lbl_admin_sub.setStyleSheet(
                    "color: #9CA3AF; font-size: 16px; border: none; margin-top: 10px; margin-bottom: 15px;")

                wel_text.addWidget(self.lbl_admin_welcome)
                wel_text.addWidget(self.lbl_admin_sub)

                info_bar_layout = QtWidgets.QHBoxLayout()
                info_bar_layout.setSpacing(12)
                badge_style = "background-color: #2D2F31; color: #66B2FF; padding: 8px 15px; border-radius: 6px; font-size: 15px; font-weight: bold; border: 1px solid #333537;"
                self.lbl_home_user = QtWidgets.QLabel("👤 当前用户: admin")
                self.lbl_home_user.setStyleSheet(badge_style)
                self.lbl_home_role = QtWidgets.QLabel("👑 角色: 超级管理员")
                self.lbl_home_role.setStyleSheet(badge_style)

                info_bar_layout.addWidget(self.lbl_home_user)
                info_bar_layout.addWidget(self.lbl_home_role)
                info_bar_layout.addStretch()

                wel_text.addLayout(info_bar_layout)

                self.lbl_realtime_clock = QtWidgets.QLabel("00:00:00")
                self.lbl_realtime_clock.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.lbl_realtime_clock.setStyleSheet(
                    "color: #66B2FF; font-size: 58px; font-weight: 900; font-family: 'Arial'; border: none; letter-spacing: 2px;")

                wel_layout.addLayout(wel_text)
                wel_layout.addStretch()
                wel_layout.addWidget(self.lbl_realtime_clock)

                layout.addWidget(card_welcome, stretch=2)

                dash_layout = QtWidgets.QHBoxLayout()
                dash_layout.setSpacing(20)

                card_users = QtWidgets.QWidget()
                card_users.setStyleSheet(card_style)
                lay_u = QtWidgets.QVBoxLayout(card_users)
                lay_u.addWidget(QtWidgets.QLabel("注册操作员总数",styleSheet="color: #9CA3AF; font-size: 16px; border: none; font-weight: bold;"))
                self.lbl_total_users = QtWidgets.QLabel("0")
                self.lbl_total_users.setStyleSheet("color: #66B2FF; font-size: 42px; font-weight: 900; border: none;")
                lay_u.addWidget(self.lbl_total_users, alignment=QtCore.Qt.AlignCenter)
                dash_layout.addWidget(card_users)

                card_alerts = QtWidgets.QWidget()
                card_alerts.setStyleSheet(card_style)
                lay_a = QtWidgets.QVBoxLayout(card_alerts)
                lay_a.addWidget(QtWidgets.QLabel("历史违规抓拍总数",styleSheet="color: #9CA3AF; font-size: 16px; border: none; font-weight: bold;"))
                self.lbl_total_alerts = QtWidgets.QLabel("0")
                self.lbl_total_alerts.setStyleSheet("color: #EF4444; font-size: 42px; font-weight: 900; border: none;")
                lay_a.addWidget(self.lbl_total_alerts, alignment=QtCore.Qt.AlignCenter)
                dash_layout.addWidget(card_alerts)

                card_att = QtWidgets.QWidget()
                card_att.setStyleSheet(card_style)
                lay_at = QtWidgets.QVBoxLayout(card_att)
                lay_at.addWidget(QtWidgets.QLabel("今日全站签到人数",styleSheet="color: #9CA3AF; font-size: 16px; border: none; font-weight: bold;"))
                self.lbl_today_att = QtWidgets.QLabel("0")
                self.lbl_today_att.setStyleSheet("color: #10B981; font-size: 42px; font-weight: 900; border: none;")
                lay_at.addWidget(self.lbl_today_att, alignment=QtCore.Qt.AlignCenter)
                dash_layout.addWidget(card_att)

                layout.addLayout(dash_layout, stretch=2)
                layout.addStretch(1)

            # 房间 1：历史记录
            elif i == 1:
                filter_layout = QtWidgets.QHBoxLayout()

                self.label_filter_date = QtWidgets.QLabel("日期:")
                self.label_filter_date.setStyleSheet("color: #9CA3AF; font-size: 15px; font-weight: bold;")
                self.date_edit_global = QtWidgets.QDateEdit()
                self.date_edit_global.setCalendarPopup(True)
                self.date_edit_global.setDate(QtCore.QDate.currentDate())

                self.label_filter_operator = QtWidgets.QLabel("搜索经手人:")
                self.label_filter_operator.setStyleSheet(
                    "color: #9CA3AF; font-size: 15px; font-weight: bold; margin-left: 15px;")

                self.input_global_operator = QtWidgets.QLineEdit()
                self.input_global_operator.setPlaceholderText("搜索账号...")
                self.input_global_operator.setFixedWidth(200)

                self.btn_search_global = QtWidgets.QPushButton("筛选")
                self.btn_search_global.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_search_global.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 15px; min-height: 28px;} QPushButton:hover { background-color: #005B94; }")

                self.btn_reset_global = QtWidgets.QPushButton("显示全部")
                self.btn_reset_global.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_reset_global.setStyleSheet(
                    "QPushButton { background-color: #333537; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 10px; min-height: 28px;} QPushButton:hover { background-color: #444746; }")

                filter_layout.addWidget(self.label_filter_date)
                filter_layout.addWidget(self.date_edit_global)
                filter_layout.addWidget(self.label_filter_operator)
                filter_layout.addWidget(self.input_global_operator)
                filter_layout.addStretch()
                filter_layout.addWidget(self.btn_search_global)
                filter_layout.addWidget(self.btn_reset_global)

                layout.addLayout(filter_layout, stretch=0)

                self.table_all_records = QtWidgets.QTableWidget()
                self.table_all_records.setColumnCount(5)
                self.table_all_records.setHorizontalHeaderLabels(
                    ["报警时间", "经手操作员", "事件类型", "置信度", "操作抓拍"])
                self.table_all_records.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_all_records.verticalHeader().setVisible(False)
                self.table_all_records.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_all_records.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                layout.addWidget(self.table_all_records, stretch=1)

            # 房间 2：统计中心
            elif i == 2:
                charts_layout = QtWidgets.QHBoxLayout()
                charts_layout.setSpacing(20)

                self.container_global_pie = QtWidgets.QWidget()
                self.container_global_pie.setStyleSheet(card_style)
                self.layout_global_pie = QtWidgets.QVBoxLayout(self.container_global_pie)
                self.layout_global_pie.setContentsMargins(10, 10, 10, 10)
                charts_layout.addWidget(self.container_global_pie, stretch=1)

                self.container_global_bar = QtWidgets.QWidget()
                self.container_global_bar.setStyleSheet(card_style)
                self.layout_global_bar = QtWidgets.QVBoxLayout(self.container_global_bar)
                self.layout_global_bar.setContentsMargins(10, 10, 10, 10)
                charts_layout.addWidget(self.container_global_bar, stretch=2)

                layout.addLayout(charts_layout, stretch=1)

            # 房间 3：员工管理
            elif i == 3:
                toolbar_layout = QtWidgets.QHBoxLayout()

                self.input_search_user = QtWidgets.QLineEdit()
                self.input_search_user.setPlaceholderText("🔍 输入用户 ID 或账号查询...")
                self.input_search_user.setFixedWidth(280)

                self.btn_search_user = QtWidgets.QPushButton("精准查询")
                self.btn_search_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_search_user.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 10px; min-height: 28px;} QPushButton:hover { background-color: #005B94; }")

                self.btn_reset_user = QtWidgets.QPushButton("显示全部")
                self.btn_reset_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_reset_user.setStyleSheet(
                    "QPushButton { background-color: #333537; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 10px; min-height: 28px;} QPushButton:hover { background-color: #444746; }")

                self.btn_add_user_dialog = QtWidgets.QPushButton("➕ 新增员工")
                self.btn_add_user_dialog.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_add_user_dialog.setFixedSize(130, 40)
                self.btn_add_user_dialog.setStyleSheet(
                    "QPushButton { background-color: #10B981; color: white; border-radius: 6px; font-weight: bold; font-size: 15px;} QPushButton:hover { background-color: #059669; }")

                toolbar_layout.addWidget(self.input_search_user)
                toolbar_layout.addWidget(self.btn_search_user)
                toolbar_layout.addWidget(self.btn_reset_user)
                toolbar_layout.addStretch()
                toolbar_layout.addWidget(self.btn_add_user_dialog)

                layout.addLayout(toolbar_layout)

                self.table_users = QtWidgets.QTableWidget()
                self.table_users.setColumnCount(5)
                self.table_users.setHorizontalHeaderLabels(
                    ["用户 ID", "系统账号", "身份角色", "绑定的密保邮箱", "操作"])
                self.table_users.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_users.verticalHeader().setVisible(False)
                self.table_users.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                layout.addWidget(self.table_users)

            # 房间 4：考勤中心
            elif i == 4:
                att_filter_layout = QtWidgets.QHBoxLayout()

                self.lbl_att_date = QtWidgets.QLabel("📅 查岗日期:")
                self.lbl_att_date.setStyleSheet("color: #9CA3AF; font-size: 15px; font-weight: bold;")
                self.date_edit_att = QtWidgets.QDateEdit()
                self.date_edit_att.setCalendarPopup(True)
                self.date_edit_att.setDate(QtCore.QDate.currentDate())

                self.btn_search_att = QtWidgets.QPushButton("🔍 生成考勤大屏")
                self.btn_search_att.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_search_att.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 15px; min-height: 28px;} QPushButton:hover { background-color: #005B94; }")

                att_filter_layout.addWidget(self.lbl_att_date)
                att_filter_layout.addWidget(self.date_edit_att)
                att_filter_layout.addWidget(self.btn_search_att)
                att_filter_layout.addStretch()
                layout.addLayout(att_filter_layout)

                att_charts_layout = QtWidgets.QHBoxLayout()
                att_charts_layout.setSpacing(20)

                self.container_att_pie = QtWidgets.QWidget()
                self.container_att_pie.setStyleSheet(card_style)
                self.layout_att_pie = QtWidgets.QVBoxLayout(self.container_att_pie)
                self.layout_att_pie.setContentsMargins(10, 10, 10, 10)
                att_charts_layout.addWidget(self.container_att_pie, stretch=1)

                self.container_att_bar = QtWidgets.QWidget()
                self.container_att_bar.setStyleSheet(card_style)
                self.layout_att_bar = QtWidgets.QVBoxLayout(self.container_att_bar)
                self.layout_att_bar.setContentsMargins(10, 10, 10, 10)
                att_charts_layout.addWidget(self.container_att_bar, stretch=2)

                layout.addLayout(att_charts_layout, stretch=1)

                self.table_attendance = QtWidgets.QTableWidget()
                self.table_attendance.setColumnCount(4)
                self.table_attendance.setHorizontalHeaderLabels(["系统账号", "身份角色", "打卡状态", "签到时间"])
                self.table_attendance.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                self.table_attendance.verticalHeader().setVisible(False)
                self.table_attendance.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                self.table_attendance.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                layout.addWidget(self.table_attendance, stretch=1)

            # 房间 5：个人中心
            elif i == 5:
                pc_layout = QtWidgets.QHBoxLayout()
                pc_layout.setSpacing(30)

                self.card_profile = QtWidgets.QWidget()
                self.card_profile.setStyleSheet(card_style)
                profile_layout = QtWidgets.QVBoxLayout(self.card_profile)
                profile_layout.setContentsMargins(30, 40, 30, 40)

                lbl_avatar = QtWidgets.QLabel("👨‍💻")
                lbl_avatar.setAlignment(QtCore.Qt.AlignCenter)
                lbl_avatar.setStyleSheet(
                    "font-size: 80px; background-color: #2D2F31; border-radius: 60px; padding: 20px;")
                lbl_avatar.setFixedSize(120, 120)

                self.lbl_profile_name = QtWidgets.QLabel("当前用户: admin")
                self.lbl_profile_name.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_profile_name.setStyleSheet(
                    "color: #FFFFFF; font-size: 22px; font-weight: bold; margin-top: 15px; border: none;")

                self.lbl_profile_role = QtWidgets.QLabel("👑 系统超级管理员")
                self.lbl_profile_role.setAlignment(QtCore.Qt.AlignCenter)
                self.lbl_profile_role.setStyleSheet(
                    "color: #F59E0B; font-size: 15px; font-weight: bold; background-color: rgba(245, 158, 11, 0.1); border-radius: 6px; padding: 5px;")

                info_style = "color: #9CA3AF; font-size: 15px; margin-top: 10px; border: none;"
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

                self.btn_profile_logout = QtWidgets.QPushButton("退出当前账号")
                self.btn_profile_logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_profile_logout.setStyleSheet(
                    "QPushButton { background-color: transparent; border: 2px solid #7F1D1D; color: #EF4444; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 15px; } QPushButton:hover { background-color: #7F1D1D; color: #FFFFFF; }")
                profile_layout.addWidget(self.btn_profile_logout)
                pc_layout.addWidget(self.card_profile, stretch=3)

                self.card_security = QtWidgets.QWidget()
                self.card_security.setStyleSheet(card_style)
                sec_layout = QtWidgets.QVBoxLayout(self.card_security)
                sec_layout.setContentsMargins(40, 40, 40, 40)
                sec_layout.setSpacing(20)

                lbl_sec_title = QtWidgets.QLabel("🔐 修改登录密码")
                lbl_sec_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold; border: none;")

                form_layout = QtWidgets.QFormLayout()
                form_layout.setSpacing(15)
                self.input_old_pwd = QtWidgets.QLineEdit()
                self.input_old_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
                self.input_old_pwd.setPlaceholderText("请输入原密码")
                self.input_new_pwd = QtWidgets.QLineEdit()
                self.input_new_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
                self.input_new_pwd.setPlaceholderText("请输入新密码")

                lbl_old = QtWidgets.QLabel("原密码:")
                lbl_old.setStyleSheet("color: #9CA3AF; font-size: 15px; border: none;")
                lbl_new = QtWidgets.QLabel("新密码:")
                lbl_new.setStyleSheet("color: #9CA3AF; font-size: 15px; border: none;")

                form_layout.addRow(lbl_old, self.input_old_pwd)
                form_layout.addRow(lbl_new, self.input_new_pwd)

                self.btn_save_pwd = QtWidgets.QPushButton("更新安全密码")
                self.btn_save_pwd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_save_pwd.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 16px; margin-top: 5px;} QPushButton:hover { background-color: #005B94; }")

                sec_layout.addWidget(lbl_sec_title)
                sec_layout.addLayout(form_layout)
                sec_layout.addWidget(self.btn_save_pwd)

                line = QtWidgets.QFrame()
                line.setFrameShape(QtWidgets.QFrame.HLine)
                line.setFrameShadow(QtWidgets.QFrame.Sunken)
                line.setStyleSheet("background-color: #333537; margin-top: 25px; margin-bottom: 25px;")
                sec_layout.addWidget(line)

                lbl_email_title = QtWidgets.QLabel("📧 修改绑定邮箱")
                lbl_email_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold; border: none;")

                email_layout = QtWidgets.QFormLayout()
                email_layout.setSpacing(15)
                self.input_new_email = QtWidgets.QLineEdit()
                self.input_new_email.setPlaceholderText("请输入新的邮箱地址")

                lbl_email = QtWidgets.QLabel("新邮箱:")
                lbl_email.setStyleSheet("color: #9CA3AF; font-size: 15px; border: none;")
                email_layout.addRow(lbl_email, self.input_new_email)

                self.btn_save_email = QtWidgets.QPushButton("更新绑定邮箱")
                self.btn_save_email.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_save_email.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 16px; margin-top: 5px;} QPushButton:hover { background-color: #005B94; }")

                sec_layout.addWidget(lbl_email_title)
                sec_layout.addLayout(email_layout)
                sec_layout.addWidget(self.btn_save_email)
                sec_layout.addStretch()

                pc_layout.addWidget(self.card_security, stretch=7)
                layout.addLayout(pc_layout)

            # 🌟 房间 6：AI 助手
            elif i == 6:
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
                self.input_chat.setPlaceholderText("请输入您的管理指令或数据问询，按回车键发送...")
                self.input_chat.setStyleSheet(
                    "QLineEdit { background-color: #131314; border: 1px solid #333537; border-radius: 25px; padding: 10px 25px; font-size: 16px; color: #E3E3E3; } QLineEdit:focus { border: 1px solid #66B2FF; }")
                self.input_chat.setFixedHeight(50)

                self.btn_send_chat = QtWidgets.QPushButton("下发指令 🚀")
                self.btn_send_chat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.btn_send_chat.setFixedSize(130, 50)
                self.btn_send_chat.setStyleSheet(
                    "QPushButton { background-color: #004A77; color: white; border-radius: 25px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #005B94; }")

                input_layout.addWidget(self.input_chat)
                input_layout.addWidget(self.btn_send_chat)
                chat_layout.addLayout(input_layout, stretch=1)
                layout.addLayout(chat_layout)

            self.stackedWidget.addWidget(page)
            self.pages.append(page)

        self.horizontalLayout_main.addWidget(self.stackedWidget)
        self.horizontalLayout_main.setStretch(0, 1)
        self.horizontalLayout_main.setStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)