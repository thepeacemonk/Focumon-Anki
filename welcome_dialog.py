from aqt import mw
from aqt.qt import *
import os
from . import font_utils

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Welcome to Focumon")
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        
        # Load font
        self.title_font = font_utils.load_custom_font("Silkscreen-Regular.ttf")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Theme detection
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Colors
        if is_dark:
            bg_color = "#242424"
            text_color = "#E0E0E0"
            btn_bg = "#FFDD19"
            btn_text = "#242424"
            btn_hover = "#FFE54D"
        else:
            bg_color = "#FAF8F2"
            text_color = "#242424"
            btn_bg = "#FFDD19"
            btn_text = "#242424"
            btn_hover = "#FFE54D"

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
                font-size: 24px;
                color: {text_color};
                margin-top: 10px;
                margin-bottom: 5px; /* Reduced from 20px */
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: 1px solid {btn_bg};
                border-radius: 20px; /* Half of min-height (40px) for true pill */
                padding: 0px 40px;
                font-size: 16px;
                font-weight: 700;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 40px;
                max-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                border-color: {btn_hover};
            }}
            QCheckBox {{
                color: {text_color};
                spacing: 8px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 1. Logo Focumon.png
        addon_dir = os.path.dirname(__file__)
        logo_path = os.path.join(addon_dir, "Focumon.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            # Resize gracefully
            scaled = pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
            # Handle Retina
            scaled.setDevicePixelRatio(self.devicePixelRatioF())
            logo_label.setPixmap(scaled)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
            
            logo_width = scaled.width() / self.devicePixelRatioF()
            
            # 2. Image focumon_fam.png (Dynamic Width Matching)
            fam_path = os.path.join(addon_dir, "focumon_fam.png")
            if os.path.exists(fam_path):
                fam_label = QLabel()
                pixmap = QPixmap(fam_path)
                
                # Scale to match the logical width of the logo
                pixel_ratio = self.devicePixelRatioF()
                scaled_w = int(logo_width * pixel_ratio)
                
                scaled_fam = pixmap.scaledToWidth(scaled_w, Qt.TransformationMode.SmoothTransformation)
                scaled_fam.setDevicePixelRatio(pixel_ratio)
                
                fam_label.setPixmap(scaled_fam)
                fam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(fam_label)
            
        # 3. Title "Welcome to Focumon"
        title_label = QLabel("Welcome to Focumon")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # "for Anki" Badge
        badge_btn = QPushButton("for Anki")
        badge_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        badge_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://ankiweb.net/shared/info/")))
        badge_btn.setFixedWidth(120) # Small fixed width or let it size? "small phrase". 120 is fine.
        # Actually letting it autosize with padding is better, but centered.
        # To center a button in QVBoxLayout, we need to set alignment or put in a container.
        # layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignCenter)
        
        badge_style = f"""
            QPushButton {{
                background-color: #202020;
                color: #E0E0E0;
                border-radius: 15px;
                padding: 4px 15px;
                font-family: '{self.title_font}', monospace;
                font-size: 14px;
                border: 1px solid #202020;
            }}
            QPushButton:hover {{
                background-color: #202020; /* Keep background dark */
                color: {btn_bg}; /* Accent color */
                border: 1px solid {btn_bg}; /* Optional: show border accent */
            }}
        """
        badge_btn.setStyleSheet(badge_style)
        
        # We need a wrapper to center it if it doesn't stretch, or use alignment
        layout.addWidget(badge_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(6) 

        # Credits
        credits_container = QWidget()
        credits_layout = QVBoxLayout(credits_container)
        credits_layout.setContentsMargins(0, 0, 0, 0)
        credits_layout.setSpacing(0)
        credits_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Base text style
        label_style = f"font-size: 12px; color: {text_color}; border: none; background: transparent;"
        
        # Link button style
        link_style = f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {text_color};
                font-size: 12px;
                font-weight: bold;
                padding: 0;
                margin: 0;
                text-align: left;
            }}
            QPushButton:hover {{
                color: {btn_bg};
            }}
        """

        # Row 1: made by Milton, graphics by Yana
        row1 = QWidget()
        row1_layout = QHBoxLayout(row1)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setSpacing(3)
        row1_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        l1 = QLabel("made by")
        l1.setStyleSheet(label_style)
        row1_layout.addWidget(l1)

        b1 = QPushButton("Milton")
        b1.setCursor(Qt.CursorShape.PointingHandCursor)
        b1.setStyleSheet(link_style)
        b1.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://x.com/miltonxren")))
        row1_layout.addWidget(b1)

        l2 = QLabel(", graphics by")
        l2.setStyleSheet(label_style)
        row1_layout.addWidget(l2)

        b2 = QPushButton("Yana")
        b2.setCursor(Qt.CursorShape.PointingHandCursor)
        b2.setStyleSheet(link_style)
        b2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.yanakorpgs.com/")))
        row1_layout.addWidget(b2)
        
        credits_layout.addWidget(row1)

        # Row 2: powered by Peace on Anki
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(3)
        row2_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        l3 = QLabel("powered by")
        l3.setStyleSheet(label_style)
        row2_layout.addWidget(l3)

        b3 = QPushButton("✌️Peace")
        b3.setCursor(Qt.CursorShape.PointingHandCursor)
        b3.setStyleSheet(link_style)
        b3.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/thepeacemonk")))
        row2_layout.addWidget(b3)
        
        l4 = QLabel("on Anki")
        l4.setStyleSheet(label_style)
        row2_layout.addWidget(l4)

        credits_layout.addWidget(row2)
        
        layout.addWidget(credits_container)
        
        layout.addSpacing(10)
        
        # 4. Button "Start here"
        start_btn = QPushButton("Start here")
        start_btn.setObjectName("startBtn")
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.clicked.connect(self.on_start)
        layout.addWidget(start_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(20)
        
        # 5. "Don't show this again"
        self.dont_show_cb = QCheckBox("Don't show this again")
        self.dont_show_cb.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dont_show_cb.setChecked(False)  # Default off, user must opt-out
        
        # Modern Checkbox Styling
        cb_style = f"""
            QCheckBox {{
                color: {text_color};
                spacing: 10px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                font-size: 13px;
                opacity: 0.8;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {text_color};
                border-radius: 6px;
                background: transparent;
            }}
            QCheckBox::indicator:hover {{
                border-color: {btn_bg};
            }}
            QCheckBox::indicator:checked {{
                background-color: {btn_bg};
                border-color: {btn_bg};
                image: none; /* We can't easily inline an SVG without a path, but solid color is fine for modern look */
            }}
            /* Create a simple checkmark using a smaller inner box or just solid fill for now */
            QCheckBox::indicator:checked {{
                 /* Using a URL requires a file, let's use a simple distinct look: Filled yellow */
            }}
        """
        # A trick for a checkmark without an image is tricky in pure stylesheet without a file. 
        # But we can assume people know filled = checked. 
        # Or we can make it a "switch" looking thing.
        # Let's try to make it look like a rounded pill switch.
        
        switch_style = f"""
            QCheckBox {{
                color: {text_color};
                font-size: 12px;
                font-weight: 600;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 2px solid #888;
                background: transparent;
            }}
            QCheckBox::indicator:checked {{
                background-color: {btn_bg};
                border-color: {btn_bg};
            }}
            QCheckBox::indicator:hover {{
                border-color: {btn_bg};
            }}
        """
        self.dont_show_cb.setStyleSheet(switch_style)
        
        layout.addWidget(self.dont_show_cb, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
    def on_start(self):
        # Save preference
        config = mw.addonManager.getConfig(__name__)
        if config is None:
            config = {}
        
        if self.dont_show_cb.isChecked():
            config["show_welcome"] = False
            mw.addonManager.writeConfig(__name__, config)
            
        self.accept()
        
        # Open Instructions Modelessly
        from .instructions_dialog import InstructionsDialog
        if not hasattr(mw, "instructions_dialog") or not mw.instructions_dialog:
            mw.instructions_dialog = InstructionsDialog(mw)
        mw.instructions_dialog.show()
        mw.instructions_dialog.activateWindow()
        mw.instructions_dialog.raise_()
