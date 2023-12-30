# -*- coding: utf-8 -*-
from environs import Env
import os

mode = os.getenv('APP_ENV', 'test')

env_path = '.env.' + mode

env = Env()
env.read_env(path=env_path)

OPEN_AI_TOKEN = env.str('OPEN_AI_TOKEN', '')
OPEN_AI_ORGANIZATION = env.str('OPEN_AI_ORGANIZATION','')
OPEN_AI_MODEL = env.str('OPEN_AI_MODEL','gpt-3.5-turbo-16k-0613')
OPEN_BASE_URL = env.str('OPEN_BASE_URL','')
OPEN_AI_PROXY = env.str('OPEN_AI_PROXY', '')