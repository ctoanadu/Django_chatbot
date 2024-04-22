import logging
import os

import dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()


def load_csv_url_from_directory(data_source_dir: str):
    """
    Load CSV files from the datastore directory using CSV loader.

    Args:
    - directory (str): Path to the datastore directory containing CSV files.

    Returns:
    - list: List of CSVLoader instances.
    """
    loader_list = []
    for filename in os.listdir(data_source_dir):
        if filename.endswith(".csv"):
            file_path = f"{data_source_dir}/{filename}"
            loader_list.append(CSVLoader(file_path=file_path))
    return loader_list


def create_question_answering_chain(data_source_dir: str):
    """
    Create a question answering chain using loaded CSV files and leveraging GPT.

    Args:
    - directory (str): Path to the directory containing CSV files.

    Returns:
    - RetrievalQA: Question answering chain.
    """
    loaders = load_csv_url_from_directory(data_source_dir)
    
    #Use a vector index to chunk, create embeddings and store in vectordb
    index_creator = VectorstoreIndexCreator()
    docsearch = index_creator.from_loaders(loaders)

    # Create question-answering chain
    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),
        chain_type="stuff",
        retriever=docsearch.vectorstore.as_retriever(),
        input_key="question",
    )
    return chain
