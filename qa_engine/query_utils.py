import openai
from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate,
                               SystemMessagePromptTemplate)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from utils import logger
from vectordb import PineconeClient
from vectordb.constants import (EMBEDDING_MODEL, OPENAI_API_KEY,
                                PINECONE_API_KEY, PINECONE_ENV)

from .constants import CHAT_MODEL

openai.api_key = OPENAI_API_KEY


class QAEngine:
    def __init__(self, index_name="xandergpt"):
        self.pinecone_client = PineconeClient(
            pinecone_api_key=PINECONE_API_KEY,
            pinecone_env=PINECONE_ENV
        )

        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL
        )

        self.index_name = index_name

    def _get_docs(
        self,
        query,
        namespace
    ):
        if not self.pinecone_client.index_exists(index_name=self.index_name):
            status, index_name = False, ""
        else:
            status, index_name = True, self.index_name

        if status:
            with get_openai_callback() as cb:
                vectorstore = self.pinecone_client.Pinecone.from_existing_index(
                    index_name=index_name,
                    embedding=self.embeddings,
                    namespace=namespace
                )
        else:
            vectorstore = None

        logger.info(f"vectorstore: {vectorstore}")

        if vectorstore:
            self.docs = vectorstore.similarity_search(
                query, namespace=namespace
            )
        else:
            self.docs = []

    def _convert_messages(self, messages):
        msgs = []

        for message in messages:
            if message["role"] == "assistant":
                msg = AIMessage(content=message["content"])
            elif message["role"] == "user":
                msg = HumanMessage(content=message["content"])
            else:
                msg = SystemMessage(content=message["content"])

            msgs.append(msg)

        return msgs

    def _convert_docs(self, docs):
        return [SystemMessage(content=doc.page_content) for doc in docs]

    def _fetch_past_messages(self, room_id):
        self.past_messages = []

        # if room_id:
        #     if cache.get(f"chatgpt_responses_{room_id}"):
        #         previous_chats = cache.get(f"chatgpt_responses_{room_id}")

        #         if len(previous_chats) > PAST_MESSAGES_LIMIT:
        #             previous_chats = previous_chats[2:]

        #         messages = previous_chats

        #         logger.info(f"Previous {len(messages)} messages:\n{messages}")

    def _get_response(
        self,
        query,
        room_id="",
        docs=[],
        type="open"
    ):
        past_messages = self._convert_messages(self.past_messages)

        logger.info(f"The type of the incoming payload is: {type}")

        if type in ["open", "all"]:
            try:
                llm = ChatOpenAI(
                    temperature=0,
                    verbose=True,
                    model_name=CHAT_MODEL
                )
            except Exception as ex:
                logger.info(f"Error while creating ChatOpenAI: {ex}")

                llm = ChatOpenAI(
                    temperature=0,
                    verbose=True,
                    model_kwargs={
                        "model": CHAT_MODEL
                    }
                )
        else:
            llm = OpenAI(
                model_name=CHAT_MODEL,
                temperature=0,
                verbose=True
            )

        base_prompt_message = """
            The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
        """

        base_prompt = SystemMessagePromptTemplate.from_template(
            base_prompt_message
        )

        docs_prompt_message = """
            Use the following data as CONTEXT to this conversation:
        """

        docs_prompt = SystemMessagePromptTemplate.from_template(
            docs_prompt_message
        )

        converted_docs = self._convert_docs(docs)

        history_prompt_message = """
            These are the previous messages in the conversation for ADDITIONAL CONTEXT:
        """

        history_prompt = SystemMessagePromptTemplate.from_template(
            history_prompt_message
        )

        query_prompt_message = """
            Answer the following query. If the data contains a list of items, please delimit them by a newline character:

            {query}
        """

        query_prompt = HumanMessagePromptTemplate.from_template(
            query_prompt_message
        )

        if type in ["open", "trained"]:
            prompts = [
                base_prompt,
                history_prompt,
                *past_messages,
                query_prompt
            ]
        else:
            prompts = [
                base_prompt,
                docs_prompt,
                *converted_docs,
                history_prompt,
                *past_messages,
                query_prompt
            ]

        logger.info(f"Prompts: {prompts}")

        prompt = ChatPromptTemplate(
            messages=prompts,
            input_variables=["query"]
        )

        if type == "trained":
            prompt = prompt.format(query=query)

            chain = load_qa_chain(
                llm=llm,
                chain_type="stuff",
                verbose=True
            )
        else:
            chain = LLMChain(
                llm=llm,
                verbose=True,
                prompt=prompt
            )

        with get_openai_callback() as cb:
            try:
                if type == "trained":
                    msg = chain.run(input_documents=docs, question=prompt)
                else:
                    msg = chain.run(query=query)
            except Exception as e:
                logger.error(
                    f"Error while running the chain: {e}", exc_info=True
                )

                return False, str(e)

            # if cb.total_tokens >= PAST_MESSAGES_PURGE_TOKEN_LIMIT:
            #     if cache.get(f"chatgpt_responses_{room_id}"):
            #         cache.delete(f"chatgpt_responses_{room_id}")

        return True, msg

    def query_llm(
        self,
        query,
        namespace,
        response_type="trained",
        room_id=""
    ):
        self._fetch_past_messages(room_id)

        if response_type == "open":
            msg_status, msg = self._get_response(
                query=query,
                room_id=room_id
            )

            messages = self.past_messages
            messages.append({"role": "user", "content": query})

            if msg_status:
                messages.append({"role": "assistant", "content": msg})

                # if room_id:
                #     cache.set(f"chatgpt_responses_{room_id}", messages)
        elif response_type == "trained":
            self._get_docs(
                query=query,
                namespace=namespace
            )

            msg_status, msg = self._get_response(
                query=query,
                room_id=room_id,
                docs=self.docs,
                type="trained"
            )

            messages = self.past_messages
            messages.append({"role": "user", "content": query})

            if msg_status:
                messages.append({"role": "assistant", "content": msg})

                # if room_id:
                #     cache.set(f"chatgpt_responses_{room_id}", messages)
        elif response_type == "all":
            self._get_docs(
                query=query,
                namespace=namespace
            )

            msg_status, msg = self._get_response(
                query=query,
                room_id=room_id,
                docs=self.docs,
                type="all"
            )

            messages = self.past_messages
            messages.append({"role": "user", "content": query})

            if msg_status:
                messages.append({"role": "assistant", "content": msg})

                # if room_id:
                #     cache.set(f"chatgpt_responses_{room_id}", messages)
        else:
            msg_status, msg = False, "Invalid response type."

        return msg_status, msg
