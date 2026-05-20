"""
	Fenomscrapers Module
"""

import threading

import xbmc
from magneto.modules import control, log_utils
window = control.homeWindow
LOGINFO = 1 # (LOGNOTICE(2) deprecated in 19, use LOGINFO(1))

class CheckSettingsFile:
	def run(self):
		try:
			xbmc.log('[ script.module.magneto.redux ]  CheckSettingsFile Service Starting...', LOGINFO)
			window.clearProperty('magneto')
			profile_dir = control.dataPath
			if not control.existsPath(profile_dir):
				success = control.makeDirs(profile_dir)
				if success: log_utils.log('%s : created successfully' % profile_dir, LOGINFO)
			else: log_utils.log('%s : already exists' % profile_dir, LOGINFO)
			settings_xml = control.joinPath(profile_dir, 'settings.xml')
			if not control.existsPath(settings_xml):
				control.setSetting('module.provider', 'Magneto')
				log_utils.log('%s : created successfully' % settings_xml, LOGINFO)
			else: log_utils.log('%s : already exists' % settings_xml, LOGINFO)
			return xbmc.log('[ script.module.magneto.redux ]  Finished CheckSettingsFile Service', LOGINFO)
		except:
			import traceback
			traceback.print_exc()

class SettingsMonitor(control.monitor_class):
	def __init__ (self):
		control.monitor_class.__init__(self)
		window.setProperty('magneto.debug.reversed', control.setting('debug.reversed'))
		xbmc.log('[ script.module.magneto.redux ]  Settings Monitor Service Starting...', LOGINFO)

	def onSettingsChanged(self): # Kodi callback when the addon settings are changed
		window.clearProperty('magneto_settings')
		control.sleep(50)
		refreshed = control.make_settings_dict()
		control.refresh_debugReversed()

class CheckUndesirablesDatabase:
	def run(self):
		xbmc.log('[ script.module.magneto.redux ]  "CheckUndesirablesDatabase" Service Starting...', LOGINFO)
		from magneto.modules import undesirables
		try:
			old_database = undesirables.Undesirables().check_database()
			if old_database: undesirables.add_new_default_keywords()
		except:
			import traceback
			traceback.print_exc()
		return xbmc.log('[ script.module.magneto.redux ]  Finished "CheckUndesirablesDatabase" Service', LOGINFO)

def _start_trakt_sync():
	try:
		from magneto.trakt.sync import TraktSyncService
		t = threading.Thread(target=TraktSyncService().run, daemon=True)
		t.start()
	except Exception:
		import traceback
		traceback.print_exc()


def _load_trakt_credentials():
	try:
		from magneto.trakt.compat import load_trakt_credentials, get_property, trakt_client, EMPTY_USER
		load_trakt_credentials()
		# If token is present but username is missing (e.g. old trakt_auth.json before this fix),
		# fetch the username from the Trakt API. Guard on client key to avoid a startup notification.
		token = get_property('trakt_token')
		user = get_property('trakt_user')
		if token and (not user or user == EMPTY_USER) and trakt_client():
			try:
				from magneto.trakt.api.trakt import TraktAPI
				from magneto.trakt.compat import set_setting as trakt_set_setting
				result = TraktAPI().auth.call_trakt('users/me')
				if result and isinstance(result, dict):
					trakt_set_setting('trakt_user', str(result['username']))
					xbmc.log('[ script.module.magneto.redux ]  Trakt username fetched: %s' % result['username'], LOGINFO)
			except Exception:
				pass
		xbmc.log('[ script.module.magneto.redux ]  Trakt credentials loaded', LOGINFO)
	except Exception:
		import traceback
		traceback.print_exc()


def main():
	while not control.monitor.abortRequested():
		xbmc.log('[ script.module.magneto.redux ]  Service Started', LOGINFO)
		CheckSettingsFile().run()
		CheckUndesirablesDatabase().run()
		if control.isVersionUpdate():
			control.clean_settings()
			xbmc.log('[ script.module.magneto.redux ]  Settings file cleaned complete', LOGINFO)
		_load_trakt_credentials()
		_start_trakt_sync()
		break
	SettingsMonitor().waitForAbort()
	xbmc.log('[ script.module.magneto.redux ]  Service Stopped', LOGINFO)

main()
