import boto3
import fitz  # PyMuPDF
import psycopg2
import os

def download_file(bucket_name, s3_key, local_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, local_path)

def extract_text(file_path):
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

def chunk_text(text, max_chars=2000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def store_chunks(chunks, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    for chunk in chunks:
        cursor.execute(
            "INSERT INTO documents (content, tsv) VALUES (%s, to_tsvector('english', %s))",
            (chunk, chunk)
        )
    conn.commit()
    cursor.close()
    conn.close()

def lambda_handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    db_config = {
        'host': os.environ['DB_HOST'],
        'dbname': os.environ['DB_NAME'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD']
    }
    s3_key = event['s3_key']
    local_path = '/tmp/document.pdf'

    download_file(bucket_name, s3_key, local_path)
    text = extract_text(local_path)
    chunks = chunk_text(text)
    store_chunks(chunks, db_config)