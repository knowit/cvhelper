from glob import glob
import json
import os

from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb

from split import CVSplitter

def split_all_cvs(path: str):
    splitter = CVSplitter(lang="no")
    for cv_path in glob(path):
        with open(cv_path) as f:
            cv = json.load(f)
            for item in splitter.get_all_splits(cv):
                yield item


def embed_and_insert(path: str):
    chroma_host = os.environ["CHROMA_HOST"]
    chroma_port = os.environ.get("CHROMA_PORT", "9000")
    embeddings = GPT4AllEmbeddings()
    chroma_client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
    vectorstore = Chroma(
        collection_name="cv_no_clean",
        embedding_function=embeddings,
        client=chroma_client,
    )
    text_list = []
    meta_list = []
    for text, meta in split_all_cvs(path):
        text_list.append(text)
        meta_list.append(meta)

    vectorstore.add_texts(text_list, meta_list)