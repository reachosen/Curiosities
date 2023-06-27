import sqlite3
import pandas as pd

def connect_database(db_name):
    return sqlite3.connect(db_name)

def close_database(conn):
    conn.close()

def check_create_table(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
    table_exists = c.fetchone()

    if table_exists:
        c.execute("SELECT * FROM articles")
        rows = c.fetchall()
        if len(rows) > 0:
            return pd.DataFrame(rows, columns=['id', 'title', 'summary'])
        else:
            return pd.DataFrame(columns=['id', 'title', 'summary'])
    else:
        c.execute('''CREATE TABLE IF NOT EXISTS articles (id TEXT PRIMARY KEY, title TEXT, summary TEXT)''')
        return pd.DataFrame(columns=['id', 'title', 'summary'])

def insert_articles_into_db(c, conn, articles_df):
    for _, article in articles_df.iterrows():
        c.execute("INSERT OR IGNORE INTO articles (id, title, summary) VALUES (?, ?, ?)",
                  (article['id'], article['title'], article['summary']))
    conn.commit()

def check_create_curiosity_table(c):
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='curiosities'")
    table_exists = c.fetchone()
    if table_exists:
        c.execute("SELECT curiosity, time_period, source, date_created FROM curiosities")
        curiosities = c.fetchall()
    else:
        c.execute('''CREATE TABLE IF NOT EXISTS curiosities
                    (curiosity TEXT PRIMARY KEY, time_period TEXT, source TEXT, date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        curiosities = []
    return curiosities

def save_curiosity(c, conn, curiosity, time_period, source):
    c.execute("INSERT OR IGNORE INTO curiosities (curiosity, time_period, source) VALUES (?, ?, ?)",
              (curiosity, time_period, source))
    conn.commit()

def get_curiosity_list(c):
    c.execute("SELECT curiosity FROM curiosities ORDER BY date_created DESC")
    curiosities = c.fetchall()
    return [curiosity[0] for curiosity in curiosities]

def check_create_table(c, table_name):
    # Check if table exists
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = c.fetchone()

    if table_exists:
        # Load data from database
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        if len(rows) > 0:
            if table_name == 'articles':
                df = pd.DataFrame(rows, columns=['id', 'title', 'summary'])
            elif table_name == 'curiosities':
                df = pd.DataFrame(rows, columns=['curiosity', 'time_period', 'source', 'date_created'])
        else:
            if table_name == 'articles':
                df = pd.DataFrame(columns=['id', 'title', 'summary'])
            elif table_name == 'curiosities':
                df = pd.DataFrame(columns=['curiosity', 'time_period', 'source', 'date_created'])
    else:
        # Create table if it doesn't exist
        if table_name == 'articles':
            c.execute('''CREATE TABLE IF NOT EXISTS articles
                         (id TEXT PRIMARY KEY, title TEXT, summary TEXT)''')
            df = pd.DataFrame(columns=['id', 'title', 'summary'])
        elif table_name == 'curiosities':
            c.execute('''CREATE TABLE IF NOT EXISTS curiosities
                         (curiosity TEXT, time_period TEXT, source TEXT, date_created TEXT)''')
            df = pd.DataFrame(columns=['curiosity', 'time_period', 'source', 'date_created'])

    return df


