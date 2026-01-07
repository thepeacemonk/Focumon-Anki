from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
import os

class ToggleSwitch(QCheckBox):
    """Custom animated toggle switch widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Animation state
        self._position = 0.0
        self._animation = QVariantAnimation(self)
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._animation.valueChanged.connect(self._handle_animation_value)
        
    def _handle_animation_value(self, value):
        self._position = value
        self.update()
        
    def setChecked(self, checked):
        super().setChecked(checked)
        # Snap to target state if not validating interaction
        target = 1.0 if checked else 0.0
        if self._animation.state() == QAbstractAnimation.State.Stopped:
             self._position = target
             self.update()

    def mousePressEvent(self, event):
        # Toggle and animate
        new_state = not self.isChecked()
        super().setChecked(new_state)
        
        self._animation.stop()
        self._animation.setStartValue(self._position)
        self._animation.setEndValue(1.0 if new_state else 0.0)
        self._animation.start()
        event.accept()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Define base colors
        if is_dark:
            off_color = QColor("#3A3A3A")
        else:
            off_color = QColor("#CCCCCC")
        on_color = QColor("#FFDD19")
        
        # Interpolate color based on position
        t = self._position
        
        r = off_color.red() + (on_color.red() - off_color.red()) * t
        g = off_color.green() + (on_color.green() - off_color.green()) * t
        b = off_color.blue() + (on_color.blue() - off_color.blue()) * t
        track_color = QColor(int(r), int(g), int(b))
        
        # Draw track
        track_rect = QRectF(0, 0, 44, 24)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, 12, 12)
        
        # Draw thumb
        thumb_range = 44 - 20 - 4 # width - thumb_size - padding*2
        thumb_x = 2 + (thumb_range * t)
        thumb_rect = QRectF(thumb_x, 2, 20, 20)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(thumb_rect)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Focumon Settings")
        self.setMinimumSize(500, 400)
        
        # Load custom font
        self.load_custom_font()
        
        self.setup_ui()
        self.load_settings()

    def load_custom_font(self):
        """Load the Silkscreen-Regular font"""
        addon_dir = os.path.dirname(__file__)
        self.font_path = os.path.join(addon_dir, "assets", "Silkscreen-Regular.ttf")
        
        if os.path.exists(self.font_path):
            font_id = QFontDatabase.addApplicationFont(self.font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                self.custom_font_family = families[0] if families else "Arial"
            else:
                self.custom_font_family = "Arial"
        else:
            self.custom_font_family = "Arial"

    def setup_ui(self):
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Color scheme (matching deck_widget.py palette)
        bg_color = "#242424" if is_dark else "#FAF8F2"
        text_color = "#FAF8F2" if is_dark else "#242424"
        accent_color = "#FFDD19"
        stat_bg = "#202020" if is_dark else "#E3E2DC"
        input_bg = "#1A1A1A" if is_dark else "#FFFFFF"
        input_border = "#3A3A3A" if is_dark else "#CCCCCC"
        
        # Get font name
        font_family = self.custom_font_family
        
        # Modern Stylesheet - FE5Cent only for titles and buttons
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
            QLabel {{
                font-size: 14px;
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel.section-title {{
                font-size: 16px;
                font-weight: 600;
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                padding: 4px 0px;
            }}
            QLabel.description {{
                font-size: 13px;
                color: {text_color};
                opacity: 0.8;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QPushButton {{
                background-color: {stat_bg};
                color: {text_color};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QPushButton:hover {{
                background-color: {"#2A2A2A" if is_dark else "#D5D4CE"};
            }}
            QPushButton:pressed {{
                background-color: {"#1A1A1A" if is_dark else "#C5C4BE"};
            }}
            QPushButton#reportBtn {{
                background-color: {"#3A3A3A" if is_dark else "#E0E0E0"};
                color: {"#FFFFFF" if is_dark else "#000000"};
                border-radius: 18px;
                padding: 0px 16px;
                font-size: 13px;
                font-weight: 600;
                min-height: 36px;
                max-height: 36px;
            }}
            QPushButton#reportBtn:hover {{
                background-color: {"#4A4A4A" if is_dark else "#D0D0D0"};
            }}
            QPushButton#donateBtn {{
                background-color: #FFDD19;
                color: #000000;
                border: none;
                border-radius: 18px;
                padding: 0px 16px;
                font-size: 13px;
                font-weight: 600;
                min-height: 36px;
                max-height: 36px;
            }}
            QPushButton#donateBtn:hover {{
                background-color: #FFE84D;
            }}
            QPushButton#saveBtn {{
                background-color: {accent_color};
                color: #000000;
            }}
            QPushButton#saveBtn:hover {{
                background-color: #FFE84D;
            }}
            QPushButton#saveBtn:pressed {{
                background-color: #E6C700;
            }}
            QLineEdit {{
                border: 1px solid {input_border};
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                background-color: {input_bg};
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLineEdit:focus {{
                border-color: {accent_color};
                outline: none;
            }}
            QFrame#username-container {{
                background-color: {stat_bg};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(32, 32, 32, 32)
        # Header Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        header_layout.addStretch()  # Add stretch to center

        # Report Bug Button
        report_btn = QPushButton("Report Bug")
        report_btn.setObjectName("reportBtn")
        report_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        report_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/thepeacemonk/Focumon-Anki")))
        report_btn.setFixedSize(120, 36)
        header_layout.addWidget(report_btn)

        # Focumon Logo (Centered)
        logo_label = QLabel()
        addon_dir = os.path.dirname(__file__)
        logo_path = os.path.join(addon_dir, "focumon.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            
            # High DPI Scaling Logic
            pixel_ratio = self.devicePixelRatioF()
            target_height = 24
            
            # Scale to (target_height * pixel_ratio)
            scaled_h = int(target_height * pixel_ratio)
            scaled_pixmap = pixmap.scaledToHeight(scaled_h, Qt.TransformationMode.SmoothTransformation)
            
            # Set device pixel ratio
            scaled_pixmap.setDevicePixelRatio(pixel_ratio)
            
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        # Donate Button
        donate_btn = QPushButton("Donate")
        donate_btn.setObjectName("donateBtn")
        donate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        donate_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://studio.buymeacoffee.com/dashboard")))
        donate_btn.setFixedSize(100, 36)
        header_layout.addWidget(donate_btn)
        
        header_layout.addStretch()  # Add stretch to center

        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)

        # Main Title - Using QFont directly for no clipping
        title = QLabel("Configuration")
        title_font = QFont(self.custom_font_family, 22, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {text_color}; padding-bottom: 0px; font-family: '{self.custom_font_family}';")
        title.setMinimumHeight(35)  # Prevent clipping
        main_layout.addWidget(title)
        
        main_layout.addSpacing(8)  # Small space after title

        # Always on Top Section
        always_on_top_layout = QHBoxLayout()
        always_on_top_layout.setSpacing(12)
        
        always_on_top_label = QLabel("Always on Top")
        always_on_top_label.setProperty("class", "section-title")
        always_on_top_label.setMinimumHeight(28)  # Prevent clipping
        
        self.always_on_top_toggle = ToggleSwitch()
        self.always_on_top_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        
        always_on_top_layout.addWidget(always_on_top_label)
        always_on_top_layout.addStretch()
        always_on_top_layout.addWidget(self.always_on_top_toggle)
        
        main_layout.addLayout(always_on_top_layout)

        # Hide Widget Section
        hide_widget_layout = QHBoxLayout()
        hide_widget_layout.setSpacing(12)
        
        hide_widget_label = QLabel("Hide Widget")
        hide_widget_label.setProperty("class", "section-title")
        hide_widget_label.setMinimumHeight(28)
        
        self.hide_widget_toggle = ToggleSwitch()
        self.hide_widget_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        
        hide_widget_layout.addWidget(hide_widget_label)
        hide_widget_layout.addStretch()
        hide_widget_layout.addWidget(self.hide_widget_toggle)
        
        main_layout.addLayout(hide_widget_layout)
        
        main_layout.addSpacing(16)
        
        # Sync Stats Section (Centralized and Modern)
        sync_section = QFrame()
        sync_section.setObjectName("username-container")
        
        sync_layout = QVBoxLayout(sync_section)
        sync_layout.setContentsMargins(0, 0, 0, 0)
        sync_layout.setSpacing(12)
        
        # Section title
        sync_title = QLabel("Profile")
        sync_title_font = QFont(self.custom_font_family, 16, QFont.Weight.Bold)
        sync_title.setFont(sync_title_font)
        sync_title.setStyleSheet(f"color: {text_color}; padding: 0px; font-family: '{self.custom_font_family}';")
        sync_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sync_title.setMinimumHeight(24)  # Prevent clipping
        sync_layout.addWidget(sync_title)
        
        # Description
        sync_desc = QLabel("Check your username on Focumon's Profile and hover over your character.")
        sync_desc.setProperty("class", "description")
        sync_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sync_layout.addWidget(sync_desc)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g., FocumonUser")
        self.username_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_input.setMinimumHeight(40)
        sync_layout.addWidget(self.username_input)
        
        main_layout.addWidget(sync_section)
        
        # Spacer to push buttons to bottom
        main_layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setMinimumHeight(40)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        self.save_btn.setMinimumHeight(40)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def load_settings(self):
        config = mw.addonManager.getConfig(__name__)
        if config:
            self.always_on_top_toggle.setChecked(config.get("always_on_top", False))
            self.hide_widget_toggle.setChecked(config.get("hide_deck_widget", False))
            self.username_input.setText(config.get("focumon_username", ""))

    def save_settings(self):
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            config = {}
        
        config["always_on_top"] = self.always_on_top_toggle.isChecked()
        config["hide_deck_widget"] = self.hide_widget_toggle.isChecked()
        config["focumon_username"] = self.username_input.text().strip()
        mw.addonManager.writeConfig(__name__, config)
        
        # If the window is open, update it
        if hasattr(mw, "focumon_window") and mw.focumon_window.isVisible():
             # We need to restart the window to apply window flags
             current_url = mw.focumon_window.browser.url()
             mw.focumon_window.close()
             # The closeEvent hides it, but here we actually want to re-init or re-show with new flags
             # Since re-initing might be complex with keeping state, for now we will just show a message 
             # or simply let the user know they might need to reopen.
             # Actually, simpler: prompt a restart of the window or just let the next open handle it.
             pass
             
        self.accept()
