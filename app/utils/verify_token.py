import base64
import re
import threading
from fastapi import HTTPException, Header
from contextvars import ContextVar

from app.utils.backend_ability import get_user_by_backend

token_local = threading.local()

# 创建上下文变量
token_var: ContextVar[str] = ContextVar("token", default="")

async def verify_token(Authorization: str = Header(None), authorization: str = Header(None)):
  token = Authorization or authorization
  print('token:', token)

  token_var.set(token)

  if not token:
      raise HTTPException(status_code=401, detail="Token is missing")

  pattern = re.compile(r'[an]k-(.*)')
  splits = pattern.match(token)
  
  if not splits:
      raise HTTPException(status_code=401, detail="Invalid token")
  
  user_id = splits.group(1)

  # 这里需要接用户系统的接口，验证Token的有效性
  is_has = get_user_by_backend(user_id)
  if not is_has:
      raise HTTPException(status_code=401, detail="user not found")
  return True
    
# 用于agent 的 token
def create_agent_token():
    if token_var.get() == '':
        return ''
    token = 'vlou-'+ token_var.get() + '-vlou'
    return token
def parse_agent_token(query: str):
    token = re.compile(r'vlou-(.*)-vlou').search(query)
    if not token:
        return ''
    return token.group(1)
def remove_agent_token(query: str):
    return re.sub(r'vlou-(.*)-vlou', '', query)