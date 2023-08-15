import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import Media, Textarea
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

# Default WYSIWYG_CONFIG
DEFAULT_WYSIWYG_CONFIG = {
    "lang": "en",
    "minHeight": "300px",
    "buttons": "html | format | undo redo | bold italic | ul ol | link | sub sup".split(),
    "formatting": ["h1", "h2", "h3", "p"],
    "linkTitle": True,
    "linkNewTab": True,
    "structure": True,
    "removeNewLines": True,
    "pasteImages": False,
    "tabAsSpaces": 4,
    "plugins": ["table"],
}

# Get WYSIWYG_CONFIG from Django's settings or use default configuration
WYSIWYG_CONFIG = getattr(settings, "WYSIWYG_CONFIG", DEFAULT_WYSIWYG_CONFIG)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super(LazyEncoder, self).default(obj)


class RedactorWidget(Textarea):
    """
    Used to render redactor into the backend of the site.
    """

    def __init__(self, attrs=None, editor_options=None):
        super().__init__(attrs)
        self.editor_options = editor_options or WYSIWYG_CONFIG

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""
        attrs["data-config"] = self.js_config
        cls = attrs.get("class", "")
        attrs["class"] = (
            cls + " uninitialised redactor-init" if cls else "uninitialised redactor-init"
        )
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        return mark_safe(
            "<textarea%s>\r\n%s</textarea>" % (flatatt(final_attrs), force_str(value))
        )

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    @property
    def js_config(self):
        """
        Outputs config as JSON object for redactor.js to load
        """
        return json.dumps(self.editor_options, cls=LazyEncoder)

    @property
    def media(self):
        """
        Returns media files for django to output
        """
        css = {"all": ("vendor/redactor/redactor.min.css", "vendor/redactor/django-admin.css")}
        js = ("vendor/redactor/redactor.min.js", "vendor/redactor/init.js")

        for plugin in self.editor_options.get("plugins", []):
            js += (f"vendor/redactor/plugins/{plugin}/{plugin}.min.js",)

        return Media(css=css, js=js)
