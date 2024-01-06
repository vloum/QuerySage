import os
import time
import aiofiles
from typing import Any, Callable, Dict, List
from fastapi import UploadFile, File, Form, Depends
from concurrent.futures import ThreadPoolExecutor

from configs.kb_config import KB_ROOT_PATH


async def upload_files_dependency(knowledge_name: str = Form(...), files: List[UploadFile] = File(...)):
    data = {"knowledge_name": knowledge_name}
    files_info = []

    temp_dir = os.path.join(os.getcwd(), f'{KB_ROOT_PATH}/{knowledge_name}')

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for file in files:
        unique_filename = f"{int(time.time())}_{file.filename}"
        file_path = os.path.join(temp_dir, unique_filename)

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        files_info.append({'filename': unique_filename, 'file_path': file_path})

    if files_info:
        data['files'] = files_info

    return data

def run_tasks_in_thread_pool(items: List[Dict], function: Callable[..., Any]) -> List[Any]:
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda item: function(**item), items)
        return list(results)