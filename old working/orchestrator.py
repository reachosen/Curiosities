from database_utils import (
    connect_database,
    check_create_table,
    insert_articles_into_db,
    save_curiosity,
    get_curiosity_list,
)
from api_utils import get_arxiv_articles, parse_arxiv_xml
from similarity_utils import rank_abstracts_by_similarity
import pandas as pd
import streamlit as st
import datetime

if "page_number" not in st.session_state:
    st.session_state.page_number = 1

def fetch_display_articles(conn, c, articles_df, ref_document, max_results, results_per_page):
    if len(articles_df) > 0:
        articles_df['similarity'] = rank_abstracts_by_similarity(articles_df['summary'].tolist(), ref_document)
        articles_df = articles_df.sort_values(by='similarity', ascending=False)
        fetch_count = max_results - len(articles_df)
    else:
        fetch_count = max_results

    if fetch_count > 0:
        xml_response = get_arxiv_articles(ref_document, fetch_count)
        if xml_response is not None:
            new_articles_df = parse_arxiv_xml(xml_response)
            new_articles_df['similarity'] = rank_abstracts_by_similarity(new_articles_df['summary'].tolist(), ref_document)
            new_articles_df = new_articles_df.sort_values(by='similarity', ascending=False)
            insert_articles_into_db(c, conn, 'articles', new_articles_df)
            articles_df = pd.concat([articles_df, new_articles_df]).head(max_results)

    total_pages = (len(articles_df) + results_per_page - 1) // results_per_page
    page_number = st.session_state.page_number

    start = (page_number - 1) * results_per_page
    end = start + results_per_page
    page_articles_df = articles_df.iloc[start:end]

    st.markdown(f"### Displaying Results")
    st.markdown(f"**Articles Displayed:** {len(page_articles_df)} of {len(articles_df)}")

    displayed_articles_df = page_articles_df
    displayed_articles_df.index = range(start + 1, start + len(displayed_articles_df) + 1)
    st.dataframe(displayed_articles_df[['title', 'similarity', 'summary']], height=400)


# Set page title and remove margin
st.set_page_config(page_title="Arxiv Article Puller", layout="wide", initial_sidebar_state="collapsed", page_icon="📚")

# Connect to SQLite database
conn = connect_database('arxiv_articles.db')
c = conn.cursor()

# Load or create articles and curiosities tables
articles_df = check_create_table(c, "articles")
check_create_table(c, "curiosities")

# Sidebar - Curiosity Text Area
st.sidebar.markdown("### Your Curiosity")
if 'curiosity' not in st.session_state:
    st.session_state.curiosity = 'optimal hospital discharges to skilled nursing facilities'

curiosity_input = st.sidebar.text_area('Enter your curiosity here', value=st.session_state.curiosity, height=200)

# Button to save curiosity
if st.sidebar.button('Save Curiosity'):
    save_curiosity(c, conn, curiosity_input, 'arxiv', datetime.datetime.now())
    st.session_state.curiosity = curiosity_input

# Select from existing curiosities
curiosity_list = get_curiosity_list(c)
if len(curiosity_list) > 0:
    selected_curiosity = st.sidebar.selectbox('Or select a previous curiosity', curiosity_list)
    if selected_curiosity != st.session_state.curiosity:
        st.session_state.curiosity = selected_curiosity

ref_document = st.session_state.curiosity.strip()

# Sidebar - Search Configuration
st.sidebar.markdown("### Search Configuration")
max_results = st.sidebar.number_input('Max Results', min_value=1, max_value=100, value=10, step=1)
results_per_page = st.sidebar.slider('Results per page', min_value=1, max_value=100, value=10, step=1)

# Sidebar - Fetch Button
if st.sidebar.button('Fetch'):
    fetch_display_articles(conn, c, articles_df, ref_document, max_results, results_per_page)

# Display Results
st.markdown(f"### Displaying Results for: {ref_document}")

if 'similarity' in articles_df.columns:
    st.dataframe(articles_df[['title', 'similarity', 'summary']], height=400)
else:
    st.write("No articles found.")

# Close the SQLite connection
conn.close()

