
import requests
from config import BACKEND_URL

headers = {
    'token': f'eyJhbGciOiJSUzI1NiJ9.dmxvdQ.oCQ9v_Cc0kKma6d2WeTs287MJDJjt9KlCZSp3lYz75cA9STCJJYQZVm4Q0C-zlyWiLpt2wDUvbCsbh4LCdH6107vNjH58IRvEAn-dWriNiH9DaAmMMpjjLViriNIh7G8Ps2IRYeiIMCXF97_pJQRWEXoudkczmCNXbTdnSb6Bh3R6BGgm_TIHEFMg3Vc22RbM6RzxBmBKJgEco1Z-pfYLzcLjRCJewPzG3EKgb3xkrdv4umuOi8JvZ6acXV_CEE_sArdLqIGNXlKcWnnJPYropumw4OFivlwX3_li79a1laHdreBjdrRb0kZsa3QrJUGBdk64-HTlX9jdGV3oEbWyA'
}

def save_cache_by_backend(key: str, value: str) -> bool:
    try:
        requests.post(f'{BACKEND_URL}/api/cache', json={ 'key': key, 'value': value, 'exp': 5 }, headers=headers)
    except Exception as e:
        print('缓存失败--',e)
        return False
    
    return True

def get_cache_by_backend(key: str) -> str:
    try:
        response = requests.post(f'{BACKEND_URL}/api/cache', json={ 'key': key }, headers=headers)
        return response.json().get('value', '')
    except Exception as e:
        print('获取缓存失败--',e)
        return ''

# 验证用户是否存在
def get_user_by_backend(user_id: str) -> bool:
    try:
        response = requests.get(f'{BACKEND_URL}/api/user/{user_id}', headers=headers)
        return response.json().get('id', False)
    except Exception as e:
        print('获取用户失败--',e)
        return False
    