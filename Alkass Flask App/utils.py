import openai
from langchain.chains import RetrievalQA
from langchain.llms.openai import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from system import Prompts


class ChatBotSummarizer:
    def __init__(self, openai_api_key, openai_api_base, openai_api_type, openai_api_version, openai_deployment_name):
        self.api_key         = openai_api_key
        self.api_base        = openai_api_base
        self.api_type        = openai_api_type
        self.api_version     = openai_api_version
        self.deployment_name = openai_deployment_name

    def initialize_openai(self):
        openai.api_key     = self.api_key
        openai.api_base    = self.api_base
        openai.api_type    = self.api_type
        openai.api_version = self.api_version

    def initialize_azure_openai(self):
        llm = AzureOpenAI(
            temperature=0.3,
            max_tokens=4096,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base,
            openai_api_type=self.api_type,
            openai_api_version=self.api_version,
            deployment_name=self.deployment_name
        )
        # llm = AzureChatOpenAI(
        #     temperature        = 0.3,
        #     max_tokens         = 4096,
        #     openai_api_key     = self.api_key,
        #     openai_api_base    = self.api_base,
        #     openai_api_type    = self.api_type,
        #     openai_api_version = self.api_version,
        #     deployment_name    = self.deployment_name
        # )
        return llm

    def chat_and_summarize(self, text):
        # Chat with OpenAI
        chat_response = self.openai_chat_completion(text)

        # Summarize using Langchain
        summary_result = self.langchain_summarize(chat_response)

        return chat_response, summary_result

    def openai_chat_completion(self, text):
        self.initialize_openai()

        system_prompt = Prompts().summarizer()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            engine=self.deployment_name
        )

        return response['choices'][0]['message']['content']

    def langchain_summarize(self, text):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts         = text_splitter.split_text(text)

        embeddings    = OpenAIEmbeddings()
        db            = Chroma.from_texts(texts, embeddings)

        retriever     = db.as_retriever(
            search_type="similarity", search_kwargs={"k": 1})
        llm = self.initialize_azure_openai()
        qa = RetrievalQA.from_chain_type(
            llm=llm, chain_type="map_reduce", retriever=retriever)
        query = Prompts().summarizer()
        result = qa.run(query)
        return result
