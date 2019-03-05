import os
from configparser import RawConfigParser


ENV_LOCAL = 'local'
ENV_PRODUCTION = 'production'
ENV_DEVELOPMENT = 'development'


config = RawConfigParser()
path = os.path.join(os.path.dirname(__file__), 'settings.ini')
config.read(path)

ENV = config.get('settings', 'ENVIRONMENT') or 'development'

ENVIRONMENTS = (ENV_LOCAL, ENV_PRODUCTION, ENV_DEVELOPMENT)

if ENV not in ENVIRONMENTS:
    print('Invalid DJANGO_ENV')
    ENV = ENV_DEVELOPMENT

if ENV == ENV_LOCAL:
    from .local import *
    print('Set local environment variable.')

if ENV == ENV_DEVELOPMENT:
    from .development import *
    print('Set development environment variable.')

if ENV == ENV_PRODUCTION:
    from .production import *
    print('Set production environment variable.')


