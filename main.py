import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import dataPreProcess
import get_glm

### 自动获取文章内容
def autoFetchContent(urls):
    # 创建浏览器对象
    chrome_driver_path = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    for url in urls:
        driver.get(url)
        time.sleep(5)
        # 找到h1和p所在的位置加入文本
        content_elements = driver.find_elements(By.CSS_SELECTOR, '.article-summary h1, h2, h3, p')
        content = [element.text for element in content_elements]
        articles_content.append(content)
    driver.quit()


### 处理每篇文章
def dataPre(articles_content):
    data = {
        'articles': []
    }
    for i, article in enumerate(articles_content):
        # 文本清理，去除多余内容
        preprocessed_text = dataPreProcess.preprocess_text(article)
        # 提取关键词
        key_info = dataPreProcess.extract_key_info(preprocessed_text)
        # 生成摘要
        abstrct = get_glm.get_glm_response("接下来我会为你发一篇材料，是李希在二十届中央纪委三次全会的工作报告，我需要在阅读它之后写一篇思想汇报，字数在1500字以上，请你为我写完。以下是材料内容：" + preprocessed_text)

        data['articles'].append({
            'article_id': i + 1,
            'raw_article': article,
            'key_info': key_info,
            'processed_article': preprocessed_text,
            'abstrct' : abstrct
        })
    with open('myarticles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # urls = ["https://wallstreetcn.com/articles/3715085", "https://www.thepaper.cn/newsDetail_forward_27372275", "https://m.huxiu.com/article/3023873.html",
    #         "https://www.uisdc.com/gpt-4o", "https://juejin.cn/post/7368701816441307187", "https://www.vivepostwave.com/13359/gpt-4o/",
    #         "https://hao.cnyes.com/post/85542", "https://www.gvm.com.tw/article/112892", "https://www.163.com/dy/article/J24TME8S05118O92.html",
    #         "https://news.sciencenet.cn/htmlnews/2024/5/522621.shtm"]
    urls = ["https://www.xuexi.cn/lgpage/detail/index.html?id=4456034376726455890&item_id=4456034376726455890"]
    articles_content = []

    autoFetchContent(urls)
    dataPre(articles_content)

