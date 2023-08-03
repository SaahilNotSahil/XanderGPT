
import ssl

import requests
from langchain.callbacks import get_openai_callback
from langchain.embeddings.openai import OpenAIEmbeddings

from utils import logger

from .client import PineconeClient
from .constants import (EMBEDDING_MODEL, OPENAI_API_KEY, PINECONE_API_KEY,
                        PINECONE_ENV)


def disable_ssl_warning():
    requests.packages.urllib3.disable_warnings()

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


def upload_text_to_pinecone(
    docs,
    index_name,
    namespace
):
    logger.info("Inside the upload_text_to_pinecone method of utils")

    vectorstore, error = None, None

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    pinecone_client = PineconeClient(
        pinecone_api_key=PINECONE_API_KEY,
        pinecone_env=PINECONE_ENV
    )

    try:
        vectorstore = pinecone_client.Pinecone.from_documents(
            documents=docs,
            embedding=embeddings,
            index_name=index_name,
            namespace=namespace
        )

        logger.info(f"Vectorstore: {vectorstore}")
    except Exception as ex:
        logger.error(
            f"The error occurred in upload_text_to_pinecone is: {ex}",
            exc_info=True
        )

        error = f"Error in uploading website text to pinecone: {str(ex)}"

    return vectorstore, error


def upload_pdf_to_pinecone(
    pages,
    index_name,
    namespace
):
    logger.info("Inside the upload_pdf_to_pinecone method of utils")

    vectorstore, error = None, None

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    pinecone_client = PineconeClient(
        pinecone_api_key=PINECONE_API_KEY,
        pinecone_env=PINECONE_ENV
    )

    try:
        with get_openai_callback() as cb:
            vectorstore = pinecone_client.Pinecone.from_documents(
                documents=pages,
                embedding=embeddings,
                index_name=index_name,
                namespace=namespace
            )
    except Exception as ex:
        logger.error(f"The error occurred in upload_pdf_to_pinecone is: {ex}")

        error = f"Error in uploading pdf to pinecone: {str(ex)}"

    return vectorstore, error


def create_pdf_from_gdoc(gdocs, path):
    logger.info("Inside the create_pdf_from_gdoc method of utils")

    doc_paths = []

    for gdoc in gdocs:
        doc_link = gdoc.get("gdoc_link")
        doc_name = gdoc.get("gdoc_name").replace(" ", "_") + ".pdf"

        try:
            doc_id = doc_link.split('/')[5]

            doc_url = \
                f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"

            file_path = f"{path}{doc_name}"

            with open(file_path, "wb") as f:
                f.write(requests.get(doc_url).content)

            doc_paths.append(doc_name)
        except Exception as ex:
            logger.error(f"Error in creating PDF file: {ex}")

    return doc_paths


def delete_namespace_from_pinecone(
    index_name,
    namespace
):
    logger.info("Inside the delete_namespace_from_pinecone method of utils")

    pinecone_client = PineconeClient(
        pinecone_api_key=PINECONE_API_KEY,
        pinecone_env=PINECONE_ENV
    )

    index = pinecone_client.get_index(index_name)

    logger.info(f"Index: {index}")

    res = index.delete(
        delete_all=True,
        namespace=namespace
    )

    return len(res.items()) == 0
