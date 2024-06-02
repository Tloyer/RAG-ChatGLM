import requests
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.prompts import ChatPromptTemplate

from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser



def MyRAG():
    loader = TextLoader('./大语言模型综述.pdf')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    client = weaviate.Client(
        embedded_options=EmbeddedOptions()
    )

    vectorstore = Weaviate.from_documents(
        client=client,
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        by_text=False
    )

    retriever = vectorstore.as_retriever()

    template = """ 你是一个文本摘要生成助手，请结合以下检索增强的文本和我的输入，为我生成精炼的摘要。你的输出格式要以“摘要：”开头 """
    prompt = ChatPromptTemplate.from_template(template)

    print(prompt)

    # rag_chain = (
    #         {"context": retriever, "question": RunnablePassthrough()}
    #         | prompt
    #         | llm
    #         | StrOutputParser()
    # )
    #
    # query = "What did the president say about Justice Breyer"
    # rag_chain.invoke(query)