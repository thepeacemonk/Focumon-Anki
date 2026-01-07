from aqt.qt import *

class StatsDialog(QDialog):
    def __init__(self, stats_data, parent=None):
        super().__init__(parent)
        self.stats_data = stats_data
        self.setWindowTitle("Focumon Stats")
        self.resize(400, 420)
        self.setup_ui()
    
    def setup_ui(self):
        from . import font_utils
        from aqt import mw
        
        # Detect theme
        is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
        
        # Color scheme (matching deck_widget.py palette)
        bg_color = "#242424" if is_dark else "#FAF8F2"
        text_color = "#FAF8F2" if is_dark else "#242424"
        text_secondary = "#AAAAAA" if is_dark else "#666666"
        accent_color = "#FFDD19"
        stat_bg = "#202020" if is_dark else "#E3E2DC"
        progress_bg = "#3A3A3A" if is_dark else "#E5E5EA"
        
        # Get font-face CSS
        # Load font into QFontDatabase
        font_family = font_utils.load_custom_font()
        
        self.setStyleSheet(f"""
            
            QDialog {{
                background-color: {bg_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }}
            QLabel {{
                color: {text_color};
            }}
            QLabel#title {{
                font-size: 20px;
                font-weight: normal;
                color: {text_color};
                padding: 0px 10px 0 10px;
                min-height: 30px;
                font-family: '{font_family}', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel#username {{
                font-size: 14px;
                color: {text_secondary};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel#statLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {text_color};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QLabel#statValue {{
                font-size: 12px;
                font-weight: normal;
                color: #D1D0D0;
                background-color: #2E282A;
                border-radius: 8px;
                padding: 5px 10px;
                font-family: '{font_family}', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QProgressBar {{
                border: none;
                border-radius: 6px;
                background-color: {progress_bg};
                height: 12px;
                text-align: center;
                color: {text_color};
            }}
            QProgressBar::chunk {{
                background-color: {accent_color};
                border-radius: 6px;
            }}
            QPushButton {{
                background-color: {accent_color};
                color: #000000;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            QPushButton:hover {{
                background-color: #FFE84D;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(2)
        
        
        # Title
        title = QLabel("Focumon Stats")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username
        username = self.stats_data.get('username', '')
        if username:
            username_label = QLabel(f"@{username}")
            username_label.setObjectName("username")
            username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(username_label)
        
        layout.addSpacing(14)
        
        # Sprites (Trainer and Focumon side by side with overlap)
        if 'trainer_sprite_data' in self.stats_data or 'focumon_sprite_data' in self.stats_data:
            sprite_container = QWidget()
            sprite_container.setFixedHeight(150)
            sprite_container.setStyleSheet("background: transparent;")
            
            # Create a layout that allows positioning
            sprite_layout = QHBoxLayout(sprite_container)
            sprite_layout.setContentsMargins(0, 0, 0, 0)
            sprite_layout.setSpacing(0)
            sprite_layout.addStretch()
            
            # Container for both sprites with overlap
            sprites_widget = QWidget()
            sprites_widget.setFixedSize(240, 150)  # Increased size to prevent clipping
            
            # Trainer sprite
            if 'trainer_sprite_data' in self.stats_data:
                trainer_label = QLabel(sprites_widget)
                pixmap = QPixmap()
                if pixmap.loadFromData(self.stats_data['trainer_sprite_data']):
                    # Use actual size (128x128) for pixelated look
                    scaled = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
                    trainer_label.setPixmap(scaled)
                    trainer_label.setGeometry(10, 10, 128, 128)  # Position at left with margin
            
            # Focumon sprite (overlapping)
            if 'focumon_sprite_data' in self.stats_data:
                focumon_label = QLabel(sprites_widget)
                pixmap = QPixmap()
                if pixmap.loadFromData(self.stats_data['focumon_sprite_data']):
                    # Use actual size (128x128) for pixelated look
                    scaled = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
                    focumon_label.setPixmap(scaled)
                    focumon_label.setGeometry(90, 10, 128, 128)  # Overlap by positioning to the right
            
            sprite_layout.addWidget(sprites_widget)
            sprite_layout.addStretch()
            
            layout.addWidget(sprite_container)
        
        layout.addSpacing(10)
        
        # Trainer Level
        if 'trainer_level' in self.stats_data:
            self._add_stat_row(layout, "Trainer Level", f"LV.{self.stats_data['trainer_level']}")
            layout.addSpacing(8)
        
        # Focumon Level
        if 'focumon_level' in self.stats_data:
            self._add_stat_row(layout, "Focumon Level", f"LV.{self.stats_data['focumon_level']}")
            layout.addSpacing(8)
        
        # Focumon Name
        if 'focumon_name' in self.stats_data:
            self._add_stat_row(layout, "Current Focumon", self.stats_data['focumon_name'])
            layout.addSpacing(8)
        
        layout.addSpacing(10)
        
        # Focudex Progress with progress bar (if available)
        if 'focudex_progress' in self.stats_data:
            self._add_progress_stat(layout, "Focudex Progress", self.stats_data['focudex_progress'])
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def _add_stat_row(self, layout, label_text, value_text):
        """Add a simple label/value row"""
        row = QHBoxLayout()
        
        label = QLabel(label_text)
        label.setObjectName("statLabel")
        
        value = QLabel(value_text)
        value.setObjectName("statValue")
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)
        layout.addLayout(row)



    def _add_progress_stat(self, layout, label_text, value_text):
        """Add a stat with progress bar (e.g., '50/100')"""
        # Label
        label = QLabel(label_text)
        label.setObjectName("statLabel")
        layout.addWidget(label)
        
        # Parse value like "50/100" or "273/360"
        try:
            parts = value_text.split('/')
            if len(parts) == 2:
                current = int(parts[0])
                maximum = int(parts[1])
                
                # Progress bar
                progress = QProgressBar()
                progress.setMinimum(0)
                progress.setMaximum(maximum)
                progress.setValue(current)
                progress.setFormat(f"{current}/{maximum}")
                layout.addWidget(progress)
            else:
                # Fallback to simple display
                value = QLabel(value_text)
                value.setObjectName("statValue")
                layout.addWidget(value)
        except:
            # Fallback to simple display
            value = QLabel(value_text)
            value.setObjectName("statValue")
            layout.addWidget(value)
        
        layout.addSpacing(8)
