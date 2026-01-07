from aqt import mw
from aqt.qt import *
import os
from . import font_utils
from .main import FocumonWindow

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Focumon Instructions")
        self.setMinimumWidth(550)
        self.setMinimumHeight(600)
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
            subtle_text = "#AAAAAA"
            btn_bg = "#FFDD19"
            btn_text = "#242424"
            btn_hover = "#FFE54D"
            section_bg = "#2C2C2C"
        else:
            bg_color = "#FAF8F2"
            text_color = "#242424"
            subtle_text = "#5A5A5A"
            btn_bg = "#FFDD19"
            btn_text = "#242424"
            btn_hover = "#FFE54D"
            section_bg = "#FFFFFF"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
            }}
            QLabel {{
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                line-height: 1.5;
            }}
            QLabel.h1 {{
                font-family: '{self.title_font}', monospace;
                font-size: 20px;
                color: {text_color};
                margin-bottom: 15px;
            }}
            QLabel.h2 {{
                font-family: '{self.title_font}', monospace;
                font-size: 16px;
                color: {text_color};
                margin-top: 0px;
                margin-bottom: 8px;
            }}
            QLabel.body {{
                font-size: 14px;
                color: {text_color};
            }}
            QFrame.section {{
                background-color: {section_bg};
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
            }}
            QPushButton {{
                background-color: {btn_bg};
                color: {btn_text};
                border: 1px solid {btn_bg};
                border-radius: 20px; /* Pill shape */
                padding: 0px 24px;
                font-size: 14px;
                font-weight: 700;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 40px;
                max-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                border-color: {btn_hover};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QWidget#scrollContent {{
                background-color: transparent;
            }}
        """)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_widget.setObjectName("scrollContent")
        scroll_layout = QVBoxLayout(content_widget)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_layout.setSpacing(20)
        
        # Title
        title = QLabel("Instructions")
        title.setProperty("class", "h1")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(title)
        
        # 1. First Steps
        first_steps_frame = QFrame()
        first_steps_frame.setProperty("class", "section")
        fs_layout = QVBoxLayout(first_steps_frame)
        
        fs_title = QLabel("First Steps")
        fs_title.setProperty("class", "h2")
        fs_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fs_layout.addWidget(fs_title)
        
        # HTML text for link
        # "Login process (preferably email...) and User pairing..."
        # Link: create your account here ... (link hidden on here)
        
        link_color = "#FFDD19" if is_dark else "#DAA520" # Visible link color
        
        fs_text = QLabel()
        fs_text.setProperty("class", "body")
        fs_text.setWordWrap(True)
        fs_text.setTextFormat(Qt.TextFormat.RichText)
        # Using a custom protocol or just anchor to catch click
        fs_text.setText(f"""
        <p><b>Login Process:</b> Log in using your email for a smoother experience. 
        Create your account <a href="focumon:login" style="color: {link_color}; text-decoration: underline;">here</a> (using my invitation 😆).</p>
        
        <p><b>User Pairing:</b> Go to <i>Tools &gt; Focumon &gt; Settings</i> (or click the Profile icon) and enter your username to sync your stats.</p>
        """)
        fs_text.linkActivated.connect(self.handle_link)
        fs_layout.addWidget(fs_text)
        
        scroll_layout.addWidget(first_steps_frame)
        
        # 2. Functions
        funcs_frame = QFrame()
        funcs_frame.setProperty("class", "section")
        f_layout = QVBoxLayout(funcs_frame)
        
        f_title = QLabel("Menu Functions")
        f_title.setProperty("class", "h2")
        f_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f_layout.addWidget(f_title)
        
        f_text = QLabel("""
        <ul>
        <li><b>Deck Widget:</b> View your current Focumon and progress directly on the Decks screen.</li>
        <li><b>Profile:</b> View detailed stats and Focudex.</li>
        <li><b>Refresh:</b> Reload the add-on if you encounter visual glitches.</li>
        <li><b>Instruction:</b> Open this guide again.</li>
        </ul>
        """)
        f_text.setProperty("class", "body")
        f_text.setWordWrap(True)
        f_layout.addWidget(f_text)
        
        scroll_layout.addWidget(funcs_frame)
        
        # 3. Tutorial Button
        tut_frame = QFrame()
        tut_frame.setProperty("class", "section")
        t_layout = QVBoxLayout(tut_frame)
        
        t_title = QLabel("Tutorial")
        t_title.setProperty("class", "h2")
        t_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t_layout.addWidget(t_title)
        
        t_btn = QPushButton("How to use Focumon")
        t_btn.setObjectName("actionBtn")
        t_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        t_btn.clicked.connect(self.open_tutorial)
        t_layout.addWidget(t_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        scroll_layout.addWidget(tut_frame)
        
        scroll_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Close button at bottom
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(20, 10, 20, 20)
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("actionBtn") # Reuse style
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(close_btn)
        bottom_layout.addStretch()
        
        main_layout.addWidget(bottom_bar)
        
        self.setLayout(main_layout)

    def handle_link(self, url):
        if url == "focumon:login":
            # Open Focumon Window to the specific URL requested
            self.open_browser("https://www.focumon.com/trainers/PeaceMonk")
        else:
            QDesktopServices.openUrl(QUrl(url))

    def open_tutorial(self):
        self.open_browser("https://www.focumon.com/about")

    def open_browser(self, target_url):
        # Open in add-on browser window
        if not hasattr(mw, "focumon_window"):
            mw.focumon_window = FocumonWindow(mw)
        
        mw.focumon_window.show()
        mw.focumon_window.activateWindow()
        
        # Navigate to URL
        if hasattr(mw.focumon_window, "browser"):
            mw.focumon_window.browser.setUrl(QUrl(target_url))
