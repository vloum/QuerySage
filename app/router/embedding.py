from flask import Blueprint
import numpy as np
from app.langchain.embedding import Embedding
from app.langchain.embedding.compute import maximal_marginal_relevance
from app.utils import post_data

embedding_blueprint = Blueprint('embedding', __name__)

@embedding_blueprint.route('/', methods=['GET'])
def hello_world_embedding():
    return "<p>Hello, World embedding!</p>"

@embedding_blueprint.route('/decode', methods=['POST'])
def decode():
    body = post_data()
    
    content_embedding = Embedding.beg().embed_query(body.get('content', ''))
    query_embedding = Embedding.beg().embed_query(body.get('query', ''))

    similarity = maximal_marginal_relevance(query_embedding, embedding_list=[content_embedding], lambda_mult=0)

    return { 'code': 200 }, 200