import os
os.environ["OPENAI_API_KEY"] = ""
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


def ragGenerateAbstract(context):
    # 加载数据
    loader = TextLoader("./data.txt", encoding='utf-8')
    documents = loader.load()
    # 创建分割器
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
    # 拆分文档
    documents = text_splitter.split_documents(documents)
    # 将数据进行向量化
    model_name = "moka-ai/m3e-base"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    embedding = HuggingFaceBgeEmbeddings(
        model_name = model_name,
        model_kwargs = model_kwargs,
        encode_kwargs = encode_kwargs
    )

    persist_directory = 'db'
    db = Chroma.from_documents(documents, embedding, persist_directory=persist_directory)

    # 检索
    retriever = db.as_retriever()
    # 增强
    template = """
        你是一个聊天助手，请根据以上内容，和我聊天。
    """

    prompt = ChatPromptTemplate.from_template("请根据以下内容生成一片摘要："+context)
    print("prompt:")
    print(prompt)

    llm = ChatOpenAI(model = "gpt-3.5-turbo",base_url="https://api.xty.app/v1")

    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return rag_chain.invoke("请你根据以下内容生成一篇摘要。" )

if __name__ == '__main__':

    # 从环境变量中获取 OpenAI API 密钥
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY 环境变量未设置")

    # 配置 OpenAI 客户端
    openai_client = OpenAI(api_key=openai_api_key)
    # 打开并读取JSON文件
    with open('articles.json', 'r', encoding='utf-8') as file:
        context = json.load(file)
    articles = context["articles"]
    # 遍历每条数据并生成ragAbstract
    for article in articles:
        processed_article = article.get('processed_article', '')
        print(processed_article)
        # 调用摘要生成函数
        rag_abstract = ragGenerateAbstract(processed_article)
        print(rag_abstract)

        # 将生成的摘要添加到文章数据中
        article['ragAbstract'] = rag_abstract

    # 将更新后的数据写回JSON文件
    with open('ragArticles.json', 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

