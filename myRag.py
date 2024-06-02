OPENAI_API_KEY = "sk-proj-Sgoug5oMJ2oiwEgiUCSuT3BlbkFJEmxktjawVgiWUPIdoYZq"
import dotenv

dotenv.load_dotenv()

import requests
import warnings
from langchain_community.document_loaders import OnlinePDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
import weaviate
from weaviate.embedded import EmbeddedOptions
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from transformers import AutoTokenizer, AutoModel
from peft import get_peft_model, LoraConfig, TaskType


def ragGenAbstract(context):
    loader = OnlinePDFLoader("https://core.ac.uk/download/322982112.pdf")
    data = loader.load()
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

    # 调用模型
    model_name = "/mnt/workspace/cache/chatglm2-6b"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

    warnings.filterwarnings("ignore")

    model.supports_gradient_checkpointing = True  # 节约cuda
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()

    model.config.use_cache = False  # silence the warnings. Please re-enable for inference!

    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM, inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0,
    )

    llm = get_peft_model(model, peft_config)

    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    query = context
    abstract = rag_chain.invoke(query)
    return abstract


if __name__ == '__main__':
    # 打开并读取JSON文件
    with open('articles.json', 'r', encoding='utf-8') as file:
        articles = json.load(file)

    # 遍历每条数据并生成ragAbstract
    for article in articles:
        processed_article = article.get('processed_article', '')

        # 调用摘要生成函数
        rag_abstract = ragGenAbstract(processed_article)

        # 将生成的摘要添加到文章数据中
        article['ragAbstract'] = rag_abstract

    # 将更新后的数据写回JSON文件
    with open('ragArticles.json', 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)