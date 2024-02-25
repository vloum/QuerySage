import os
import time
import uuid
import aiofiles
from typing import Any, Callable, Dict, List
from fastapi import UploadFile, File, Form, Depends
from concurrent.futures import ThreadPoolExecutor
from app.utils.tencent_cos import cos_upload_file, parsing_path_file

from configs.kb_config import KB_ROOT_PATH


async def upload_files_dependency(knowledge_name: str = Form(...), files: List[UploadFile] = File(...)):
    data = {"knowledge_name": knowledge_name}
    files_info = []

    temp_dir = os.path.join(os.getcwd(), f'{KB_ROOT_PATH}/{knowledge_name}')

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for file in files:
        file_id = uuid.uuid4()
        file_path, file_name = parsing_path_file(file.filename, file_id)

        # unique_filename = f"{int(time.time())}_{file.filename}"
        file_path = os.path.join(temp_dir, file_name)

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        files_info.append({'filename': file_name, 'origin_name': file.filename, 'file_path': file_path})

        # 上传到腾讯云
        cos_upload_file(file_path, file_id)

    if files_info:
        data['files'] = files_info

    return data

# 判断文件后缀返回对应的 md 格式
def get_md_format(ext: str, file_path: str, description: str, file_name: str):
    if ext in ['png', 'jpg', 'jpeg', 'gif']:
        return f'![{description}]({file_path})'
    return f'[{file_name}]({file_path})'


def run_tasks_in_thread_pool(items: List[Dict], function: Callable[..., Any]) -> List[Any]:
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda item: function(**item), items)
        return list(results)