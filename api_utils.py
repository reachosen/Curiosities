import requests
import xml.etree.ElementTree as ET
import pandas as pd

def get_arxiv_articles(query, max_results=10):
    base_url = 'http://export.arxiv.org/api/query'
    payload = {
        'search_query': query,
        'start': 0,
        'max_results': max_results
    }
    response = requests.get(base_url, params=payload)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_arxiv_xml(xml_data):
    root = ET.fromstring(xml_data)
    namespaces = {
        'default': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    articles = []
    for entry in root.findall('default:entry', namespaces=namespaces):
        article = {}
        article['id'] = entry.find('default:id', namespaces=namespaces).text
        article['title'] = entry.find('default:title', namespaces=namespaces).text
        article['summary'] = entry.find('default:summary', namespaces=namespaces).text
        articles.append(article)

    return pd.DataFrame(articles)
