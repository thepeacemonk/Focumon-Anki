import re

def extract_username_from_dashboard(html_content):
    """
    Extracts the username from the dashboard HTML looking for the Public Profile link.
    Example: <a ... href="/trainers/PeaceMonk">
    """
    match = re.search(r'href="/trainers/([^"]+)"', html_content)
    if match:
        return match.group(1)
    return None

def extract_levels(html_content):
    """
    Extracts both Trainer Level (1st badge) and Focumon Level (2nd badge).
    Returns a dict with 'trainer_level' and 'focumon_level'.
    """
    # Find all badges with LV.
    badges = re.findall(r'<div class="badge[^>]*">LV\.(\d+)</div>', html_content)
    levels = {}
    if len(badges) >= 1:
        levels['trainer_level'] = badges[0]
    if len(badges) >= 2:
        levels['focumon_level'] = badges[1]
    return levels

def extract_focumon_level(html_content):
    """
    Extracts the Focumon Level (2nd badge) - kept for backward compatibility.
    """
    levels = extract_levels(html_content)
    return levels.get('focumon_level')

def extract_focudex(html_content):
    """
    Extracts Focudex progress (e.g., '2/186').
    """
    # Pattern: <span>Focudex</span> followed by <span>2/186</span>
    match = re.search(r'<span>Focudex</span>\s*<span>([\d/]+)</span>', html_content)
    if match:
        return match.group(1).strip()
    return None

def extract_focumon_name(html_content):
    """
    Extracts the currently equipped Focumon name from data-tip attribute.
    """
    # Look for the second tooltip (first is trainer, second is Focumon)
    # Pattern: data-tip="Hemling"
    tooltips = re.findall(r'data-tip="([^"]+)"', html_content)
    if len(tooltips) >= 2:
        return tooltips[1]  # Second tooltip is the Focumon
    return None

def extract_sprite_urls(html_content):
    """
    Extracts trainer and Focumon sprite URLs.
    Returns a dict with 'trainer_sprite' and 'focumon_sprite'.
    """
    sprites = {}
    
    # Trainer sprite: /assets/trainer/battle/XXX.png
    trainer_match = re.search(r'src="(/assets/trainer/battle/[^"]+\.png)"', html_content)
    if trainer_match:
        sprites['trainer_sprite'] = trainer_match.group(1)
    
    # Focumon sprite: /assets/focumon/battle/XXX.png
    focumon_match = re.search(r'src="(/assets/focumon/battle/[^"]+\.png)"', html_content)
    if focumon_match:
        sprites['focumon_sprite'] = focumon_match.group(1)
    
    return sprites
