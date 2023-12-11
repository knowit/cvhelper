from glob import glob
import os
import sys
from cvpartner_client import CVPartnerClient
import json
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
import chromadb
from split import CVSplitter


def main():
    # Get token and download path from command line arguments
    token = os.environ["CVPARTNER_TOKEN"]
    download_path = sys.argv[1]

    # Create an instance of CVPartnerClient
    client = CVPartnerClient(token=token)

    # Download all CVs
#    client.download_all_cvs(download_path)
    client.download_cv("5b8fd663c86c13111ac8eb0f","5b8fd663c86c13111ac8eb10",download_path)
    embed_and_insert(f"{download_path}/5b8fd663c86c13111ac8eb0f.json")

def split_all_cvs(path: str):
    splitter = CVSplitter(lang="no")
    for cv_path in glob(path):
        with open(cv_path) as f:
            cv = json.load(f)
            for item in splitter.get_all_splits(cv):
                yield item


def embed_and_insert(path: str):
    chroma_host = os.environ["CHROMA_HOST"]
    chroma_port = os.environ.get("CHROMA_PORT", "8000")
    embeddings = GPT4AllEmbeddings()
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
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

if __name__ == "__main__":
    main()
