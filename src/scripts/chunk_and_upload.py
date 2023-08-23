import os
from tqdm import tqdm
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import argparse


load_dotenv()

data_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

azure_search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
index_name = os.getenv("INDEX_NAME")
model = "text-embedding-ada-002"


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chunk-size",
        dest="chunk_size",
        type=int,
        default=400,
        help="Number of characters per chunk",
    )
    parser.add_argument(
        "--chunk-overlap",
        dest="chunk_overlap",
        type=int,
        default=10,
        help="Number of characters to overlap between chunks",
    )

    return parser.parse_args()


def _list_html_files(path: str):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".html")]


def _upload_file(
    vector_store: AzureSearch,
    file_path: str,
    chunk_size: int = 400,
    chunk_overlap: int = 10
):
    loader = UnstructuredHTMLLoader(file_path)

    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)

    vector_store.add_documents(docs)


def main(
    vector_store: AzureSearch,
    chunk_size: int = 400,
    chunk_overlap: int = 10
):
    html_files = _list_html_files(data_path)

    print("uploading files")
    for file_path in tqdm(html_files):
        _upload_file(vector_store, file_path, chunk_size, chunk_overlap)


if __name__ == "__main__":
    args = _get_args()
    chunk_size = args.chunk_size
    chunk_overlap = args.chunk_overlap

    print("initializing vector store")
    embeddings: OpenAIEmbeddings = OpenAIEmbeddings(
        deployment=model,
        chunk_size=1)
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=azure_search_endpoint,
        azure_search_key=azure_search_key,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    main(vector_store, chunk_size, chunk_overlap)
