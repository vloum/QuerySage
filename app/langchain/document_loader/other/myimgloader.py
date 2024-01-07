import base64
import os
from typing import List
from langchain.schema import HumanMessage
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from app.langchain.document_loader.other.ocr import get_ocr
from app.langchain.utils import get_ChatOpenAI


class RapidOCRLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def img2text(filepath):
            resp = ""
            ocr = get_ocr()
            result, _ = ocr(filepath)
            if result:
                ocr_result = [line[1] for line in result]
                resp += "\n".join(ocr_result)
            return resp

        text = img2text(self.file_path)

        if len(text) == 0:
            text = open_ai_vision(filepath=self.file_path)

        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)

# openai的vision识别图片内容
def open_ai_vision(filepath):
    chat = get_ChatOpenAI(
        model_name='openai-vision',
        temperature=0.8,
        streaming=False)
    ext = os.path.splitext(filepath)[-1].lower()
    base64 = encode_image(image_path=filepath)
    messages = [
        HumanMessage(
            content= [
                {
                    "type": "text",
                    "text": "解释图片信息"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{ext};base64,{base64}"
                    }
                }
            ]
        )
    ]

    result = chat(messages)

    return result.content

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

if __name__ == "__main__":
    loader = RapidOCRLoader(file_path="../../../temp/1704634834_法狗狗-横版-黑色.png")
    docs = loader.load()
    print(docs)
