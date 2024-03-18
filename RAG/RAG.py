from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests


def generate_text(prompt, api_key, endpoint):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        # 'max_tokens': 2048,  # You can set a maximum token limit
        'temperature': 0.7,
        'top_p': 0.5,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0,
        #'stop': ["\n", ".", "!", "?"],  # Tokens to stop at end of sentences
        'n': 1
    }
    print(data['messages'][1]['content'])
    response = requests.post(endpoint, headers=headers, json=data)
    # print("response : ", response.json())
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.text)
        return None


def retrieve_documents(query, documents):
    retriever_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    # Encode the query and documents
    query_embedding = retriever_model.encode(query, convert_to_tensor=True)
    doc_embeddings = retriever_model.encode(documents, convert_to_tensor=True)

    # Calculate cosine similarity between query and documents
    similarities = cosine_similarity(query_embedding.cpu().detach().numpy().reshape(1, -1),
                                     doc_embeddings.cpu().detach().numpy())

    # Get the indices of top 10 most similar documents
    top_n_indices = np.argsort(similarities[0])[-10:][::-1]

    # Get the top n most similar documents
    top_n_documents = [documents[idx] for idx in top_n_indices]

    return top_n_documents
