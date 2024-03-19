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
    return df


job_data = getdata()
job_data['info'] = job_data.apply(lambda row: 'Company: ' + row['company'] + '\nJob Title: ' + row['jobtitle'] + '\nJob Description: ' + row['jobdetails'] + '\nLink to the Job: ' + row['link'], axis=1)
query = "give me a job that has python and scala"
relevant_doc = retrieve_documents(query, job_data['info'])
relevant_doc = '\n'.join(relevant_doc)
prompt = """
JOBS: {} 
QUESTION: {} 
INSTRUCTIONS: Answer the user's QUESTION using the list of jobs mentioned in the JOBS text above. 
Keep your answer grounded in the facts of the JOBS. 
If the none of the JOBS answer the QUESTION, 
return that you do not know and provide suggestions of JOBS that are close to the QUESTION.
Always add corresponding links to the suggested jobs.
""".format(relevant_doc, query)
print("Prompt:", prompt)


# Your OpenAI API key
api_key = ''

# Endpoint for ChatGPT v1 API
endpoint = 'https://api.openai.com/v1/chat/completions'

# Generate text
generated_text = generate_text(prompt, api_key, endpoint)
print("Generated Text:")
print(generated_text)
