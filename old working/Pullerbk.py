import requests
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

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

def rank_abstracts_by_similarity(abstracts, ref_document):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    ref_embedding = model.encode([ref_document])
    abstract_embeddings = model.encode(abstracts)
    similarities = cosine_similarity(ref_embedding, abstract_embeddings)
    return similarities.flatten()


st.set_page_config(layout="wide")

col1, col2 = st.beta_columns([1, 2])

with col1:
    st.markdown("### Your Curiosity")
    user_input = st.text_area('Enter your curiosity here',
                              value='''optimal hospital discharges to skilled nursing facilities''',
                              height=400)

with col2:
    st.markdown("### Articles")
    ref_document = user_input.strip()

    # Use the function to get articles
    xml_response = get_arxiv_articles(ref_document)

    # Parse XML response and convert to DataFrame
    if xml_response is not None:
        articles_df = parse_arxiv_xml(xml_response)
        articles_df['similarity'] = rank_abstracts_by_similarity(articles_df['summary'].tolist(), ref_document)

        # Display the number of articles pulled
        st.markdown(f"**Articles Pulled:** {len(articles_df)}")

        # Adjust dataframe row index and display the dataframe with custom styling
        articles_df.index = range(1, len(articles_df) + 1)
        st.dataframe(articles_df[['title', 'similarity', 'summary']].sort_values(by='similarity', ascending=False),
                     height=400)
    else:
        st.write("No articles found.")
