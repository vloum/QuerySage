# -*- coding: utf-8 -*-
from environs import Env
import os

mode = os.getenv('APP_ENV', 'test')

env_path = '.env.' + mode

env = Env()
env.read_env(path=env_path)

EMBEDDING_TYPE = env.str('EMBEDDING_TYPE', '')

SU_URL = env.str('SU_URL', '')
SU_TABLE = env.str('SU_TABLE', '')
SU_TIMEOUT = env.int('SU_TIMEOUT', 60)
SU_PASSWORD = env.str('SU_PASSWORD', '')
SU_SERVICE_KEY = env.str('SU_SERVICE_KEY', '')
SU_MATCH_FUNCTION = env.str('SU_MATCH_FUNCTION', '')

OPEN_BASE_URL = env.str('OPEN_BASE_URL','')
OPEN_AI_TOKEN = env.str('OPEN_AI_TOKEN', '')
OPEN_AI_PROXY = env.str('OPEN_AI_PROXY', '')
OPEN_AI_ORGANIZATION = env.str('OPEN_AI_ORGANIZATION','')
OPEN_AI_MODEL = env.str('OPEN_AI_MODEL','gpt-3.5-turbo-16k-0613')

BING_SEARCH_KEY = env.str('BING_SEARCH_KEY','')

TAVILY_API_KEY = env.str('TAVILY_API_KEY', '')