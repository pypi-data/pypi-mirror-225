from django.contrib.admin import options
from django.db import models

from giant_utils.widgets import RedactorWidget


class RichTextField(models.TextField):
    """
    Rich text field for use with Redactor
    """

    def formfield(self, **kwargs):
        defaults = {"widget": RedactorWidget}
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)


options.FORMFIELD_FOR_DBFIELD_DEFAULTS[RichTextField] = {"widget": RedactorWidget}
