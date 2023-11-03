import os

import openai
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.llms.openai import AzureOpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter


load_dotenv()


def openai_chat_completion(text: str) -> str:
    # setup the OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")

    messages = [
        {"role": "system", "content": "You are a very good intelligent bot. You are given a news article of a sports broadcasting company and you have to summarize it within 2 to 3 sentences. And, don't put the whole article in the summary. Just put the main points of the article. You can also add your own words in the summary."},
        {"role": "user", "content": text},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        engine=deployment_name
    )

    return response['choices'][0]['message']['content']


def langchain_summarize(text: str) -> str:
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(text)
    # select the embeddings
    # embeddings = OpenAIEmbeddings(chunk_size = 1, model_kwargs = {"reduce_k_below_max_tokens": True})
    # embeddings = OpenAIEmbeddings(chunk_size = 1)
    embeddings = OpenAIEmbeddings()
    # create the vectorstore to use as the index
    db = Chroma.from_texts(texts, embeddings)
    # expose this index in a retriever interface
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 1})
    # create a chain to answer questions
    llm = AzureOpenAI(
        temperature=0.3,
        max_tokens=4096,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        openai_api_type=os.getenv("OPENAI_API_TYPE"),
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME")
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="map_reduce",
        retriever=retriever,
        # return_source_documents = True
    )
    query = "You are a very good intelligent bot. You are given a news article and you have to summarize it within 2 to 3 sentences. And, don't put the whole article in the summary. Just put the main points of the article. You can also add your own words in the summary."
    # result = qa({"query": query})
    result = qa.run(query)
    return result



class ChatBotSummarizer:
    def __init__(self):
        load_dotenv()
        self.api_key         = os.getenv("OPENAI_API_KEY")
        self.api_base        = os.getenv("OPENAI_API_BASE")
        self.api_type        = os.getenv("OPENAI_API_TYPE")
        self.api_version     = os.getenv("OPENAI_API_VERSION")
        self.deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")

    def initialize_openai(self):
        openai.api_key     = self.api_key
        openai.api_base    = self.api_base
        openai.api_type    = self.api_type
        openai.api_version = self.api_version

    def initialize_azure_openai(self):
        llm = AzureOpenAI(
            temperature        = 0.3,
            max_tokens         = 4096,
            openai_api_key     = self.api_key,
            openai_api_base    = self.api_base,
            openai_api_type    = self.api_type,
            openai_api_version = self.api_version,
            deployment_name    = self.deployment_name
        )
        return llm

    def chat_and_summarize(self, text):
        # Chat with OpenAI
        chat_response = self.openai_chat_completion(text)

        # Summarize using Langchain
        summary_result = self.langchain_summarize(chat_response)

        return chat_response, summary_result

    def openai_chat_completion(self, text):
        self.initialize_openai()
        messages = [
            {"role": "system", "content": "You are a very good intelligent bot. You are given a news article of a sports broadcasting company and you have to summarize it within 2 to 3 sentences. And, don't put the whole article in the summary. Just put the main points of the article. You can also add your own words in the summary."},
            {"role": "user", "content": text},
        ]
        response = openai.ChatCompletion.create(
            model    = "gpt-3.5-turbo",
            messages = messages,
            engine   = self.deployment_name
        )

        return response['choices'][0]['message']['content']

    def langchain_summarize(self, text):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(text)
        embeddings = OpenAIEmbeddings()
        db = Chroma.from_texts(texts, embeddings)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
        llm = self.initialize_azure_openai()
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="map_reduce", retriever=retriever)
        query = "You are a very good intelligent bot. You are given a news article and you have to summarize it within 2 to 3 sentences. And, don't put the whole article in the summary. Just put the main points of the article. You can also add your own words in the summary."
        result = qa.run(query)
        return result

