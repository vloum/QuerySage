import os
import time
from typing import Callable, Dict, List
from flask import request, current_app
from concurrent.futures import ThreadPoolExecutor

def get_data():
    return request.args.to_dict()

def post_data():
    content_type = request.headers.get('Content-Type', '')

    if 'multipart/form-data' in content_type:
        return handle_form_data()
    elif 'application/json' in content_type:
        return request.get_json() or {}
    else:
        raise ValueError(f'Unsupported Content-Type: {content_type}')

def handle_form_data():
    data = request.values.to_dict()  # 合并表单和查询参数
    files_info = []  # 用于存储所有文件的信息

    # 检查并处理所有上传的文件
    for file_key in request.files:
        file = request.files[file_key]
        temp_dir = os.path.join(os.getcwd(), 'temp')

        # 确保临时目录存在
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        unique_filename = f"{int(time.time())}_{file.filename}"
        file_path = os.path.join(temp_dir, unique_filename)
        file.save(file_path)  # 保存文件到临时目录

        # 将文件信息添加到列表中
        files_info.append({'filename': file.filename, 'file_path': file_path})

    # 如果有文件被上传，更新data字典
    if files_info:
        data['files'] = files_info

    return data


def process_tasks(items: List[Dict], function: Callable[[Dict], Dict]) -> List[Dict]:
    app = current_app._get_current_object()

    def task_wrapper(item):
        with app.app_context():
            return function(item)

    with ThreadPoolExecutor() as executor:
        # 使用 map 方法并行处理每个项目
        results = executor.map(task_wrapper, items)
        return list(results)