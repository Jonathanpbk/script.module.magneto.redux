"""
QR code image generator for Trakt authentication.

Requires the 'segno' library (pure Python, no C extensions):
  - On CoreELEC, install via: pip3 install segno
  - Or place the segno package folder inside lib/vendor/segno/

If segno is not available, make_qrcode() returns None and the auth dialog
falls back to showing the URL and user code as plain text, which still works.
"""

import os

import xbmcvfs

from magneto.trakt.compat import ADDON_PROFILE_PATH, kodilog

# Try to import segno from several possible locations
_segnomake = None
try:
    from segno import make as _segnomake
except ImportError:
    try:
        from magneto.vendor.segno import make as _segnomake
    except ImportError:
        pass


def make_qrcode(url):
    """Generate a QR code PNG for the given URL. Returns the file path, or None on failure."""
    if not url:
        return None
    if _segnomake is None:
        kodilog(
            'segno library not found — QR code image unavailable. '
            'Install with: pip3 install segno'
        )
        return None
    try:
        if not os.path.exists(ADDON_PROFILE_PATH):
            xbmcvfs.mkdir(ADDON_PROFILE_PATH)
        art_path = os.path.join(ADDON_PROFILE_PATH, 'trakt_qr.png')
        kodilog('Creating Trakt QR code: %s' % art_path)
        qrcode = _segnomake(url, micro=False)
        qrcode.save(art_path, scale=20)
        return art_path
    except Exception as e:
        kodilog('Error creating QR code: %s' % str(e))
        return None
