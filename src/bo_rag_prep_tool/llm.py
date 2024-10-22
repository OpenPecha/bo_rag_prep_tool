import os

import anthropic

from bo_rag_prep_tool.context import get_context

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set ANTHROPIC_API_KEY environment variable")


def get_claude_response(prompt: str):
    # Initialize the client with your API key
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Create a message request
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",  # Specify the model version
        max_tokens=1000,  # Set maximum tokens for the response
        temperature=0.5,  # Adjust randomness of responses (0.0 for deterministic)
        system="You are a helpful assistant.",  # System message for context
        messages=[{"role": "user", "content": prompt}],
    )

    # Print the response content
    return response.content[0].text


def get_answer(query: str):
    contexts = get_context(query)
    context_texts = "\n\n".join([context["content"] for context in contexts])

    prompt = f"""
    Your task is to respond to the question based on the provided context.

    Strictly follow these guidelines when answering the questions:

    - Answer the question based on the given contexts (some of which might be irrelevant).
    - Give me a short but informative and pleasant answer.
    - Speak in plain tibetan.
    - Be careful of the language, ensuring it is respectful and appropriate.
    - If you dont have a proper answer from contexts,respond with "ང་ལ་དེའི་ལན་འདེབས་རྒྱུའི་གྲངས་ཐོ་འདང་ངེས་ཤིག་མེད།."

    Question: {query}
    Contexts: {context_texts}

    """
    answer = get_claude_response(prompt)
    return answer
