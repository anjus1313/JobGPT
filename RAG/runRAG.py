import pandas as pd
import psycopg2
from RAG import retrieve_documents, generate_text
from configparser import ConfigParser


def config(filename='dbConfig.config', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {param[0]: param[1] for param in parser.items(section)}


def getdata():
    params = config()
    conn = psycopg2.connect(**params)
    sql_query = "SELECT * FROM jobs;"
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    print(df)
    return df


job_data = getdata()
job_data['info'] = job_data.apply(
    lambda row: 'Company: ' + row['company'] + '\nJob Title: ' + row['jobtitle'] + '\nJob Description: ' + row[
        'jobdetails'] + '\nLink to the Job: ' + row['link'], axis=1)
query = "give me a job that has data pipelines, scala and python. All 3 must be there"
relevant_doc = retrieve_documents(query, job_data['info'])
print("Query:", query)
#print("Most Relevant Document:", relevant_doc)
relevant_doc = '\n'.join(relevant_doc)
prompt = """
DOCUMENT: {}
QUESTION: {}
INSTRUCTIONS:
Answer the user's QUESTION using the DOCUMENT text above.
Keep your answer grounded in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION, return {{NONE}}
""".format(relevant_doc, query)


# Your OpenAI API key
api_key = ''

# Endpoint for ChatGPT v1 API
endpoint = 'https://api.openai.com/v1/chat/completions'

# Generate text
generated_text = generate_text(prompt, api_key, endpoint)
print("Generated Text:")
print(generated_text)
