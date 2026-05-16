"""
主题管理器 — 为智慧工地安全管控系统提供深空暗黑与工业亮白双主题切换
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5.QtGui import QColor


# ============================================================
# 📌 主题常量定义
# ============================================================
THEME_DARK = "深空暗黑 (Dark Theme)"
THEME_LIGHT = "工业亮白 (Light Theme)"

# ============================================================
# 🌙 深空暗黑主题 (原版风格)
# ============================================================
DARK_THEME = """
    * { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; 
        font-size: 15px; 
    }
    QWidget#centralwidget { background-color: #131314; }
    QWidget#left_sidebar { background-color: #1E1F20; border-right: 1px solid #333537; }
    QLabel#label_main_title { font-size: 26px; font-weight: bold; color: #FFFFFF; padding-top: 30px; }
    QLabel#label_sub_title { font-size: 15px; color: #9CA3AF; padding-bottom: 25px; border-bottom: 1px solid #333537; margin-bottom: 25px; letter-spacing: 2px;}

    QPushButton[class="nav_btn"] { background-color: transparent; color: #C4C7C5; font-size: 19px; text-align: center; border: 1px solid transparent; border-radius: 28px; font-weight: normal; }
    QPushButton[class="nav_btn"]:hover { background-color: #333537; color: #FFFFFF; }
    QPushButton[class="nav_btn"]:checked { background-color: #004A77; color: #C3E7FF; font-weight: bold; border: 1px solid #004A77; border-radius: 28px; }
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
    QCheckBox::indicator:checked { background-color: #004A77; border: 1px solid #004A77; }
    QCheckBox::indicator:hover { border: 1px solid #66B2FF; }

    QSpinBox { background-color: #131314; color: #E3E3E3; border: 1px solid #333537; border-radius: 6px; padding: 5px 10px; min-height: 25px; font-size: 15px; }
    QSpinBox:focus, QSpinBox:hover { border: 1px solid #66B2FF; }
    QSpinBox::up-button, QSpinBox::down-button { width: 20px; background-color: transparent; border-left: 1px solid #333537; }
    QSpinBox::up-button:hover, QSpinBox::down-button:hover { background-color: #333537; }
    
    QScrollBar:vertical { background: #131314; width: 10px; border-radius: 5px; }
    QScrollBar::handle:vertical { background: #333537; border-radius: 5px; min-height: 30px; }
    QScrollBar::handle:vertical:hover { background: #4B5563; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    QScrollBar:horizontal { background: #131314; height: 10px; border-radius: 5px; }
    QScrollBar::handle:horizontal { background: #333537; border-radius: 5px; min-width: 30px; }
    QScrollBar::handle:horizontal:hover { background: #4B5563; }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
    
    QDialog { background-color: #1E1F20; }
    QDialog QLabel { color: #E3E3E3; }
    QMessageBox { background-color: #1E1F20; }
    QMessageBox QLabel { color: #E3E3E3; }
    QInputDialog { background-color: #1E1F20; }
    QInputDialog QLabel { color: #E3E3E3; }
    
    QProgressBar { background-color: #131314; border: 1px solid #333537; border-radius: 6px; text-align: center; color: #E3E3E3; }
    QProgressBar::chunk { background-color: #004A77; border-radius: 4px; }
    
    QListWidget { background-color: #131314; color: #E3E3E3; border-radius: 6px; padding: 5px; font-size: 14px; }
    QListWidget::item:selected { background-color: #004A77; color: #FFFFFF; }
"""

# ============================================================
# ☀️ 工业亮白主题 (全新设计)
# ============================================================
LIGHT_THEME = """
    * { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; 
        font-size: 15px; 
    }
    QWidget#centralwidget { background-color: #F0F4F8; }
    QWidget#left_sidebar { background-color: #FFFFFF; border-right: 1px solid #D1D5DB; }
    QLabel#label_main_title { font-size: 26px; font-weight: bold; color: #1E293B; padding-top: 30px; }
    QLabel#label_sub_title { font-size: 15px; color: #64748B; padding-bottom: 25px; border-bottom: 1px solid #E2E8F0; margin-bottom: 25px; letter-spacing: 2px;}

    QPushButton[class="nav_btn"] { background-color: transparent; color: #475569; font-size: 19px; text-align: center; border: 1px solid transparent; border-radius: 28px; font-weight: normal; }
    QPushButton[class="nav_btn"]:hover { background-color: #E2E8F0; color: #1E293B; }
    QPushButton[class="nav_btn"]:checked { background-color: #2563EB; color: #FFFFFF; font-weight: bold; border: 1px solid #2563EB; border-radius: 28px; }
    QLabel[class="page_title"] { font-size: 28px; font-weight: bold; color: #1E293B; }

    QTableWidget { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 12px; gridline-color: transparent; font-size: 15px; color: #1E293B; padding: 5px; }
    QHeaderView::section { background-color: #F8FAFC; color: #64748B; font-weight: bold; font-size: 15px; padding: 15px; border: none; border-bottom: 1px solid #E2E8F0; }
    QTableWidget::item { border-bottom: 1px solid #F1F5F9; padding: 8px; }
    QTableWidget::item:selected { background-color: #DBEAFE; color: #1E40AF; }

    QLineEdit { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 0px 15px; min-height: 38px; color: #1E293B; font-size: 15px; }
    QLineEdit:focus { border: 1px solid #2563EB; }

    QDateEdit { background-color: #FFFFFF; color: #1E293B; border: 1px solid #D1D5DB; border-radius: 6px; padding: 6px 10px; font-size: 15px; min-width: 120px; }
    QDateEdit:hover { border: 1px solid #2563EB; }
    QComboBox { background-color: #FFFFFF; color: #1E293B; border: 1px solid #D1D5DB; border-radius: 6px; padding: 6px 10px; font-size: 15px; }
    QComboBox:hover { border: 1px solid #2563EB; }
    QComboBox QAbstractItemView { background-color: #FFFFFF; color: #1E293B; selection-background-color: #DBEAFE; selection-color: #1E40AF; }

    QTabWidget::pane { border: 1px solid #D1D5DB; background: #FFFFFF; border-radius: 8px; top: -1px; }
    QTabBar::tab { background: #F1F5F9; color: #64748B; border: 1px solid #D1D5DB; padding: 10px 25px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px; }
    QTabBar::tab:selected { background: #FFFFFF; color: #2563EB; font-weight: bold; border-bottom-color: #FFFFFF; }
    QTabBar::tab:hover:!selected { background: #E2E8F0; color: #1E293B; }
    QWidget#tab_workspace, QWidget#tab_security { background-color: #FFFFFF; }
    QCheckBox { color: #1E293B; font-size: 15px; }
    QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 1px solid #D1D5DB; background-color: #FFFFFF; }
    QCheckBox::indicator:checked { background-color: #2563EB; border: 1px solid #2563EB; }
    QCheckBox::indicator:hover { border: 1px solid #2563EB; }

    QSpinBox { background-color: #FFFFFF; color: #1E293B; border: 1px solid #D1D5DB; border-radius: 6px; padding: 5px 10px; min-height: 25px; font-size: 15px; }
    QSpinBox:focus, QSpinBox:hover { border: 1px solid #2563EB; }
    QSpinBox::up-button, QSpinBox::down-button { width: 20px; background-color: transparent; border-left: 1px solid #D1D5DB; }
    QSpinBox::up-button:hover, QSpinBox::down-button:hover { background-color: #E2E8F0; }
    
    QScrollBar:vertical { background: #F1F5F9; width: 10px; border-radius: 5px; }
    QScrollBar::handle:vertical { background: #CBD5E1; border-radius: 5px; min-height: 30px; }
    QScrollBar::handle:vertical:hover { background: #94A3B8; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    QScrollBar:horizontal { background: #F1F5F9; height: 10px; border-radius: 5px; }
    QScrollBar::handle:horizontal { background: #CBD5E1; border-radius: 5px; min-width: 30px; }
    QScrollBar::handle:horizontal:hover { background: #94A3B8; }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
    
    QDialog { background-color: #FFFFFF; }
    QDialog QLabel { color: #1E293B; }
    QMessageBox { background-color: #FFFFFF; }
    QMessageBox QLabel { color: #1E293B; }
    QInputDialog { background-color: #FFFFFF; }
    QInputDialog QLabel { color: #1E293B; }
    
    QProgressBar { background-color: #E2E8F0; border: 1px solid #D1D5DB; border-radius: 6px; text-align: center; color: #1E293B; }
    QProgressBar::chunk { background-color: #2563EB; border-radius: 4px; }
    
    QListWidget { background-color: #FFFFFF; color: #1E293B; border-radius: 6px; padding: 5px; font-size: 14px; border: 1px solid #D1D5DB; }
    QListWidget::item:selected { background-color: #DBEAFE; color: #1E40AF; }
"""


# ============================================================
# 🎨 主题应用工具函数
# ============================================================

def get_theme_stylesheet(theme_name):
    """根据主题名称返回对应的完整样式表"""
    if theme_name == THEME_LIGHT:
        return LIGHT_THEME
    return DARK_THEME


def apply_theme(window, theme_name):
    """为指定窗口应用主题样式表
    
    Args:
        window: QMainWindow 实例
        theme_name: 主题名称 (THEME_DARK / THEME_LIGHT)
    """
    stylesheet = get_theme_stylesheet(theme_name)
    window.setStyleSheet(stylesheet)
    
    # 如果是亮色主题，还需要更新内联样式相关的控件颜色
    if theme_name == THEME_LIGHT:
        _apply_light_theme_overrides(window)
    else:
        _apply_dark_theme_overrides(window)


def _apply_dark_theme_overrides(window):
    """深空暗黑主题的内联样式完全覆盖 — 涵盖 modern_ui.py 和 admin_ui.py 所有硬编码控件"""

    # ================================================================
    # 1. 🏠 首页欢迎区
    # ================================================================
    if hasattr(window, 'lbl_welcome_title'):
        window.lbl_welcome_title.setStyleSheet("color: #FFFFFF; font-size: 36px; font-weight: bold; border: none;")
    if hasattr(window, 'lbl_welcome_sub'):
        window.lbl_welcome_sub.setStyleSheet("color: #9CA3AF; font-size: 16px; border: none; margin-top: 10px;")
    if hasattr(window, 'lbl_admin_welcome'):
        window.lbl_admin_welcome.setStyleSheet("color: #FFFFFF; font-size: 36px; font-weight: bold; border: none;")
    if hasattr(window, 'lbl_admin_sub'):
        window.lbl_admin_sub.setStyleSheet("color: #9CA3AF; font-size: 16px; border: none; margin-top: 10px; margin-bottom: 15px;")

    # ================================================================
    # 2. 🏷️ 信息徽章
    # ================================================================
    badge_style = "background-color: #2D2F31; color: #66B2FF; padding: 8px 15px; border-radius: 6px; font-size: 14px; font-weight: bold; border: 1px solid #333537;"
    for attr in ['lbl_home_user', 'lbl_home_role', 'lbl_home_model', 'lbl_home_device']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(badge_style)

    # ================================================================
    # 3. 🕒 实时时钟
    # ================================================================
    if hasattr(window, 'lbl_realtime_clock'):
        window.lbl_realtime_clock.setStyleSheet("color: #66B2FF; font-size: 58px; font-weight: 900; font-family: 'Arial'; border: none; letter-spacing: 2px;")

    # ================================================================
    # 4. 📊 统计数字
    # ================================================================
    card_map = {
        'lbl_stat_total': ("#EF4444", "38px"),
        'lbl_stat_today': ("#F59E0B", "38px"),
        'lbl_stat_source': ("#3B82F6", "28px"),
        'lbl_total_users': ("#66B2FF", "42px"),
        'lbl_total_alerts': ("#EF4444", "42px"),
        'lbl_today_att': ("#10B981", "42px"),
    }
    for attr, (color, size) in card_map.items():
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(f"color: {color}; font-size: {size}; font-weight: 900; border: none;")

    # ================================================================
    # 5. 🃏 统计卡片标题标签
    # ================================================================
    card_title_dark = "color: #9CA3AF; font-size: 16px; font-weight: bold; border: none;"
    for attr in ['lbl_c1_title', 'lbl_c2_title', 'lbl_c3_title']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(card_title_dark)

    # ================================================================
    # 6. 📦 卡片容器
    # ================================================================
    card_bg  = "QWidget { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; } QLabel { border: none; }"
    card_bg2 = "QWidget { background-color: #1E1F22; border: 1px solid #393B40; border-radius: 12px; }"
    for attr in ['card_total', 'card_today', 'card_top_source', 'card_profile', 'card_security']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg)
    for attr in ['card_welcome', 'card_quick', 'card_punch']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg2)
    for attr in ['card_ai', 'card_storage', 'card_alert', 'card_ui']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg)
    # 管理端
    for attr in ['card_users', 'card_alerts', 'card_att']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg2)
    # 管理端图表容器
    for attr in ['container_global_pie', 'container_global_bar', 'container_att_pie', 'container_att_bar']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg2)

    # ================================================================
    # 7. 🚀 快捷启动按钮
    # ================================================================
    for btn_attr in ['btn_quick_img', 'btn_quick_vid', 'btn_quick_rt']:
        if hasattr(window, btn_attr):
            getattr(window, btn_attr).setStyleSheet(
                "QPushButton { background-color: #2B2D30; color: #E6E8EA; border: 1px solid #43454A; border-radius: 8px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #3574F0; border: none; color: white; }")

    # ================================================================
    # 8. ✅ 签到按钮 & 签到信息
    # ================================================================
    if hasattr(window, 'btn_check_in'):
        window.btn_check_in.setStyleSheet(
            "QPushButton { background-color: #3574F0; color: white; border-radius: 70px; font-size: 22px; font-weight: bold; border: 8px solid rgba(53, 116, 240, 0.3); } QPushButton:hover { background-color: #4682F2; } QPushButton:disabled { background-color: #10B981; border: 8px solid rgba(16, 185, 129, 0.3); color: white; font-size: 20px; }")
    if hasattr(window, 'lbl_check_in_msg'):
        window.lbl_check_in_msg.setStyleSheet("color: #9CA3AF; font-size: 15px; border: none; margin-top: 15px;")

    # ================================================================
    # 9. 🔹 快捷/签到区域标题标签
    # ================================================================
    for attr in ['lbl_quick', 'lbl_punch']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold; border: none;")

    # ================================================================
    # 10. ⏱️ 状态指示标签
    # ================================================================
    status_label_dark = "background-color: #1E1F20; border: 1px solid #333537; border-radius: 8px; padding: 8px 15px; color: #C3E7FF; font-weight: bold; font-size: 15px;"
    for attr in ['label_time_image', 'label_targets_image', 'label_fps_video', 'label_targets_video']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(status_label_dark)

    # ================================================================
    # 11. 🔵 置信度标签
    # ================================================================
    conf_label_dark = "color: #9CA3AF; font-weight: bold; font-size: 15px; border: none;"
    for attr in ['label_conf_image', 'label_conf_video', 'label_conf_rt']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(conf_label_dark)

    # ================================================================
    # 12. ⚙️ 系统设置 — 默认置信度数值
    # ================================================================
    if hasattr(window, 'lbl_default_conf_val'):
        window.lbl_default_conf_val.setStyleSheet("color: #66B2FF; font-weight: bold; font-size: 16px;")

    # ================================================================
    # 13. 📂 浏览路径按钮
    # ================================================================
    if hasattr(window, 'btn_browse_path'):
        window.btn_browse_path.setStyleSheet(
            "QPushButton { background-color: #2D2F31; color: white; border: 1px solid #43454A; border-radius: 4px; padding: 8px 15px; font-weight:bold; } QPushButton:hover { background-color: #444746; }")

    # ================================================================
    # 14. 🔍 搜索/操作按钮（primary: blue）
    # ================================================================
    primary_btn = "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 15px; min-height: 28px;} QPushButton:hover { background-color: #005B94; }"
    for attr in ['btn_search_history', 'btn_search_global', 'btn_search_user', 'btn_search_att', 'btn_upload_image', 'btn_upload_video']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(primary_btn)

    # ================================================================
    # 15. 🔄 重置/次要按钮
    # ================================================================
    secondary_btn = "QPushButton { background-color: #2D2F31; color: white; border: 1px solid #43454A; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 10px; min-height: 28px;} QPushButton:hover { background-color: #444746; }"
    for attr in ['btn_reset_history', 'btn_reset_global', 'btn_reset_user']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(secondary_btn)

    # ================================================================
    # 16. ➕ 新增用户按钮（绿色）
    # ================================================================
    if hasattr(window, 'btn_add_user_dialog'):
        window.btn_add_user_dialog.setStyleSheet(
            "QPushButton { background-color: #065F46; color: white; border-radius: 6px; font-weight: bold; font-size: 15px;} QPushButton:hover { background-color: #059669; }")

    # ================================================================
    # 17. 🎨 系统设置保存按钮
    # ================================================================
    if hasattr(window, 'btn_save_system'):
        window.btn_save_system.setStyleSheet(
            "QPushButton { background-color: #004A77; color: white; border-radius: 8px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #005B94; }")

    # ================================================================
    # 18. 🤖 AI 聊天区域
    # ================================================================
    if hasattr(window, 'chat_display'):
        window.chat_display.setStyleSheet(
            "QTextBrowser { background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px; padding: 25px; font-size: 16px; color: #E3E3E3; }")
    if hasattr(window, 'input_chat'):
        window.input_chat.setStyleSheet(
            "QLineEdit { background-color: #131314; border: 1px solid #333537; border-radius: 25px; padding: 10px 25px; font-size: 16px; color: #E3E3E3; } QLineEdit:focus { border: 1px solid #66B2FF; }")
    if hasattr(window, 'btn_send_chat'):
        window.btn_send_chat.setStyleSheet(
            "QPushButton { background-color: #004A77; color: white; border-radius: 25px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #005B94; }")

    # ================================================================
    # 19. 📡 通道面板
    # ================================================================
    if hasattr(window, 'channel_panel'):
        window.channel_panel.setStyleSheet("background-color: #1E1F20; border: 1px solid #333537; border-radius: 12px;")
    if hasattr(window, 'lbl_ch_title'):
        window.lbl_ch_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold; border: none;")
    if hasattr(window, 'input_rtsp'):
        window.input_rtsp.setStyleSheet("QLineEdit { background-color: #131314; border: 1px solid #333537; border-radius: 6px; padding: 8px; font-size: 14px; color: #E3E3E3; }")
    if hasattr(window, 'btn_browse_rt'):
        window.btn_browse_rt.setStyleSheet("QPushButton { background-color: #2D2F31; color: white; border-radius: 6px; padding: 8px; font-weight:bold; } QPushButton:hover { background-color: #444746; }")
    if hasattr(window, 'btn_add_rt'):
        window.btn_add_rt.setStyleSheet("QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 8px; font-weight:bold; } QPushButton:hover { background-color: #005B94; }")
    if hasattr(window, 'btn_remove_rt'):
        window.btn_remove_rt.setStyleSheet("QPushButton { background-color: transparent; border: 1px solid #7F1D1D; color: #EF4444; border-radius: 6px; padding: 8px; font-weight:bold; } QPushButton:hover { background-color: #7F1D1D; color: white; }")
    if hasattr(window, 'btn_start_cams'):
        window.btn_start_cams.setStyleSheet("QPushButton { background-color: #10B981; color: white; border-radius: 6px; padding: 12px; font-weight:bold; font-size: 16px; } QPushButton:hover { background-color: #059669; }")
    if hasattr(window, 'btn_stop_cams'):
        window.btn_stop_cams.setStyleSheet("QPushButton { background-color: #DC2626; color: white; border-radius: 6px; padding: 12px; font-weight:bold; font-size: 16px; } QPushButton:hover { background-color: #B91C1C; }")
    if hasattr(window, 'list_channels'):
        window.list_channels.setStyleSheet("background-color: #131314; color: #E3E3E3; border-radius: 6px; padding: 5px; font-size: 14px;")

    # ================================================================
    # 20. 👤 个人中心
    # ================================================================
    if hasattr(window, 'lbl_avatar'):
        window.lbl_avatar.setStyleSheet("font-size: 80px; background-color: #2D2F31; border-radius: 60px; padding: 20px;")
    if hasattr(window, 'lbl_profile_name'):
        window.lbl_profile_name.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold; margin-top: 15px; border: none;")
    if hasattr(window, 'lbl_profile_role'):
        window.lbl_profile_role.setStyleSheet("color: #F59E0B; font-size: 14px; font-weight: bold; background-color: rgba(245, 158, 11, 0.1); border-radius: 6px; padding: 5px;")
    info_dark = "color: #9CA3AF; font-size: 14px; border: none;"
    for attr in ['lbl_login_time', 'lbl_login_ip']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(info_dark)
    if hasattr(window, 'lbl_checkin_status'):
        window.lbl_checkin_status.setStyleSheet("color: #10B981; font-size: 18px; font-weight: bold; background-color: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 8px;")
    if hasattr(window, 'lbl_attendance_days'):
        window.lbl_attendance_days.setStyleSheet("color: #E3E3E3; font-size: 16px; margin-top: 10px;")
    if hasattr(window, 'lbl_personal_intercept'):
        window.lbl_personal_intercept.setStyleSheet("color: #66B2FF; font-size: 16px; margin-top: 10px;")
    if hasattr(window, 'btn_logout'):
        window.btn_logout.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #7F1D1D; color: #EF4444; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 15px; } QPushButton:hover { background-color: #7F1D1D; color: #FFFFFF; }")
    if hasattr(window, 'btn_admin_logout'):
        window.btn_admin_logout.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #7F1D1D; color: #EF4444; border-radius: 6px; font-weight: bold; font-size: 18px; } QPushButton:hover { background-color: #7F1D1D; color: #FFFFFF; }")
    if hasattr(window, 'btn_profile_logout'):
        window.btn_profile_logout.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #7F1D1D; color: #EF4444; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 15px; } QPushButton:hover { background-color: #7F1D1D; color: #FFFFFF; }")

    # ================================================================
    # 21. 🔐 安全设置区
    # ================================================================
    section_title_dark = "color: #FFFFFF; font-size: 18px; font-weight: bold; border: none;"
    for attr in ['lbl_sec_title', 'lbl_email_title', 'lbl_theme_title']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(section_title_dark)

    form_label_dark = "color: #9CA3AF; font-size: 15px; border: none;"
    for attr in ['lbl_old', 'lbl_new', 'lbl_email', 'lbl_theme']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(form_label_dark)

    secure_btn = "QPushButton { background-color: #004A77; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 16px; margin-top: 5px;} QPushButton:hover { background-color: #005B94; }"
    for attr in ['btn_save_pwd', 'btn_save_email', 'btn_apply_theme']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(secure_btn)

    # ================================================================
    # 22. ➖ 分割线
    # ================================================================
    line_dark = "background-color: #333537; margin-top: 25px; margin-bottom: 25px;"
    _apply_line_overrides(window, line_dark)

    # ================================================================
    # 23. 📅 筛选标签（管理端）
    # ================================================================
    filter_label_dark = "color: #9CA3AF; font-size: 15px; font-weight: bold; border: none;"
    for attr in ['label_filter_date', 'label_filter_event', 'label_filter_operator', 'lbl_att_date']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(filter_label_dark)


def _apply_light_theme_overrides(window):
    """工业亮白主题的内联样式完全覆盖 — 涵盖 modern_ui.py 和 admin_ui.py 所有硬编码控件"""

    # ================================================================
    # 1. 🏠 首页欢迎区
    # ================================================================
    # 操作员欢迎标题
    if hasattr(window, 'lbl_welcome_title'):
        window.lbl_welcome_title.setStyleSheet("color: #1E293B; font-size: 36px; font-weight: bold; border: none;")
    if hasattr(window, 'lbl_welcome_sub'):
        window.lbl_welcome_sub.setStyleSheet("color: #475569; font-size: 16px; border: none; margin-top: 10px;")
    # 管理员欢迎标题
    if hasattr(window, 'lbl_admin_welcome'):
        window.lbl_admin_welcome.setStyleSheet("color: #1E293B; font-size: 36px; font-weight: bold; border: none;")
    if hasattr(window, 'lbl_admin_sub'):
        window.lbl_admin_sub.setStyleSheet("color: #475569; font-size: 16px; border: none; margin-top: 10px; margin-bottom: 15px;")

    # ================================================================
    # 2. 🏷️ 信息徽章
    # ================================================================
    badge_style = "background-color: #EFF6FF; color: #2563EB; padding: 8px 15px; border-radius: 6px; font-size: 14px; font-weight: bold; border: 1px solid #BFDBFE;"
    for attr in ['lbl_home_user', 'lbl_home_role', 'lbl_home_model', 'lbl_home_device']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(badge_style)

    # ================================================================
    # 3. 🕒 实时时钟
    # ================================================================
    if hasattr(window, 'lbl_realtime_clock'):
        window.lbl_realtime_clock.setStyleSheet("color: #2563EB; font-size: 58px; font-weight: 900; font-family: 'Arial'; border: none; letter-spacing: 2px;")

    # ================================================================
    # 4. 📊 统计数字（状态色保持不变）
    # ================================================================
    card_map = {
        'lbl_stat_total': ("#DC2626", "38px"),
        'lbl_stat_today': ("#D97706", "38px"),
        'lbl_stat_source': ("#2563EB", "28px"),
        'lbl_total_users': ("#2563EB", "42px"),
        'lbl_total_alerts': ("#DC2626", "42px"),
        'lbl_today_att': ("#059669", "42px"),
    }
    for attr, (color, size) in card_map.items():
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(f"color: {color}; font-size: {size}; font-weight: 900; border: none;")

    # ================================================================
    # 5. 🃏 统计卡片标题标签
    # ================================================================
    card_title_light = "color: #475569; font-size: 16px; font-weight: bold; border: none;"
    for attr in ['lbl_c1_title', 'lbl_c2_title', 'lbl_c3_title']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(card_title_light)

    # ================================================================
    # 6. 📦 卡片容器
    # ================================================================
    card_bg  = "QWidget { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 12px; } QLabel { border: none; }"
    card_bg2 = "QWidget { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 12px; }"
    for attr in ['card_total', 'card_today', 'card_top_source', 'card_profile', 'card_security']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg)
    for attr in ['card_welcome', 'card_quick', 'card_punch']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg2)
    for attr in ['card_ai', 'card_storage', 'card_alert', 'card_ui']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg)
    # 管理端统计卡片
    for attr in ['card_users', 'card_alerts', 'card_att']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg2)
    # 管理端图表容器
    for attr in ['container_global_pie', 'container_global_bar', 'container_att_pie', 'container_att_bar']:
        if hasattr(window, attr): getattr(window, attr).setStyleSheet(card_bg2)

    # ================================================================
    # 7. 🚀 快捷启动按钮
    # ================================================================
    for btn_attr in ['btn_quick_img', 'btn_quick_vid', 'btn_quick_rt']:
        if hasattr(window, btn_attr):
            getattr(window, btn_attr).setStyleSheet(
                "QPushButton { background-color: #F1F5F9; color: #1E293B; border: 1px solid #D1D5DB; border-radius: 8px; font-size: 16px; font-weight: bold; } QPushButton:hover { background-color: #2563EB; border: none; color: white; }")

    # ================================================================
    # 8. ✅ 签到按钮 & 签到信息
    # ================================================================
    if hasattr(window, 'btn_check_in'):
        window.btn_check_in.setStyleSheet(
            "QPushButton { background-color: #2563EB; color: white; border-radius: 70px; font-size: 22px; font-weight: bold; border: 8px solid rgba(37, 99, 235, 0.3); } QPushButton:hover { background-color: #1D4ED8; } QPushButton:disabled { background-color: #059669; border: 8px solid rgba(5, 150, 105, 0.3); color: white; font-size: 20px; }")
    if hasattr(window, 'lbl_check_in_msg'):
        window.lbl_check_in_msg.setStyleSheet("color: #475569; font-size: 15px; border: none; margin-top: 15px;")

    # ================================================================
    # 9. 🔹 快捷/签到区域标题标签
    # ================================================================
    for attr in ['lbl_quick', 'lbl_punch']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet("color: #1E293B; font-size: 18px; font-weight: bold; border: none;")

    # ================================================================
    # 10. ⏱️ 状态指示标签（检测耗时/目标数/FPS）
    # ================================================================
    status_label_style = "background-color: #F8FAFC; border: 1px solid #D1D5DB; border-radius: 8px; padding: 8px 15px; color: #2563EB; font-weight: bold; font-size: 15px;"
    for attr in ['label_time_image', 'label_targets_image', 'label_fps_video', 'label_targets_video']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(status_label_style)

    # ================================================================
    # 11. 🔵 置信度标签
    # ================================================================
    conf_label_light = "color: #475569; font-weight: bold; font-size: 15px; border: none;"
    for attr in ['label_conf_image', 'label_conf_video', 'label_conf_rt']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(conf_label_light)

    # ================================================================
    # 12. ⚙️ 系统设置 — 默认置信度数值
    # ================================================================
    if hasattr(window, 'lbl_default_conf_val'):
        window.lbl_default_conf_val.setStyleSheet("color: #2563EB; font-weight: bold; font-size: 16px;")

    # ================================================================
    # 13. 📂 浏览路径按钮
    # ================================================================
    if hasattr(window, 'btn_browse_path'):
        window.btn_browse_path.setStyleSheet(
            "QPushButton { background-color: #F1F5F9; color: #1E293B; border: 1px solid #D1D5DB; border-radius: 4px; padding: 8px 15px; font-weight:bold; } QPushButton:hover { background-color: #E2E8F0; }")

    # ================================================================
    # 14. 🔍 搜索/操作按钮（primary: blue）
    # ================================================================
    primary_btn = "QPushButton { background-color: #2563EB; color: white; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 15px; min-height: 28px;} QPushButton:hover { background-color: #1D4ED8; }"
    for attr in ['btn_search_history', 'btn_search_global', 'btn_search_user', 'btn_search_att', 'btn_upload_image', 'btn_upload_video']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(primary_btn)

    # ================================================================
    # 15. 🔄 重置/次要按钮（secondary: light gray）
    # ================================================================
    secondary_btn = "QPushButton { background-color: #F1F5F9; color: #1E293B; border: 1px solid #D1D5DB; border-radius: 6px; padding: 6px 15px; font-weight: bold; font-size: 15px; margin-left: 10px; min-height: 28px;} QPushButton:hover { background-color: #E2E8F0; }"
    for attr in ['btn_reset_history', 'btn_reset_global', 'btn_reset_user']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(secondary_btn)

    # ================================================================
    # 16. ➕ 新增用户按钮（绿色）
    # ================================================================
    if hasattr(window, 'btn_add_user_dialog'):
        window.btn_add_user_dialog.setStyleSheet(
            "QPushButton { background-color: #059669; color: white; border-radius: 6px; font-weight: bold; font-size: 15px;} QPushButton:hover { background-color: #047857; }")

    # ================================================================
    # 17. 🎨 系统设置保存按钮
    # ================================================================
    if hasattr(window, 'btn_save_system'):
        window.btn_save_system.setStyleSheet(
            "QPushButton { background-color: #2563EB; color: white; border-radius: 8px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #1D4ED8; }")

    # ================================================================
    # 18. 🤖 AI 聊天区域
    # ================================================================
    if hasattr(window, 'chat_display'):
        window.chat_display.setStyleSheet(
            "QTextBrowser { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 12px; padding: 25px; font-size: 16px; color: #334155; }")
    if hasattr(window, 'input_chat'):
        window.input_chat.setStyleSheet(
            "QLineEdit { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 25px; padding: 10px 25px; font-size: 16px; color: #1E293B; } QLineEdit:focus { border: 1px solid #2563EB; }")
    if hasattr(window, 'btn_send_chat'):
        window.btn_send_chat.setStyleSheet(
            "QPushButton { background-color: #2563EB; color: white; border-radius: 25px; font-weight: bold; font-size: 16px; } QPushButton:hover { background-color: #1D4ED8; }")

    # ================================================================
    # 19. 📡 通道面板
    # ================================================================
    if hasattr(window, 'channel_panel'):
        window.channel_panel.setStyleSheet("background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 12px;")
    if hasattr(window, 'lbl_ch_title'):
        window.lbl_ch_title.setStyleSheet("color: #1E293B; font-size: 18px; font-weight: bold; border: none;")
    if hasattr(window, 'input_rtsp'):
        window.input_rtsp.setStyleSheet("QLineEdit { background-color: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; padding: 8px; font-size: 14px; color: #1E293B; }")
    if hasattr(window, 'btn_browse_rt'):
        window.btn_browse_rt.setStyleSheet("QPushButton { background-color: #F1F5F9; color: #1E293B; border-radius: 6px; padding: 8px; font-weight:bold; border: 1px solid #D1D5DB; } QPushButton:hover { background-color: #E2E8F0; }")
    if hasattr(window, 'btn_add_rt'):
        window.btn_add_rt.setStyleSheet("QPushButton { background-color: #2563EB; color: white; border-radius: 6px; padding: 8px; font-weight:bold; } QPushButton:hover { background-color: #1D4ED8; }")
    if hasattr(window, 'btn_remove_rt'):
        window.btn_remove_rt.setStyleSheet("QPushButton { background-color: transparent; border: 1px solid #DC2626; color: #DC2626; border-radius: 6px; padding: 8px; font-weight:bold; } QPushButton:hover { background-color: #FEE2E2; color: #DC2626; }")
    if hasattr(window, 'btn_start_cams'):
        window.btn_start_cams.setStyleSheet("QPushButton { background-color: #059669; color: white; border-radius: 6px; padding: 12px; font-weight:bold; font-size: 16px; } QPushButton:hover { background-color: #047857; }")
    if hasattr(window, 'btn_stop_cams'):
        window.btn_stop_cams.setStyleSheet("QPushButton { background-color: #DC2626; color: white; border-radius: 6px; padding: 12px; font-weight:bold; font-size: 16px; } QPushButton:hover { background-color: #B91C1C; }")
    if hasattr(window, 'list_channels'):
        window.list_channels.setStyleSheet("background-color: #FFFFFF; color: #1E293B; border-radius: 6px; padding: 5px; font-size: 14px; border: 1px solid #D1D5DB;")

    # ================================================================
    # 20. 👤 个人中心
    # ================================================================
    if hasattr(window, 'lbl_avatar'):
        window.lbl_avatar.setStyleSheet("font-size: 80px; background-color: #F1F5F9; border-radius: 60px; padding: 20px;")
    if hasattr(window, 'lbl_profile_name'):
        window.lbl_profile_name.setStyleSheet("color: #1E293B; font-size: 22px; font-weight: bold; margin-top: 15px; border: none;")
    # 角色标签（状态色保持）
    if hasattr(window, 'lbl_profile_role'):
        window.lbl_profile_role.setStyleSheet("color: #D97706; font-size: 14px; font-weight: bold; background-color: rgba(217, 119, 6, 0.1); border-radius: 6px; padding: 5px;")
    # 登录信息
    info_light = "color: #64748B; font-size: 14px; border: none;"
    for attr in ['lbl_login_time', 'lbl_login_ip']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(info_light)
    # 考勤/拦截统计
    if hasattr(window, 'lbl_checkin_status'):
        window.lbl_checkin_status.setStyleSheet("color: #059669; font-size: 18px; font-weight: bold; background-color: rgba(5, 150, 105, 0.1); padding: 15px; border-radius: 8px;")
    if hasattr(window, 'lbl_attendance_days'):
        window.lbl_attendance_days.setStyleSheet("color: #475569; font-size: 16px; margin-top: 10px;")
    if hasattr(window, 'lbl_personal_intercept'):
        window.lbl_personal_intercept.setStyleSheet("color: #2563EB; font-size: 16px; margin-top: 10px;")
    # 注销按钮
    if hasattr(window, 'btn_logout'):
        window.btn_logout.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #DC2626; color: #DC2626; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 15px; } QPushButton:hover { background-color: #FEE2E2; color: #DC2626; }")
    if hasattr(window, 'btn_admin_logout'):
        window.btn_admin_logout.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #DC2626; color: #DC2626; border-radius: 6px; font-weight: bold; font-size: 18px; } QPushButton:hover { background-color: #FEE2E2; color: #DC2626; }")
    # 管理端个人注销
    if hasattr(window, 'btn_profile_logout'):
        window.btn_profile_logout.setStyleSheet("QPushButton { background-color: transparent; border: 2px solid #DC2626; color: #DC2626; border-radius: 6px; padding: 12px; font-weight: bold; font-size: 15px; } QPushButton:hover { background-color: #FEE2E2; color: #DC2626; }")

    # ================================================================
    # 21. 🔐 安全设置区（修改密码/邮箱）
    # ================================================================
    section_title_light = "color: #1E293B; font-size: 18px; font-weight: bold; border: none;"
    for attr in ['lbl_sec_title', 'lbl_email_title', 'lbl_theme_title']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(section_title_light)

    form_label_light = "color: #475569; font-size: 15px; border: none;"
    for attr in ['lbl_old', 'lbl_new', 'lbl_email', 'lbl_theme']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(form_label_light)

    # 安全设置按钮
    secure_btn = "QPushButton { background-color: #2563EB; color: white; border-radius: 6px; padding: 10px; font-weight: bold; font-size: 16px; margin-top: 5px;} QPushButton:hover { background-color: #1D4ED8; }"
    for attr in ['btn_save_pwd', 'btn_save_email', 'btn_apply_theme']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(secure_btn)

    # ================================================================
    # 22. ➖ 分割线
    # ================================================================
    line_light = "background-color: #E2E8F0; margin-top: 25px; margin-bottom: 25px;"
    # 查找所有 line 和 line2（通过 try/except 或者 hasattr 无法直接判断 line 对象）
    # 改用通用方法：动态查找 window 中所有 QFrame 子控件
    _apply_line_overrides(window, line_light)

    # ================================================================
    # 23. 📅 筛选标签（管理端历史/考勤等）
    # ================================================================
    filter_label_light = "color: #475569; font-size: 15px; font-weight: bold; border: none;"
    for attr in ['label_filter_date', 'label_filter_event', 'label_filter_operator', 'lbl_att_date']:
        if hasattr(window, attr):
            getattr(window, attr).setStyleSheet(filter_label_light)


def _apply_line_overrides(window, line_style):
    """查找窗口中的 QFrame 分割线并应用样式（避免依赖特定对象名）"""
    # 尝试已知的分割线对象名
    for attr_name in ['line', 'line2']:
        if hasattr(window, attr_name):
            obj = getattr(window, attr_name)
            if hasattr(obj, 'setStyleSheet'):
                obj.setStyleSheet(line_style)
