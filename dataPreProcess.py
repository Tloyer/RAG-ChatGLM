import re
import jieba
from collections import Counter

def preprocess_text(text):
    """
    文本预处理函数：去重、去除无关内容、文本清理等
    """
    # 合并段落为一个字符串
    text = ' '.join(text)

    # 去重：移除重复的段落或句子
    sentences = list(dict.fromkeys(text.split('。')))  # 中文句号分割句子
    text = '。'.join(sentences)

    # 去除HTML标签
    text = re.sub(r'<[^>]+>', '', text)

    # 去除非中文字符（保留中文、数字和部分标点符号）
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9。，、！？]', '', text)

    return text


def extract_key_info(text):
    # 分句
    sentences = text.split('。')

    # 简单的规则匹配关键信息，可以根据需要更改规则
    date_pattern = re.compile(r'\d{4}年\d{1,2}月\d{1,2}日')
    location_pattern = re.compile(r'(北京|上海|国外|国内|中国|美国|国际|欧洲)')
    person_pattern = re.compile(r'(奥特曼|巴特莱|奥尔特曼|Altman|Murati|雷军|徐鹏|穆拉蒂|熊伟铭|陈磊)')
    event_pattern = re.compile(r'(发布|推出|宣布|上线|开启|公布|参加|举行|召开|举办)')

    # 使用集合来存储不重复的信息
    dates = set()
    locations = set()
    persons = set()
    events = set()

    for sentence in sentences:
        # 提取日期
        dates.update(date_pattern.findall(sentence))
        # 提取地点
        locations.update(location_pattern.findall(sentence))
        # 提取人物
        persons.update(person_pattern.findall(sentence))
        # 提取事件
        events.update(event_pattern.findall(sentence))
        # 将集合转换为列表并存储到key_info
    key_info = {
        'dates': list(dates),
        'locations': list(locations),
        'persons': list(persons),
        'events': list(events)
    }
    return key_info


def remove_duplicates(items):
    """去除重复的项"""
    return list(dict.fromkeys(items))


def summarize_key_info(key_info):
    """总结关键信息"""
    summary = {
        'dates': remove_duplicates(key_info['dates']),
        'locations': remove_duplicates(key_info['locations']),
        'persons': remove_duplicates(key_info['persons']),
        'events': remove_duplicates(key_info['events'])
    }
    return summary

