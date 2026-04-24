import pymysql
import datetime


class DBHelper:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.database = 'helmet_system'
        self.create_tables()

    def connect(self):
        try:
            conn = pymysql.connect(
                host=self.host, user=self.user, password=self.password,
                database=self.database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return None

    def create_tables(self):
        conn = self.connect()
        if not conn: return
        try:
            with conn.cursor() as cursor:
                # 1. 用户表
                sql_users = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'operator',
                    email VARCHAR(100) NOT NULL
                )
                """
                cursor.execute(sql_users)

                # 2. 违规记录表
                sql_records = """
                CREATE TABLE IF NOT EXISTS alert_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    alert_time DATETIME NOT NULL,
                    event_type VARCHAR(50) NOT NULL,
                    confidence VARCHAR(20) NOT NULL,
                    image_path VARCHAR(255),
                    operator_name VARCHAR(50) NOT NULL
                )
                """
                cursor.execute(sql_records)

                # 3. 考勤打卡表
                sql_attendance = """
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    check_time DATETIME NOT NULL,
                    status VARCHAR(20) DEFAULT '已签到'
                )
                """
                cursor.execute(sql_attendance)
            conn.commit()
        except Exception as e:
            print(f"⚠️ 建表失败: {e}")
        finally:
            conn.close()

    def check_login(self, username, password):
        conn = self.connect()
        if not conn: return False, None
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
                result = cursor.fetchone()
                return (True, result['role']) if result else (False, None)
        finally:
            conn.close()

    def register_user(self, username, password, email, role='operator'):
        conn = self.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password, role, email) VALUES (%s, %s, %s, %s)",
                               (username, password, role, email))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def verify_user_email(self, username, email):
        conn = self.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s AND email = %s", (username, email))
                return cursor.fetchone() is not None
        finally:
            conn.close()

    def reset_password(self, username, new_password):
        conn = self.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
            conn.commit()
            return True
        finally:
            conn.close()

    def insert_record(self, alert_time, event_type, confidence, image_path, operator_name):
        conn = self.connect()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO alert_records (alert_time, event_type, confidence, image_path, operator_name) VALUES (%s, %s, %s, %s, %s)",
                    (alert_time, event_type, confidence, image_path, operator_name))
            conn.commit()
            return True
        finally:
            conn.close()

    def get_all_records(self):
        conn = self.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM alert_records ORDER BY id DESC")
                return cursor.fetchall()
        finally:
            conn.close()

    def get_records_by_user(self, username):
        conn = self.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM alert_records WHERE operator_name = %s ORDER BY id ASC", (username,))
                return cursor.fetchall()
        finally:
            conn.close()

    def update_user_password(self, username, old_pwd, new_pwd):
        conn = self.connect()
        if not conn: return False, "数据库连接失败"
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if not result: return False, "系统找不到该用户"
                if str(result['password']) != str(old_pwd): return False, "原密码输入错误"
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_pwd, username))
            conn.commit()
            return True, "密码更新成功"
        except Exception as e:
            return False, f"数据库异常: {str(e)}"
        finally:
            conn.close()

    def update_user_email(self, username, new_email):
        conn = self.connect()
        if not conn: return False, "数据库连接失败"
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET email = %s WHERE username = %s", (new_email, username))
            conn.commit()
            return True, "邮箱已成功入库"
        except Exception as e:
            return False, f"数据库异常: {str(e)}"
        finally:
            conn.close()

    # ==========================
    # 🌟 新增：考勤打卡硬核接口
    # ==========================
    def add_check_in(self, username):
        """写入打卡记录（防重复打卡）"""
        conn = self.connect()
        if not conn: return False, "数据库连接失败"
        try:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            with conn.cursor() as cursor:
                cursor.execute("SELECT check_time FROM attendance WHERE username=%s AND DATE(check_time)=%s",
                               (username, today))
                if cursor.fetchone():
                    return False, "您今日已打卡，无需重复操作！"
                cursor.execute("INSERT INTO attendance (username, check_time) VALUES (%s, NOW())", (username,))
            conn.commit()
            return True, "签到成功"
        except Exception as e:
            return False, f"打卡异常: {e}"
        finally:
            conn.close()

    def get_today_check_in(self, username):
        """查询今日打卡时间"""
        conn = self.connect()
        if not conn: return None
        try:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            with conn.cursor() as cursor:
                cursor.execute("SELECT check_time FROM attendance WHERE username=%s AND DATE(check_time)=%s",
                               (username, today))
                res = cursor.fetchone()
                return res['check_time'] if res else None
        finally:
            conn.close()

    def get_attendance_days(self, username):
        """统计本月全勤天数"""
        conn = self.connect()
        if not conn: return 0
        try:
            current_month = datetime.datetime.now().strftime('%Y-%m')
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(DISTINCT DATE(check_time)) as days FROM attendance WHERE username=%s AND DATE_FORMAT(check_time, '%%Y-%%m')=%s",
                    (username, current_month))
                res = cursor.fetchone()
                return res['days'] if res else 0
        finally:
            conn.close()

    def get_all_users(self):
        """获取系统里的所有员工账号信息"""
        conn = self.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, username, role, email FROM users ORDER BY id ASC")
                return cursor.fetchall()
        finally:
            conn.close()

    def delete_user(self, target_username):
        """开除员工：硬核删除账号"""
        if target_username == 'admin':
            return False, "系统警告：无法删除超级管理员账号！"

        conn = self.connect()
        if not conn: return False, "数据库连接失败"

        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE username = %s", (target_username,))
            conn.commit()
            return True, f"账号 {target_username} 已被永久删除！"
        except Exception as e:
            return False, f"删除异常: {e}"
        finally:
            conn.close()

    def get_all_attendance(self):
        """获取所有员工的考勤流水"""
        conn = self.connect()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM attendance ORDER BY check_time DESC")
                return cursor.fetchall()
        finally:
            conn.close()

    def edit_user(self, uid, new_role, new_email, new_password=""):
        """🌟 超管专属：修改员工的权限、邮箱，乃至强制重置密码"""
        conn = self.connect()
        if not conn: return False, "数据库连接失败"
        try:
            with conn.cursor() as cursor:
                # 如果没填密码，就不修改密码；如果填了，就一起强制覆盖
                if new_password:
                    cursor.execute("UPDATE users SET role=%s, email=%s, password=%s WHERE id=%s",
                                   (new_role, new_email, new_password, uid))
                else:
                    cursor.execute("UPDATE users SET role=%s, email=%s WHERE id=%s", (new_role, new_email, uid))
            conn.commit()
            return True, "员工信息修改成功"
        except Exception as e:
            return False, f"修改异常: {e}"
        finally:
            conn.close()
