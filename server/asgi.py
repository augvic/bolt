# ================================================== #

# ~~ Imports.
import os
from django.core.asgi import get_asgi_application

# ================================================== #

# ~~ Config.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
application = get_asgi_application()

# ================================================== #
