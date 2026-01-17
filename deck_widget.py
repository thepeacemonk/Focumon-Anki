"""
Deck Browser Widget for Focumon Add-on
Displays a 200px by 200px widget with Focumon stats on the deck browser.
"""

from aqt import mw, gui_hooks
import aqt.deckbrowser
from . import scrapers
import urllib.request
import urllib.error

# Cache for the widget HTML
cached_html = None

def generate_css():
    """Generate CSS for the Focumon widget."""
    from . import font_utils
    
    # Detect theme
    is_dark = mw.pm.night_mode() if hasattr(mw.pm, 'night_mode') else False
    
    # Color scheme
    bg_color = "#242424" if is_dark else "#FAF8F2"
    text_color = "#FAF8F2" if is_dark else "#242424"
    accent_color = "#FFDD19"
    stat_bg = "#202020" if is_dark else "#E3E2DC"
    
    # Get font-face CSS
    font_face = font_utils.get_font_face_css()
    
    return f"""
        {font_face}
        
        #focumon-widget-container {{
            position: relative;
            display: inline-block;
            margin-top: 20px;
            margin-bottom: 20px;
            margin-left: 6.875px;
            margin-right: 6.875px;
        }}
        
        #focumon-widget {{
            width: 200px;
            height: 200px;
            border-radius: 20px;
            background: {bg_color};
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px;
            box-sizing: border-box;
            color: {text_color};
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow: hidden;
        }}
        
        #focumon-widget .widget-username {{
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 4px;
            text-align: center;
            font-family: 'Silkscreen', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        
        #focumon-widget .sprites-container {{
            position: relative;
            width: 140px;
            height: 65px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        #focumon-widget .sprite {{
            position: absolute;
            width: 60px;
            height: 60px;
            object-fit: contain;
            image-rendering: pixelated;
            bottom: 1px;
        }}
        
        #focumon-widget .sprite.trainer {{
            left: 21px;
            z-index: 2;
        }}
        
        #focumon-widget .sprite.focumon {{
            left: 59px;
            z-index: 1;
        }}
        
        #focumon-widget .widget-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            width: 100%;
            margin-top: 2px;
        }}
        
        #focumon-widget .stat-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 10px;
            background: {stat_bg};
            padding: 8px 10px;
            border-radius: 16px;
            width: 90%;
            line-height: 1;
        }}
        
        #focumon-widget .stat-label {{
            font-weight: 600;
            font-family: 'Silkscreen', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: {text_color};
        }}
        
        #focumon-widget .stat-value {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: normal;
            font-family: 'Silkscreen', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
            font-size: 8px;
            line-height: 1;
            color: #D1D0D0;
            background: #2E282A;
            padding: 4px 6px;
            border-radius: 8px;
        }}
        
        #focumon-widget .no-stats {{
            font-size: 12px;
            text-align: center;
            opacity: 0.9;
            line-height: 1.4;
            margin-top: 20px;
            font-family: 'Silkscreen', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}

        #focumon-widget .top-buttons {{
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            z-index: 10;
        }}

        #focumon-widget .icon-btn {{
            width: 16px;
            height: 16px;
            cursor: pointer;
            opacity: 0.4;
            transition: opacity 0.2s ease;
            color: {text_color};
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        #focumon-widget .icon-btn:hover {{
            opacity: 1;
        }}

        #focumon-widget .icon-btn svg {{
            width: 100%;
            height: 100%;
            fill: currentColor;
        }}
    """

def generate_html(stats_data=None):
    """Generate HTML for the Focumon widget."""
    
    # Top Buttons (Settings, Refresh, & Open)
    gear_svg = get_svg_content("gear.svg")
    refresh_svg = get_svg_content("refresh.svg")
    gamepad_svg = get_svg_content("gamepad.svg")
    
    buttons_html = f"""
        <div class="top-buttons">
            <div class="icon-btn" onclick="pycmd('focumon_settings')" title="Settings">
                {gear_svg}
            </div>
            <div class="icon-btn" onclick="pycmd('focumon_refresh')" title="Refresh">
                {refresh_svg}
            </div>
            <div class="icon-btn" onclick="pycmd('focumon_open')" title="Open Focumon">
                {gamepad_svg}
            </div>
        </div>
    """
    
    if not stats_data or len(stats_data) <= 1:  # Only username or nothing
        # Load focumon_fam.png
        import os
        import base64
        addon_dir = os.path.dirname(__file__)
        img_path = os.path.join(addon_dir, "focumon_fam.png")
        img_html = ""
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode('utf-8')
                img_html = f'<img src="data:image/png;base64,{b64_data}" style="width: 45%; height: auto; margin-bottom: 0px; border-radius: 8px;">'

        # Show placeholder when no stats are available
        return f"""
            <div id="focumon-widget">
                {buttons_html}
                {img_html}
                <div class="no-stats" style="margin-top: 5px;">
                    Pair your username<br>
                    on Settings<br>
                    by clicking the gear icon
                </div>
            </div>
        """
    
    # Start building the widget HTML
    html_parts = []
    
    html_parts.append(buttons_html)

    # Username at the top
    username = stats_data.get('username', 'Trainer')
    html_parts.append(f'<div class="widget-username">{username}</div>')
    
    # Display sprites side by side if available
    if 'trainer_sprite_data' in stats_data or 'focumon_sprite_data' in stats_data:
        import base64
        sprites_html = '<div class="sprites-container">'
        
        if 'trainer_sprite_data' in stats_data:
            sprite_b64 = base64.b64encode(stats_data['trainer_sprite_data']).decode('utf-8')
            sprites_html += f'<img class="sprite trainer" src="data:image/png;base64,{sprite_b64}" alt="Trainer">'
        
        if 'focumon_sprite_data' in stats_data:
            sprite_b64 = base64.b64encode(stats_data['focumon_sprite_data']).decode('utf-8')
            sprites_html += f'<img class="sprite focumon" src="data:image/png;base64,{sprite_b64}" alt="Focumon">'
        
        sprites_html += '</div>'
        html_parts.append(sprites_html)
    
    # Stats section
    html_parts.append('<div class="widget-content">')
    
    # Display trainer level if available
    if 'trainer_level' in stats_data:
        html_parts.append(f'''
            <div class="stat-row">
                <span class="stat-label">Level</span>
                <span class="stat-value">LV.{stats_data["trainer_level"]}</span>
            </div>
        ''')
    
    # Display Focudex progress if available
    if 'focudex_progress' in stats_data:
        html_parts.append(f'''
            <div class="stat-row">
                <span class="stat-label">Focudex</span>
                <span class="stat-value">{stats_data["focudex_progress"]}</span>
            </div>
        ''')
    
    html_parts.append('</div>')  # Close widget-content
    
    return f'<div id="focumon-widget">{"" .join(html_parts)}</div>'

