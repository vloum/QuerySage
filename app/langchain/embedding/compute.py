import numpy as np
from typing import List, Tuple
from langchain_community.utils.math import cosine_similarity


def maximal_marginal_relevance(
    query_embedding: List[float],
    embedding_list: List[List[float]],
    lambda_mult: float = 0.5,
    k: int = 4,
) -> List[Tuple[int, float]]:
    """Calculate maximal marginal relevance and return indices with similarities."""

    query_embedding = np.array(query_embedding, dtype=np.float32)
    
    # 空列表或者k值非法时，返回空列表
    if min(k, len(embedding_list)) <= 0:
        return []
    
    # 如果query_embedding是一维的，将其转换为二维
    if query_embedding.ndim == 1:
        query_embedding = np.expand_dims(query_embedding, axis=0)

    similarity_to_query = cosine_similarity(query_embedding, embedding_list)[0]
    most_similar = int(np.argmax(similarity_to_query))
    idxs_with_scores = [(most_similar, similarity_to_query[most_similar])]
    selected = np.array([embedding_list[most_similar]])

    while len(idxs_with_scores) < min(k, len(embedding_list)):
        best_score = -np.inf
        idx_to_add = -1
        similarity_to_selected = cosine_similarity(embedding_list, selected)

        for i, query_score in enumerate(similarity_to_query):
            if i in [idx for idx, _ in idxs_with_scores]:
                continue
            redundant_score = max(similarity_to_selected[i])
            equation_score = lambda_mult * query_score - (1 - lambda_mult) * redundant_score

            if equation_score > best_score:
                best_score = equation_score
                idx_to_add = i

        idxs_with_scores.append((idx_to_add, similarity_to_query[idx_to_add]))
        selected = np.append(selected, [embedding_list[idx_to_add]], axis=0)

    return idxs_with_scores
