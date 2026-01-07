from aqt import mw
from aqt.qt import *
import os
from . import font_utils

class FocumonInfoDialog(QDialog):
    """
    Custom replacement for aqt.utils.showInfo with Focumon styling.
    """
    def __init__(self, text, title="Focumon", parent=None, type="info"):
        super().__init__(parent or mw)
        self.setWindowTitle("Focumon")  # Simplified Window Title
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint) # Remove ? button
        self.setMinimumWidth(380)
        self.setMaximumWidth(550)
        
        self.text_content = text
        self.title_content = title
        self.dialog_type = type
        
        # Load fonts
        self.title_font = font_utils.load_custom_font("Silkscreen-Regular.ttf")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Modern Color Palette
        if is_dark:
            bg_color = "#242424"
            text_color = "#E0E0E0"
            subtle_text = "#AAAAAA"
            btn_bg = "#FFDD19"
            btn_text = "#242424"
            btn_hover = "#FFE54D"
            border_color = "#3A3A3A"
        else:
            bg_color = "#FAF8F2"
            text_color = "#242424"
            subtle_text = "#5A5A5A"
            btn_bg = "#FFDD19"
            btn_text = "#242424"
            btn_hover = "#FFE54D"
            border_color = "#E0E0E0"

        # Stylesheet
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
            QLabel {{
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel#title {{
                font-family: '{self.title_font}', monospace;
                font-size: 20px;
                color: {text_color};
                margin-bottom: 12px;
                letter-spacing: -0.5px;
            }}
            QLabel#message {{
                font-size: 14px;
                line-height: 1.5;
                color: {text_color};
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: none;
                border-radius: 18px; /* Pill shape */
                padding: 8px 32px;
                font-size: 14px;
                font-weight: 700;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
            }}
            QPushButton:pressed {{
                background-color: #E6C700;
                padding-top: 9px; /* Pressed effect */
                padding-bottom: 7px;
            }}
            QPushButton:focus {{
                outline: none;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(35, 20, 35, 25)
        layout.setSpacing(0)
        layout.addStretch()
        # Helper to load image
        addon_dir = os.path.dirname(__file__)
        img_path = os.path.join(addon_dir, "focumon_fam.png")
        if os.path.exists(img_path):
            img_label = QLabel()
            
            # High DPI Scaling Logic
            pixmap = QPixmap(img_path)
            pixel_ratio = self.devicePixelRatioF()
            target_width = 100
            
            # Scale to (target_width * pixel_ratio)
            scaled_w = int(target_width * pixel_ratio)
            scaled_pixmap = pixmap.scaledToWidth(scaled_w, Qt.TransformationMode.SmoothTransformation)
            
            # Set device pixel ratio so it renders at logical size
            scaled_pixmap.setDevicePixelRatio(pixel_ratio)
            
            img_label.setPixmap(scaled_pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)
            
        layout.addSpacing(5)

        
        # Title
        title_label = QLabel(self.title_content.upper()) # Uppercase for that retro feel if desired, or keep generic
        title_label.setObjectName("title")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(15)
        
        # Divider (Optional, let's keep it clean without for now, or just spacing)
        
        # Message
        msg_label = QLabel(self.text_content)
        msg_label.setObjectName("message")
        msg_label.setWordWrap(True)
        msg_label.setTextFormat(Qt.TextFormat.RichText)
        msg_label.setOpenExternalLinks(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center text for modern feel
        layout.addWidget(msg_label)
        
        layout.addSpacing(5)
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch() # Center button
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

def show_custom_info(text, title="Focumon", parent=None, type="info"):
    """
    Helper to show the custom dialog.
    """
    d = FocumonInfoDialog(text, title, parent, type)
    d.exec()
