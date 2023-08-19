# import load
# from load import pdf_text_dict
# import os
# import openai
# import pinecone
# import json
# import itertools
# import numpy as np

# # define a function to pass the output of the pdf_text_dict to the OpenAI embedding API to get the embeddings of the text.

# docs = "Hello, world!"


# def write(docs):
#     # Set the OpenAI API key
#     openai.api_key = os.environ["OPENAI"]

#     # Generate text embeddings using OpenAI
#     response = openai.Embedding.create(model="text-embedding-ada-002", input=docs)
#     embeddings = [record["embedding"] for record in response["data"]]

#     # print(embeddings)

#     # Initialize Pinecone
#     pinecone.init(api_key=os.environ["PINECONE"], environment="us-west4-gcp-free")

#     # Define the index name
#     index_name = "mojave"

#     # Create or connect to the Pinecone index
#     # if index_name not in pinecone.list_indexes():
#     #     pinecone.create_index(index_name, dimension=len(embeddings[0]), metric="cosine")
#     index = pinecone.Index(index_name)

#     # Batch processing and indexing
#     def chunks(vectors, batch_size=100):
#         it = iter(vectors)
#         chunk = tuple(itertools.islice(it, batch_size))
#         while chunk:
#             yield chunk
#             chunk = tuple(itertools.islice(it, batch_size))

#     for writable in chunks(embeddings, batch_size=100):
#         index.upsert(vectors=writable)


# write(docs)


# # for file_name, text in pdf_text_dict.items():
# #     print(f"File: {file_name}\nText: {text}\n")
# import pinecone
# import os
# import openai

# # Set the OpenAI API key
# openai.api_key = os.environ["OPENAI"]

# # Define the input text
# docs = "Hello"

# # Generate text embeddings using OpenAI
# response = openai.Embedding.create(model="text-embedding-ada-002", input=docs)
# embeddings = [record["embedding"] for record in response["data"]]
# # embeddings = response["data"][0]["embedding"]

# embedding = list(zip(embeddings))

# # Initialize Pinecone with the API key
# pinecone.init(api_key=os.environ["PINECONE"], environment="us-west4-gcp-free")

# # Define the index name
# index_name = "mojave"
# dimension = len(response["data"][0]["embedding"])

# # Create or connect to the Pinecone index
# # if index_name not in pinecone.list_indexes():
# #     pinecone.create_index(index_name, dimension=dimension, metric="cosine")
# index = pinecone.Index(index_name)


# # Upsert the embeddings
# index.upsert(vectors=embedding)

import pinecone
import os
import openai

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI"]

# Define the input text
docs = "Hello"

# Generate text embeddings using OpenAI
response = openai.Embedding.create(model="text-embedding-ada-002", input=docs)
embeddings = [record["embedding"] for record in response["data"]]

# Initialize Pinecone with the API key
pinecone.init(api_key=os.environ["PINECONE"], environment="us-west4-gcp-free")

# Define the index name
index_name = "mojave"
dimension = len(response["data"][0]["embedding"])

# Create or connect to the Pinecone index
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(index_name, dimension=dimension, metric="cosine")
index = pinecone.Index(index_name)

# Upsert the embeddings
# index.upsert(vectors=embeddings)
# Upsert the embeddings directly
for i, embedding in enumerate(embeddings):
    index.upsert(ids=[f"id-{i}"], vectors=[embedding])


# # Batch processing and indexing
# def chunks(iterable, batch_size=100):
#     it = iter(iterable)
#     chunk = tuple(itertools.islice(it, batch_size))
#     while chunk:
#         yield chunk
#         chunk = tuple(itertools.islice(it, batch_size))


# vector_dim = 1536
# vector_count = 10000

# example_data_generator = map(
#     lambda i: (f"id-{i}", [random.random() for _ in range(vector_dim)]),
#     range(vector_count),
# )
# print(example_data_generator)

# for writable in chunks(embeddings, batch_size=100):
#     index.upsert(vectors=writable)
