from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PiratesConfig(AppConfig):
    name = "pirates"
    verbose_name = _("Pirates")

    def ready(self):
        try:
            import pirates.signals
        except ImportError:
            pass
