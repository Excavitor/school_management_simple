from .base import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [config("RENDER_EXTERNAL_HOSTNAME", default="")]

DATABASES = {
    "default": dj_database_url.config(
        # Replace this with your local test DB for migrations
        default=config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"