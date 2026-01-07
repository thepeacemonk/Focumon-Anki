from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

try:
    from aqt.qt import QWebEngineView, QWebEngineProfile, QWebEnginePage
except ImportError:
    # Fallback for older Anki versions or specific builds
    QWebEngineView = None

import os
import shutil
from . import scrapers

class FocumonWindow(QMainWindow):
    def cleanup_cache(self, path):
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f"Failed to clean cache: {e}")

    def __init__(self, parent=None):
        super(FocumonWindow, self).__init__(parent)
        self.setWindowTitle("Focumon for Anki")
        self.resize(1100, 750)

        # Ensure the window stays on top if desired
        # Retrieve the config using the add-on name explicitly if needed, but __name__ here is Focumon.main
        # We need the package name which is usually the directory name or accessible via mw.addonManager.addonFromModule
        addon_id = mw.addonManager.addonFromModule(__name__)
        config = mw.addonManager.getConfig(addon_id)
        if config and config.get("always_on_top", False):
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        if QWebEngineView is None:
            showInfo("QWebEngineView is not supported on this Anki version.")
            return

        self.browser = QWebEngineView()
        
        # Enable persistent cookies/storage so you stay logged in
        addon_dir = os.path.dirname(__file__)
        storage_path = os.path.join(addon_dir, "user_data")
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        profile = QWebEngineProfile("FocumonProfile", self.browser)
        profile.setPersistentStoragePath(storage_path)

        # Separate cache path so we can clean it independently from cookies/storage
        cache_path = os.path.join(addon_dir, "cache_trash")
        self.cleanup_cache(cache_path)
        
        # Clean up legacy cache folders from previous versions if they exist in user_data
        for legacy_folder in ["GPUCache", "DawnCache", "VideoDecodeStats", "ShaderCache", "Code Cache"]:
            self.cleanup_cache(os.path.join(storage_path, legacy_folder))

        profile.setCachePath(cache_path)
        
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)

        page = QWebEnginePage(profile, self.browser)
        self.browser.setPage(page)
        
        # Load Focumon App
        self.browser.setUrl(QUrl("https://www.focumon.com"))
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def closeEvent(self, event):
        # Just hide the window instead of destroying it for faster reopening
        event.ignore()
        self.hide()

    def refresh(self):
        """Reload the current page."""
        if self.browser:
            self.browser.reload()

    def sync_stats(self):
        """
        Fetches and displays Focumon stats using HTTP request.
        Works independently of whether the browser window is open.
        """
        # Get username from config
        addon_id = mw.addonManager.addonFromModule(__name__)
        config = mw.addonManager.getConfig(addon_id)
        username = config.get("focumon_username", "").strip()
        
        if not username:
            showInfo("Please set your Focumon username in the add-on settings first.\n\nGo to: Tools > Focumon > Settings")
            return
        
        # Fetch profile page
        try:
            import urllib.request
            from .stats_dialog import StatsDialog
            
            url = f"https://www.focumon.com/trainers/{username}"
            
            # Create request with headers to appear like a browser
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
            
            # Parse stats
            levels = scrapers.extract_levels(html)
            focudex = scrapers.extract_focudex(html)
            focumon_name = scrapers.extract_focumon_name(html)
            sprite_urls = scrapers.extract_sprite_urls(html)
            
            # Prepare data for dialog
            stats_data = {'username': username}
            
            if levels:
                if 'trainer_level' in levels:
                    stats_data['trainer_level'] = levels['trainer_level']
                if 'focumon_level' in levels:
                    stats_data['focumon_level'] = levels['focumon_level']
            
            if focudex:
                stats_data['focudex_progress'] = focudex
            
            if focumon_name:
                stats_data['focumon_name'] = focumon_name
            
            # Download sprite images
            if sprite_urls:
                if 'trainer_sprite' in sprite_urls:
                    try:
                        sprite_url = f"https://www.focumon.com{sprite_urls['trainer_sprite']}"
                        req = urllib.request.Request(sprite_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=5) as response:
                            stats_data['trainer_sprite_data'] = response.read()
                    except:
                        pass  # Fail silently if sprite can't be downloaded
                
                if 'focumon_sprite' in sprite_urls:
                    try:
                        sprite_url = f"https://www.focumon.com{sprite_urls['focumon_sprite']}"
                        req = urllib.request.Request(sprite_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=5) as response:
                            stats_data['focumon_sprite_data'] = response.read()
                    except:
                        pass  # Fail silently if sprite can't be downloaded
            
            if len(stats_data) > 1:  # More than just username
                dialog = StatsDialog(stats_data, self)
                dialog.exec()
            else:
                showInfo(f"No stats found for @{username}.\n\nThe profile page layout might have changed, or the username might be incorrect.")
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                showInfo(f"Profile not found for username: {username}\n\nPlease check your username in the settings.")
            else:
                showInfo(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            showInfo(f"Network error: {e.reason}\n\nPlease check your internet connection.")
        except Exception as e:
            showInfo(f"Error fetching stats: {str(e)}")