import pinecone
import os
import openai
from tqdm.auto import tqdm
import datetime
from time import sleep

#  initialize the openai api key
# openai.api_key = os.environ["OPENAI"]
# embed_model = "text-embedding-ada-002"
# res = openai.Embedding.create(input=["hi"], engine=embed_model)
# print(res.keys())
# print(res["data"])
# # print(len(res["data"][0]["embedding"]))


# initialize the pinecone api key
index_name = "mojave"
# dimension = len(res["data"][0]["embedding"])
dimension = 1536

# initializing connection
pinecone.init(api_key=os.environ["PINECONE"], environment="us-west4-gcp-free")

# check if index exists
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=dimension, metric="cosine")

# connect to index
index = pinecone.Index(index_name)
# view index stats
# print(index.describe_index_stats())

batch_size = 100
chunks = [i for i in range(0, 1000)]

for i in tqdm(range(0, len(chunks), batch_size)):
    # find end of batch
    i_end = min(len(chunks), i + batch_size)
    meta_batch = chunks[i:i_end]
    print(meta_batch)
    try:
        res = openai.Embedding.create(input=meta_batch, engine="text-embedding-ada-002")
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(
                    input=meta_batch, engine="text-embedding-ada-002"
                )
                done = True
            except:
                pass
    embeds = [record["embedding"] for record in res["data"]]
    print(embeds)
    # for batch in meta_batch:
    #     to_upsert = list(zip(batch, embeds))
    # print(to_upsert)
    # index.upsert(vectors=to_upsert)
