import formshare.plugins as plugins
import formshare.plugins.utilities as u
import sys
import os


class alliance_branding(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")
        u.add_static_view(config, "alliance", "static")

    def get_translation_directory(self):
        module = sys.modules["alliance_branding"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "alliance_branding"
