# import load
# from load import pdf_text_dict
import os
import openai
import pinecone
import json
import itertools

# define a function to pass the output of the pdf_text_dict to the OpenAI embedding API to get the embeddings of the text.

docs = "Hello, world!"


def write(docs):
    # Set the OpenAI API key
    openai.api_key = os.environ["OPENAI"]

    # Generate text embeddings using OpenAI
    response = openai.Embedding.create(model="text-embedding-ada-002", input=docs)
    embeddings = [record["embedding"] for record in response["data"]]

    # print(embeddings)

    # Initialize Pinecone
    pinecone.init(api_key=os.environ["PINECONE"], environment="us-west4-gcp-free")

    # Define the index name
    index_name = "mojave"

    # Create or connect to the Pinecone index
    # if index_name not in pinecone.list_indexes():
    #     pinecone.create_index(index_name, dimension=len(embeddings[0]), metric="cosine")
    index = pinecone.Index(index_name)

    # Batch processing and indexing
    def chunks(vectors, batch_size=100):
        it = iter(vectors)
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(it, batch_size))

    for writable in chunks(embeddings, batch_size=100):
        index.upsert(vectors=zip(range(len(writable)), writable))


write(docs)


# for file_name, text in pdf_text_dict.items():
#     print(f"File: {file_name}\nText: {text}\n")
