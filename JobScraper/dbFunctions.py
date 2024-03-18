import psycopg2
from configparser import ConfigParser


def config(filename='dbConfig.config', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {param[0]: param[1] for param in parser.items(section)}


def create_connection():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    return [cur, conn]


def close_connection(cur, conn):
    cur.close()
    conn.close()


def display_table_structure(table_name):
    [cur, conn] = create_connection()
    query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
    cur.execute(query)
    rows = cur.fetchall()
    print(f"Table structure for {table_name}:")
    for row in rows:
        print(f"Column: {row[0]}, Data Type: {row[1]}")
    close_connection(cur, conn)


def create_table():
    [cur, conn] = create_connection()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            jobTitle VARCHAR(200),
            company VARCHAR(200),
            location VARCHAR(200),
            jobDetails TEXT,
            link VARCHAR(200),
            jobPlatform VARCHAR(200),
            jobType VARCHAR(200),
            datePosted TIMESTAMP
        )
    '''
    try:
        cur.execute(create_table_query)
        print("Table created successfully.")
    except psycopg2.Error as e:
        print("Error creating table:", e)
    conn.commit()
    close_connection(cur, conn)


def delete_table():
    [cur, conn] = create_connection()
    delete_table_query = '''
        DROP TABLE IF EXISTS jobs 
    '''
    try:
        cur.execute(delete_table_query)
        print("Table deleted successfully.")
    except psycopg2.Error as e:
        print("Error creating table:", e)
    conn.commit()
    close_connection(cur, conn)


def load_table(job):
    [cur, conn] = create_connection()
    query = '''
            INSERT INTO jobs (jobTitle, company, location, jobDetails, link, jobPlatform, jobType, datePosted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
    try:
        cur.execute(query, (
        job.title, job.company, job.location, job.content, job.link, job.platform, job.type, job.date_object))
    except psycopg2.Error as e:
        print("Error loading job:", e)
    conn.commit()
    close_connection(cur, conn)


def display_table_rows():
    [cur, conn] = create_connection()
    query = "SELECT * FROM jobs"
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print("Error loading job:", e)
    conn.commit()
    close_connection(cur, conn)
