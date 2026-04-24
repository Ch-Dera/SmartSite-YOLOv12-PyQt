import sys
import random
import string
import smtplib
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QPen

from UI.login_ui import Ui_Form
from main_app import MainApp

from admin_app import AdminWindow

from core.db_helper import DBHelper


class LoginWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 雇佣数据库大管家
        self.db = DBHelper()

        # 绑定核心动作
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.register)
        self.btn_refresh_captcha.clicked.connect(self.generate_captcha)
        self.btn_forgot_pwd.clicked.connect(self.forgot_password)

        # 回车键也可以直接登录！
        self.input_pwd.returnPressed.connect(self.login)
        self.input_captcha.returnPressed.connect(self.login)

        # 🌟 软件刚启动时，自动画一张验证码出来
        self.current_captcha_text = ""
        self.generate_captcha()

        # ==========================================

    # 🌟 手摇高级防爆破验证码生成器
    # ==========================================
    def generate_captcha(self):
        """生成 4 位随机字符和极具干扰性的安全验证码"""
        chars = random.choices(string.ascii_uppercase + string.digits, k=4)
        self.current_captcha_text = "".join(chars)

        width, height = 100, 42
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor("#FFFFFF"))  # 纯白背景
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 画干扰线
        for _ in range(5):
            painter.setPen(QPen(QColor(random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)), 2))
            painter.drawLine(random.randint(0, width), random.randint(0, height),
                             random.randint(0, width), random.randint(0, height))

        # 撒噪点
        for _ in range(50):
            painter.setPen(QPen(QColor(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)), 2))
            painter.drawPoint(random.randint(0, width), random.randint(0, height))

        # 画字母 (加入了倾斜和随机高度)
        font = QFont("Arial", 18, QFont.Bold)
        painter.setFont(font)
        for i, char in enumerate(chars):
            painter.setPen(QColor(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)))
            # 随机上下偏移一点，防止机器容易识别
            painter.drawText(15 + i * 20, random.randint(26, 34), char)

        painter.end()
        self.label_captcha.setPixmap(pixmap)

    # ==========================================
    # 📝 账号注册与绑定邮箱
    # ==========================================
    def register(self):
        username = self.input_user.text().strip()
        password = self.input_pwd.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "警告", "注册账号和密码不能为空！")
            return

        # 弹出一个极简风格的原生输入框
        email, ok = QInputDialog.getText(self, "绑定密保邮箱",
                                         "为了您的数据安全，请绑定密保邮箱：\n(用于后期重置系统密码)")

        if ok and email:
            if "@" not in email:
                QMessageBox.warning(self, "警告", "邮箱格式不正确！")
                return

            success = self.db.register_user(username, password, email)
            if success:
                QMessageBox.information(self, "成功", f"账号 [{username}] 注册成功！\n请牢记您的绑定邮箱：{email}")
                self.input_user.clear()
                self.input_pwd.clear()
            else:
                QMessageBox.warning(self, "警告", "注册失败，该账号可能已被注册！")
        else:
            QMessageBox.warning(self, "警告", "企业级系统必须绑定邮箱才能完成注册！")

    # ==========================================
    # 🚀 登录与大厅双剑合璧
    # ==========================================
    def login(self):
        user_captcha = self.input_captcha.text().strip().upper()

        # 1. 第一道防线：验证码防爆破
        if not user_captcha:
            QMessageBox.warning(self, "警告", "请输入右侧的安全验证码！")
            return
        elif user_captcha != self.current_captcha_text:
            QMessageBox.warning(self, "警告", "验证码输入错误！")
            self.generate_captcha()
            self.input_captcha.clear()
            return

        # 2. 第二道防线：账号校验
        username = self.input_user.text().strip()
        password = self.input_pwd.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "警告", "账号和密码不能为空！")
            return

        success, role = self.db.check_login(username, password)

        if success:
            if role == 'admin':
                QMessageBox.information(self, "最高权限", f"欢迎超级管理员：{username}！\n\n即将进入【管理端指挥中心】...")
                self.admin_window = AdminWindow()
                self.admin_window.show()
                self.close()
            else:
                # 🌟 核心交接：登录门关闭，唤醒深空暗黑指挥大厅！
                self.main_window = MainApp(username)
                self.main_window.show()
                self.close()
        else:
            QMessageBox.critical(self, "访问拒绝", "账号或系统密码不正确！")
            self.generate_captcha()
            self.input_captcha.clear()

    # ==========================================
    # 📧 邮箱找回密码核心引擎
    # ==========================================
    def forgot_password(self):
        username, ok1 = QInputDialog.getText(self, "找回密码", "请输入您的【系统账号】:")
        if not ok1 or not username: return

        email, ok2 = QInputDialog.getText(self, "找回密码", f"请输入账号 [{username}] 的【密保邮箱】:")
        if not ok2 or not email: return

        # 去数据库比验身份
        if not self.db.verify_user_email(username, email):
            QMessageBox.critical(self, "验证失败", "该系统账号与密保邮箱不匹配，请核实！")
            return

        QMessageBox.information(self, "系统提示", "正在连接邮件服务器，请稍候...")
        verify_code = "".join(random.choices(string.digits, k=6))

        if self.send_email_code(email, verify_code):
            user_code, ok3 = QInputDialog.getText(self, "安全验证", f"验证码已发送至 {email}\n请输入收到的 6 位验证码:")

            if ok3 and user_code == verify_code:
                new_pwd, ok4 = QInputDialog.getText(self, "重置密码", "身份验证通过！\n请设置新的系统登录密码:",
                                                    QLineEdit.Password)
                if ok4 and new_pwd:
                    self.db.reset_password(username, new_pwd)
                    QMessageBox.information(self, "大功告成", "密码重置成功！请使用新密码重新登录。")
            else:
                QMessageBox.warning(self, "错误", "验证码输入错误，重置被终止！")
        else:
            QMessageBox.critical(self, "网络错误", "验证码发送失败，请检查网络或联系超级管理员！")

    def send_email_code(self, receiver_email, code):
        """邮件发射井"""
        sender = '3499561169@qq.com'
        password = 'qoxfhaweqforchbh'

        mail_content = f"""
        【智慧工地安全检测系统 v2.0】

        您好！您正在尝试重置系统密码。
        您的专属验证码是：{code}

        (该验证码 5 分钟内有效。如非本人操作，请立刻联系系统管理员更改安全配置。)
        """
        message = MIMEText(mail_content, 'plain', 'utf-8')
        message['Subject'] = '【系统安全】智慧工地密码重置验证'
        message['From'] = sender
        message['To'] = receiver_email

        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(sender, password)
            server.sendmail(sender, [receiver_email], message.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_win = LoginWindow()
    login_win.show()
    sys.exit(app.exec_())