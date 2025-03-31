# ================================================== #

# ~~ Importando appconfig.
from django.apps import AppConfig

# ================================================== #

# ~~ App.
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

# ================================================== #