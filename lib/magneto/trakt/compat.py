"""
Compatibility shim: maps kellytook utility function names to Magneto equivalents.
All Trakt API files import from here instead of from kellytook's lib.utils.kodi.* modules.
"""

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

_ADDON = xbmcaddon.Addon('script.module.magneto.redux')
ADDON_PATH = _ADDON.getAddonInfo('path')
ADDON_PROFILE_PATH = xbmcvfs.translatePath(_ADDON.getAddonInfo('profile'))
ADDON_VERSION = _ADDON.getAddonInfo('version')

EMPTY_USER = 'unknown_user'

_window = xbmcgui.Window(10000)


# --- Window properties (used to store auth tokens in RAM) ---

def get_property(prop):
    return _window.getProperty(prop)

def set_property(prop, value):
    return _window.setProperty(prop, str(value) if value is not None else '')

def clear_property(prop):
    return _window.clearProperty(prop)

def get_property_no_fallback(prop):
    val = _window.getProperty(prop)
    return val if val != '' else None

def set_property_no_fallback(prop, value):
    return _window.setProperty(prop, str(value) if value is not None else '')


# --- Settings (routed through Magneto's cached settings dict) ---

def get_setting(setting_id, fallback=None):
    from magneto.modules.control import setting
    return setting(setting_id, fallback)

def set_setting(setting_id, value):
    from magneto.modules.control import setSetting
    return setSetting(setting_id, str(value))


# --- Logging ---

def kodilog(message, level=xbmc.LOGINFO):
    xbmc.log('[script.module.magneto.redux][trakt] %s' % str(message), level)


# --- Notifications ---

def notification(message, time=3000):
    from magneto.modules.control import notification as _notify
    _notify(message=str(message), time=time)


# --- Sleep ---

def sleep(ms):
    xbmc.sleep(int(ms))


# --- Localised strings ---

def translation(string_id):
    return _ADDON.getLocalizedString(string_id)


# --- Dialogs ---

def dialog_ok(heading='', line1=''):
    xbmcgui.Dialog().ok(str(heading), str(line1))


# --- File operations ---

def delete_file(path):
    xbmcvfs.delete(path)


# --- Clipboard ---

def copy2clip(text):
    xbmc.executebuiltin('CopyText(%s)' % str(text))


# --- Date/time ---

def get_datetime():
    from datetime import datetime
    return datetime.now()


# --- Settings helper wrappers (match kellytook's settings module) ---

def trakt_client():
    return get_setting('trakt_client', '')

def trakt_secret():
    return get_setting('trakt_secret', '')

def trakt_lists_sort_order(setting_name):
    try:
        return int(get_setting('trakt_sort_%s' % setting_name, '0'))
    except (TypeError, ValueError):
        return 0


# --- Stubs for list-browsing features (not used in scrobble-only mode) ---

def set_pluging_category(*args, **kwargs):
    """Stub: sets plugin category for list views. Not used for scrobbling."""
    pass

def cache_object(function, string, args, **kwargs):
    """Stub: general cache. Not used for scrobbling — calls function directly."""
    if isinstance(args, (list, tuple)):
        return function(*args)
    return function(args)

def action_url_run(name, **kwargs):
    """Stub: builds a RunPlugin URL for context menus. Not used for scrobbling."""
    return ''
