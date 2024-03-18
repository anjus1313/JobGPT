import pandas as pd
import psycopg2
from RAG import retrieve_documents, generate_text
from JobScraper import dbFunctions as db
import numpy as np

def getdata():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="rigved",
        host="localhost",
        port="5432"
    )
    sql_query = "SELECT * FROM jobs;"
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    print(df)
    return df


job_data = getdata()
job_data['info'] = job_data.apply(lambda row: 'Company: ' + row['company'] + '\nJob Title: ' + row['jobtitle'] + '\nJob Description: ' + row['jobdetails'] + '\nLink to the Job: ' + row['link'], axis=1)
query = "give me a summary of the top 5 data engineer jobs that uses python along with the url"
relevant_doc = retrieve_documents(query, job_data['info'])
print("Query:", query)
print("Most Relevant Document:", relevant_doc)
relevant_doc = '\n'.join(relevant_doc)
prompt = """
DOCUMENT: {}
QUESTION: {}
INSTRUCTIONS:
Answer the user's QUESTION using the DOCUMENT text above.
Keep your answer grounded in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION, return {{NONE}}
""".format(relevant_doc, query)
# If the DOCUMENT doesn’t contain the facts to answer the QUESTION, return {{NONE}}
# Your OpenAI API key
api_key = ''
# Endpoint for ChatGPT v1 API
endpoint = 'https://api.openai.com/v1/chat/completions'
# Generate text
generated_text = generate_text(prompt, api_key, endpoint)
print("Generated Text:")
print(generated_text)
