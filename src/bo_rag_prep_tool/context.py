from pathlib import Path

import numpy as np

from bo_rag_prep_tool.embedding import get_openai_embedding
from bo_rag_prep_tool.utils import read_json


def cosine_similarity(vec1, vec2):
    # Convert lists to numpy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    # Calculate the dot product of the two vectors
    dot_product = np.dot(vec1, vec2)

    # Calculate the norm (magnitude) of each vector
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # Calculate the cosine similarity
    similarity = dot_product / (norm_vec1 * norm_vec2)

    return similarity


def get_context(query: str):
    query_embedding = get_openai_embedding([query])[0]

    context_datas = read_json(Path("resource/ངོས་ཀྱི་ཡུལ་དང་ངོས་ཀྱི་མི་མང་།.json"))

    similarities = []
    # Store top three contexts data for llm generation
    for context_data in context_datas:
        similarity = cosine_similarity(query_embedding, context_data["embedding"])
        similarities.append(
            (similarity, context_data)
        )  # Pair similarity with context data

    # Sort the context data based on the similarity score in descending order
    top_contexts = sorted(similarities, key=lambda x: x[0], reverse=True)[:10]

    # Extract the top 3 context data
    top_three_contexts = [context[1] for context in top_contexts]

    return top_three_contexts
