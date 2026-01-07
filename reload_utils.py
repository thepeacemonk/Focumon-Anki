"""
Hot-reload utility for Focumon add-on development.
Allows reloading of modules without restarting Anki.
"""

from aqt import mw
from aqt.utils import showInfo
import importlib
import sys


def reload_modules():
    """
    Reload settings, stats_dialog, and deck_widget modules.
    This allows changes to be reflected without restarting Anki.
    """
    try:
        # Get the package name
        package_name = __name__.rsplit('.', 1)[0]  # Gets 'Focumon' or the addon folder name
        
        # List of modules to reload
        modules_to_reload = [
            'settings',
            'stats_dialog', 
            'deck_widget',
            'scrapers',  # Also reload scrapers as it's used by deck_widget
            'font_utils'  # Reload font utils as well
        ]
        
        for module_name in modules_to_reload:
            full_module_name = f"{package_name}.{module_name}"
            
            if full_module_name in sys.modules:
                module = sys.modules[full_module_name]
                importlib.reload(module)

        
        # Clear the deck widget cache
        deck_widget_module = sys.modules.get(f"{package_name}.deck_widget")
        if deck_widget_module and hasattr(deck_widget_module, 'reset_cache'):
            deck_widget_module.reset_cache()
        
        # Refresh the deck browser to show changes
        if mw.state == "deckBrowser":
            mw.deckBrowser.refresh()
        
        from .ui_utils import show_custom_info
        show_custom_info("Successfully reloaded profile information", title="Refresh")
        
    except Exception as e:
        from .ui_utils import show_custom_info
        show_custom_info(f"Error reloading modules:<br><br>{str(e)}<br><br>You may need to restart Anki.", title="Error")
