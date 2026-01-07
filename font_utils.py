
import os
import base64
from aqt.qt import QFontDatabase, QApplication


def load_custom_font(font_name="Silkscreen-Regular.ttf"):
    """Load a custom font into QFontDatabase and return the family name."""
    font_path = os.path.join(os.path.dirname(__file__), "assets", font_name)
    
    if not os.path.exists(font_path):
        return "sans-serif"
        
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            return families[0]
    
    return "sans-serif"


def get_font_base64(font_name="Silkscreen-Regular.ttf"):
    """Load a custom font and return as base64-encoded string for CSS embedding."""
    font_path = os.path.join(os.path.dirname(__file__), "assets", font_name)
    
    try:
        with open(font_path, 'rb') as f:
            font_data = f.read()
        return base64.b64encode(font_data).decode('utf-8')
    except FileNotFoundError:
        # Return None if font file is not found
        return None

def get_font_face_css():
    """Generate @font-face CSS rules for Focumon fonts."""
    css = ""
    
    # FE5Cent
    fe5_b64 = get_font_base64("FE5Cent-Regular.ttf")
    if fe5_b64:
        css += f"""
        @font-face {{
            font-family: 'FE5Cent';
            src: url(data:font/truetype;charset=utf-8;base64,{fe5_b64}) format('truetype');
            font-weight: normal;
            font-style: normal;
        }}
        """
        
    # Silkscreen
    silk_b64 = get_font_base64("Silkscreen-Regular.ttf")
    if silk_b64:
        css += f"""
        @font-face {{
            font-family: 'Silkscreen';
            src: url(data:font/truetype;charset=utf-8;base64,{silk_b64}) format('truetype');
            font-weight: normal;
            font-style: normal;
        }}
        """
        
    return css
