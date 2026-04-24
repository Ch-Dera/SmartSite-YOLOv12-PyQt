# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 550)
        Form.setMinimumSize(QtCore.QSize(800, 550))

        # 🌟 终极渲染魔法：给所有弹窗注入暗黑血统
        Form.setStyleSheet("""
            /* =======================================
               🌟 全局弹窗样式 (修复白底黑框的阴阳脸)
               ======================================= */
            QDialog, QMessageBox, QInputDialog {
                background-color: #1E1F22;
            }
            QDialog QLabel, QMessageBox QLabel, QInputDialog QLabel {
                color: #E6E8EA;
                font-size: 14px;
                font-family: "Microsoft YaHei";
            }
            QDialog QPushButton, QMessageBox QPushButton, QInputDialog QPushButton {
                background-color: #3574F0;
                color: white;
                border-radius: 6px;
                padding: 6px 18px;
                font-size: 14px;
                font-weight: bold;
                min-height: 30px;
                min-width: 80px;
            }
            QDialog QPushButton:hover, QMessageBox QPushButton:hover, QInputDialog QPushButton:hover {
                background-color: #4682F2;
            }

            /* =======================================
               🌟 登录面板基础样式
               ======================================= */
            QWidget#Form { 
                background-color: #0F111A; 
            }
            QWidget#card_widget {
                background-color: #1E1F22; 
                border: 1px solid #393B40;
                border-radius: 12px;
            }
            QLabel#title_label { 
                color: #E6E8EA; 
                font-size: 24px; 
                font-weight: bold; 
                font-family: "Microsoft YaHei";
                letter-spacing: 1px;
            }
            QLabel#subtitle_label { 
                color: #528BFF; 
                font-size: 12px; 
                font-weight: bold; 
                letter-spacing: 3px;
                margin-bottom: 5px;
            }
            QLineEdit { 
                background-color: #2B2D30; 
                border: 1px solid #43454A; 
                border-radius: 6px; 
                padding: 0px 15px; 
                min-height: 45px;  
                color: #E6E8EA; 
                font-size: 14px; 
                font-family: "Microsoft YaHei";
            }
            QLineEdit:focus { 
                border: 1px solid #528BFF; 
                background-color: #1E1F22;
            }
            QPushButton#btn_login { 
                background-color: #3574F0; 
                color: white; 
                border-radius: 6px; 
                min-height: 45px;  
                font-size: 16px; 
                font-weight: bold; 
                margin-top: 10px;
            }
            QPushButton#btn_login:hover { background-color: #4682F2; }

            QPushButton#btn_register { 
                background-color: transparent; 
                color: #9CA3AF; 
                border: 1px solid #43454A;
                border-radius: 6px; 
                min-height: 45px;  
                font-size: 16px; 
                font-weight: bold; 
            }
            QPushButton#btn_register:hover { 
                background-color: #2B2D30; 
                color: #E6E8EA;
            }

            QPushButton#btn_refresh_captcha { 
                background-color: #2B2D30; 
                border: 1px solid #43454A;
                color: #9CA3AF; 
                border-radius: 6px; 
                font-size: 20px; 
                min-height: 45px;  
            }
            QPushButton#btn_refresh_captcha:hover { 
                background-color: #393B40; 
                color: #FFFFFF;
            }

            QPushButton#btn_forgot_pwd {
                color: #8B949E; 
                background: transparent; 
                border: none;
                font-size: 13px;
                padding: 0px;
            }
            QPushButton#btn_forgot_pwd:hover { color: #528BFF; text-decoration: underline; }

            QLabel#label_captcha {
                background-color: #FFFFFF;
                border-radius: 6px;
            }
        """)

        self.main_layout = QtWidgets.QVBoxLayout(Form)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.card_widget = QtWidgets.QWidget(Form)
        self.card_widget.setObjectName("card_widget")
        self.card_widget.setFixedSize(400, 490)

        self.card_layout = QtWidgets.QVBoxLayout(self.card_widget)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(16)

        # --- 标题区 ---
        self.title_label = QtWidgets.QLabel("智慧工地管控系统")
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)

        self.subtitle_label = QtWidgets.QLabel("SYSTEM LOGIN")
        self.subtitle_label.setObjectName("subtitle_label")
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)

        self.card_layout.addWidget(self.title_label)
        self.card_layout.addWidget(self.subtitle_label)

        # --- 账号输入 ---
        self.input_user = QtWidgets.QLineEdit()
        self.input_user.setObjectName("input_user")
        self.input_user.setPlaceholderText("请输入系统账号")
        self.card_layout.addWidget(self.input_user)

        # --- 密码输入 ---
        self.input_pwd = QtWidgets.QLineEdit()
        self.input_pwd.setObjectName("input_pwd")
        self.input_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_pwd.setPlaceholderText("请输入登录密码")
        self.card_layout.addWidget(self.input_pwd)

        # --- 忘记密码对齐 ---
        self.pwd_tools_layout = QtWidgets.QHBoxLayout()
        self.pwd_tools_layout.setContentsMargins(0, 0, 5, 0)
        self.pwd_tools_layout.addStretch()
        self.btn_forgot_pwd = QtWidgets.QPushButton("忘记密码?")
        self.btn_forgot_pwd.setObjectName("btn_forgot_pwd")
        self.btn_forgot_pwd.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pwd_tools_layout.addWidget(self.btn_forgot_pwd)
        self.card_layout.addLayout(self.pwd_tools_layout)

        # --- 验证码区 ---
        self.captcha_layout = QtWidgets.QHBoxLayout()
        self.captcha_layout.setSpacing(12)

        self.input_captcha = QtWidgets.QLineEdit()
        self.input_captcha.setObjectName("input_captcha")
        self.input_captcha.setPlaceholderText("验证码")
        self.captcha_layout.addWidget(self.input_captcha, stretch=1)

        self.label_captcha = QtWidgets.QLabel()
        self.label_captcha.setObjectName("label_captcha")
        self.label_captcha.setFixedSize(100, 45)
        self.captcha_layout.addWidget(self.label_captcha, stretch=0)

        self.btn_refresh_captcha = QtWidgets.QPushButton("↻")
        self.btn_refresh_captcha.setObjectName("btn_refresh_captcha")
        self.btn_refresh_captcha.setFixedSize(45, 45)
        self.btn_refresh_captcha.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.captcha_layout.addWidget(self.btn_refresh_captcha, stretch=0)

        self.card_layout.addLayout(self.captcha_layout)

        # --- 按钮区 ---
        self.btn_login = QtWidgets.QPushButton("登录")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.card_layout.addWidget(self.btn_login)

        self.btn_register = QtWidgets.QPushButton("注册")
        self.btn_register.setObjectName("btn_register")
        self.btn_register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.card_layout.addWidget(self.btn_register)

        self.main_layout.addWidget(self.card_widget)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "智慧工地管控系统 - 登录"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())