def fetch_stats():
    """Fetch Focumon stats for the configured username."""
    addon_id = mw.addonManager.addonFromModule(__name__)
    config = mw.addonManager.getConfig(addon_id)
    username = config.get("focumon_username", "").strip() if config else ""
    
    if not username:
        return None
    
    try:
        url = f"https://www.focumon.com/trainers/{username}"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
        
        # Parse stats
        stats_data = {'username': username}
        
        levels = scrapers.extract_levels(html)
        if levels:
            if 'trainer_level' in levels:
                stats_data['trainer_level'] = levels['trainer_level']
            if 'focumon_level' in levels:
                stats_data['focumon_level'] = levels['focumon_level']
        
        focudex = scrapers.extract_focudex(html)
        if focudex:
            stats_data['focudex_progress'] = focudex
        
        focumon_name = scrapers.extract_focumon_name(html)
        if focumon_name:
            stats_data['focumon_name'] = focumon_name
        
        sprite_urls = scrapers.extract_sprite_urls(html)
        if sprite_urls:
            if 'trainer_sprite' in sprite_urls:
                try:
                    sprite_url = f"https://www.focumon.com{sprite_urls['trainer_sprite']}"
                    req = urllib.request.Request(sprite_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=3) as response:
                        stats_data['trainer_sprite_data'] = response.read()
                except:
                    pass
            
            if 'focumon_sprite' in sprite_urls:
                try:
                    sprite_url = f"https://www.focumon.com{sprite_urls['focumon_sprite']}"
                    req = urllib.request.Request(sprite_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=3) as response:
                        stats_data['focumon_sprite_data'] = response.read()
                except:
                    pass
        
        return stats_data if len(stats_data) > 1 else None
        
    except:
        return None

def get_svg_content(filename):
    """Read SVG content from assets folder."""
    import os
    addon_dir = os.path.dirname(__file__)
    path = os.path.join(addon_dir, "assets", filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def handle_focumon_commands(handled, message, context):
    """Handle JS messages from the widget."""
    if message == "focumon_settings":
        from .settings import SettingsDialog
        d = SettingsDialog(mw)
        if d.exec():
            reset_cache()
            mw.deckBrowser.refresh()
        return (True, None)
    elif message == "focumon_open":
        if not hasattr(mw, "focumon_window"):
            from .main import FocumonWindow
            mw.focumon_window = FocumonWindow(mw)
        mw.focumon_window.show()
        mw.focumon_window.activateWindow()
        return (True, None)
    elif message == "focumon_refresh":
        reset_cache()
        if mw.state == "deckBrowser":
            mw.deckBrowser.refresh()
        
        # Also refresh the Focumon window content if it's initialized
        if hasattr(mw, "focumon_window"):
            mw.focumon_window.refresh()
            
        return (True, None)
    return handled

# Register command handler
gui_hooks.webview_did_receive_js_message.append(handle_focumon_commands)

def add_widget_to_deck_browser(deck_browser: aqt.deckbrowser.DeckBrowser, 
                                content: aqt.deckbrowser.DeckBrowserContent):
    """Appends the Focumon widget to the deck browser's stats area."""
    global cached_html
    
    # Check if widget should be hidden
    addon_id = mw.addonManager.addonFromModule(__name__)
    config = mw.addonManager.getConfig(addon_id)
    if config and config.get("hide_deck_widget", False):
        return

    # Prevent adding the widget multiple times
    if "<div id='focumon-widget-container'>" in content.stats:
        return
    
    if cached_html is None:
        stats_data = fetch_stats()
        css = generate_css()
        html_content = generate_html(stats_data)
        cached_html = f"<div id='focumon-widget-container'><style>{css}</style>{html_content}</div>"
    
    content.stats += cached_html

def reset_cache(*args, **kwargs):
    """Clears the cached HTML, forcing a refresh on next view."""
    global cached_html
    cached_html = None

def on_theme_change():
    """Reset cache and refresh deck browser when theme changes."""
    reset_cache()
    if mw.state == "deckBrowser":
        mw.deckBrowser.refresh()

# Register hooks
gui_hooks.deck_browser_will_render_content.append(add_widget_to_deck_browser)
gui_hooks.reviewer_will_end.append(reset_cache)
gui_hooks.sync_did_finish.append(reset_cache)
gui_hooks.theme_did_change.append(on_theme_change)
