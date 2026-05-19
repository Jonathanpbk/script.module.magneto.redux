import xbmcgui

from magneto.trakt.compat import translation


class QRProgressDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, xml_file, location):
        super().__init__(xml_file, location)
        self.title = 'Trakt Authentication'
        self.message = ''
        self.progress = 0
        self.iscanceled = False
        self.qr_image_path = ''

    def setup(
        self,
        title,
        qr_code,
        url,
        user_code='',
        debrid_type='',
        is_debrid=True,
        url_label_id=90557,
        custom_message=None,
    ):
        self.title = title
        self.qr_image_path = qr_code or ''

        if custom_message:
            self.message = custom_message
        elif is_debrid:
            if debrid_type == 'RealDebrid':
                self.message = 'Visit https://real-debrid.com/device\n\nEnter code: %s' % user_code
            else:
                self.message = 'Visit %s\n\nEnter code: %s' % (url, user_code)
        else:
            if user_code:
                self.message = (
                    'Visit [COLOR cyan]%s[/COLOR]\n\nEnter code: [B][COLOR seagreen]%s[/COLOR][/B]'
                    % (url, user_code)
                )
            else:
                self.message = 'Visit [COLOR cyan]%s[/COLOR]' % url

    def show_dialog(self):
        self.show()
        self.onInit()

    def close_dialog(self):
        self.close()

    def onInit(self):
        self.getControl(12001).setLabel(self.title)
        self.getControl(12002).setLabel(self.message)
        self.getControl(12004).setPercent(self.progress)
        if self.qr_image_path:
            self.getControl(12006).setImage(self.qr_image_path)
        self.setFocusId(12003)

    def update_progress(self, percent, message=None):
        self.progress = percent
        self.getControl(12004).setPercent(percent)
        if message:
            self.getControl(12002).setLabel(message)

    def onClick(self, controlId):
        if controlId == 12003:
            self.iscanceled = True
            self.close_dialog()

    def onAction(self, action):
        if action.getId() in (10, 92):
            self.iscanceled = True
            self.close_dialog()
