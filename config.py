# -*- coding: utf-8 -*-
from environs import Env
import os

mode = os.getenv('APP_ENV', 'test')

env_path = '.env.' + mode

env = Env()
env.read_env(path=env_path)

EMBEDDING_TYPE = env.str('EMBEDDING_TYPE', 'open_ai')

SU_URL = env.str('SU_URL', '')
SU_TABLE = env.str('SU_TABLE', '')
SU_TIMEOUT = env.int('SU_TIMEOUT', 60)
SU_PASSWORD = env.str('SU_PASSWORD', '')
SU_SERVICE_KEY = env.str('SU_SERVICE_KEY', '')
SU_MATCH_FUNCTION = env.str('SU_MATCH_FUNCTION', '')

SU_KNOWLEDGE_URL = env.str('SU_KNOWLEDGE_URL', '')
SU_KNOWLEDGE_KEY = env.str('SU_KNOWLEDGE_KEY', '')
SU_KNOWLEDGE_TABLE = env.str('SU_KNOWLEDGE_TABLE', '')
SU_KNOWLEDGE_MATCH_FUNCTION = env.str('SU_KNOWLEDGE_MATCH_FUNCTION', '')

OPEN_BASE_URL = env.str('OPEN_BASE_URL','')
OPEN_AI_TOKEN = env.str('OPEN_AI_TOKEN', '')
OPEN_AI_PROXY = env.str('OPEN_AI_PROXY', '')
OPEN_AI_ORGANIZATION = env.str('OPEN_AI_ORGANIZATION','')
OPEN_AI_MODEL = env.str('OPEN_AI_MODEL','gpt-3.5-turbo-16k-0613')
OPEN_AI_DALLE_URL = env.str('OPEN_AI_DALLE_URL','')

BING_SEARCH_KEY = env.str('BING_SEARCH_KEY','')

TAVILY_API_KEY = env.str('TAVILY_API_KEY', '')
WOLFRAM_APP_ID = env.str('WOLFRAM_APP_ID', '')

TENCENT_SECRET_ID = env.str('TENCENT_SECRET_ID', '')
TENCENT_SECRET_KEY = env.str('TENCENT_SECRET_KEY', '')

BACKEND_URL = env.str('BACKEND_URL', 'http://192.168.1.99:8888')
