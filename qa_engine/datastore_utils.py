from utils import logger
from vectordb import upload_text_to_pinecone, website_text_data


async def add_website_data(urls, index_name, namespace):
    try:
        docs = await website_text_data(urls)
    except Exception as e:
        logger.error(f"Error while getting website data: {e}", exc_info=True)

        return False, str(e)

    vectorstore, error = upload_text_to_pinecone(
        docs=docs, index_name=index_name, namespace=namespace
    )

    if vectorstore:
        return True, None

    return False, error
