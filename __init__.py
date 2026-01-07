from aqt import mw
from aqt.qt import QAction, QMenu
from .main import FocumonWindow
from .settings import SettingsDialog
from . import deck_widget  # Import to register deck browser widget hooks
from .reload_utils import reload_modules

def show_focumon():
    if not hasattr(mw, "focumon_window"):
        mw.focumon_window = FocumonWindow(mw)
    mw.focumon_window.show()
    mw.focumon_window.activateWindow()

def show_settings():
    d = SettingsDialog(mw)
    if d.exec():
        from .deck_widget import reset_cache
        reset_cache()
        if mw.state == "deckBrowser":
            mw.deckBrowser.refresh()

# Setup the menu item in Tools
focumon_menu = QMenu("Focumon", mw)
mw.form.menuTools.addMenu(focumon_menu)

action = QAction("Open Focumon", mw)
action.triggered.connect(show_focumon)
focumon_menu.addAction(action)

settings_action = QAction("Settings", mw)
settings_action.triggered.connect(show_settings)
focumon_menu.addAction(settings_action)

def sync_focumon_stats():
    if not hasattr(mw, "focumon_window"):
        mw.focumon_window = FocumonWindow(mw)
    # Ensure window is created so the webview exists
    # If hidden, that's fine, we just need the instance
    mw.focumon_window.sync_stats()

sync_action = QAction("Profile", mw)
sync_action.triggered.connect(sync_focumon_stats)
focumon_menu.addAction(sync_action)

# Add separator and reload action for development
focumon_menu.addSeparator()
reload_action = QAction("Refresh", mw)
reload_action.triggered.connect(reload_modules)
focumon_menu.addAction(reload_action)

def show_instructions():
    from .instructions_dialog import InstructionsDialog
    if not hasattr(mw, "instructions_dialog") or not mw.instructions_dialog:
        mw.instructions_dialog = InstructionsDialog(mw)
    mw.instructions_dialog.show()
    mw.instructions_dialog.activateWindow()
    mw.instructions_dialog.raise_()

instr_action = QAction("Instructions", mw)
instr_action.triggered.connect(show_instructions)
focumon_menu.insertAction(settings_action, instr_action)

def check_welcome_screen():
    config = mw.addonManager.getConfig(__name__)
    if config is None:
        config = {}
    
    # Default true if not set
    if config.get("show_welcome", True):
        # We need to show the welcome screen
        # Use a timer to ensure main window is visible/ready
        from .welcome_dialog import WelcomeDialog
        if not hasattr(mw, "welcome_dialog") or not mw.welcome_dialog:
            mw.welcome_dialog = WelcomeDialog(mw)
        mw.welcome_dialog.show()
        mw.welcome_dialog.activateWindow()
        mw.welcome_dialog.raise_()

from aqt import gui_hooks
gui_hooks.profile_did_open.append(check_welcome_screen)