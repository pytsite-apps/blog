"""PytSite Blog Settings Form.
"""
from pytsite import widget, lang, validation, settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(settings.Form):
    """PytSite Blog Settings Form.
    """

    def _setup_widgets(self):
        """Hook.
        """
        self.add_widget(widget.input.StringList(
            uid='setting_links',
            weight=10,
            label=lang.t('app@links'),
            add_btn_label=lang.t('app@add_link'),
            unique=True,
            rules=validation.rule.Url(),
        ))

        # It is important to call super method AFTER
        super()._setup_widgets()
