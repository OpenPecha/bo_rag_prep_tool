import os
import time
from pathlib import Path
from typing import List

import cohere
from tqdm import tqdm

from bo_rag_prep_tool.utils import read_json, write_json

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("Please set COHERE_API_KEY environment variable")

co = cohere.ClientV2(api_key=cohere_api_key)


def get_cohere_embeddings(
    texts: List[str],
    model="embed-multilingual-light-v3.0",
    input_type="search_document",
):
    """
    Input: List of string, model name, input type
    Restriction: - Max number of input per call is 96
                 - 100 calls per minute
                 - 1000 calls per month
                 - 100000 tokens per minute
    """
    output = co.embed(
        texts=texts, model=model, input_type=input_type, embedding_types=["float"]
    )
    return output.embeddings.float


def populate_embeddings(data_with_metadata_file: Path, output_path: Path):
    json_data = read_json(data_with_metadata_file)
    num_of_data = len(json_data)
    api_limit = 96

    for i in tqdm(
        range(1, num_of_data + 1, api_limit),
        desc="Getting 96 input's  embeddings at a time",
    ):
        curr_texts = []
        # Get texts from json data
        for j in range(i, i + api_limit):
            if j > num_of_data:
                break
            curr_texts.append(json_data[j - 1]["content"])

        # Get embeddings and assign the embeddings to the texts
        time.sleep(20)
        embeddings = get_cohere_embeddings(curr_texts)
        for j in range(i, i + api_limit):
            if j > num_of_data:
                break
            json_data[j - 1]["embedding"] = embeddings[j - i]

    output_file = output_path / "embeddings.json"
    write_json(output_file, json_data)
