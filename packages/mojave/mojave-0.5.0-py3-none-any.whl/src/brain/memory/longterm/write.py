# import load
# from load import pdf_text_dict
import os
import openai
import pinecone
import json

# define a function to pass the output of the pdf_text_dict to the OpenAI embedding API to get the embeddings of the text.

docs = "Hello, world!"


def write(docs):
    # Set the OpenAI API key
    openai.api_key = os.environ["OPENAI"]

    # Generate text embeddings using OpenAI
    response = openai.Embedding.create(model="text-embedding-ada-002", input=docs)
    embeddings = [record["embedding"] for record in response["data"]]

    print(embeddings)


write(docs)


# for file_name, text in pdf_text_dict.items():
#     print(f"File: {file_name}\nText: {text}\n")
