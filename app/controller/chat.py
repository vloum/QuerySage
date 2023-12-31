

from app.langchain.chatModels import Chat
from app.langchain.vector.supabase import Supabase

class ChatClass(object):

    # 法律问答
    @staticmethod
    def law(query: str):
        search_documents = Supabase.max_marginal_relevance_search(query=query)

        chat_result = Chat.start(query=query, documents=search_documents)

        laws = []

        for document in search_documents:
            # 使用列表推导式和join来构建标题
            title_parts = [document.metadata.get(f'Header{i}', '') for i in range(6)]
            title = '-'.join(filter(None, title_parts))  # 过滤掉空字符串

            laws.append({
                'title': title,
                'law': document.page_content
            })

        return { 'result': chat_result, 'laws': laws}


ControllerChat = ChatClass()
