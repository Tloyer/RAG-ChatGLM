# RAG-ChatGLM
**RAG+ChatGLM结合，为新闻生成摘要**

* 1.dataPreProcess：数据预处理，包括清洗多余信息，提取关键词等 
* 2.get_glm：调用ChatGLM模型接口
* 3.myRag：RAG方法实现，利用data.txt增强检索，调用的是ChatGPT-3.5-turbo
* 4.main：程序的入口
* 5.articles.json：输出结果，包括新闻的id、新闻原文、关键词、预处理后的新闻、生成的摘要等
* 6.ragArticles.json：Rag的输出结果
