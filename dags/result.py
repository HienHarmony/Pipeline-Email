import requests
import pandas as pd
import logging
import os
from pymongo import MongoClient
client = MongoClient("mongodb://mongo:27017/")
db = client['email_database']  
collection = db['emails']      

def init_log(logger_name, log_dir, log_file):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    log_path = os.path.join(log_dir, log_file)
    file_handler = logging.FileHandler(log_path, encoding='utf-8', mode='a')
    file_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    if logger.hasHandlers():
        logger.handlers.clear()
    
    logger.addHandler(file_handler)
    return logger

logger = init_log('emails', './log', 'emails.log')
url = "https://raw.githubusercontent.com/tnhanh/data-midterm-17A/refs/heads/main/email.csv"

response = requests.get(url)
if response.status_code == 200:
    data = pd.read_csv(url)
    
    sample_data = data.sample(n=200)
    
    new_records = []
    for _, row in sample_data.iterrows():
        if not collection.find_one({"message": row['message']}):
            new_records.append({"file": row['file'], "message": row['message']})
    
    if new_records:
        collection.insert_many(new_records)
        logger.info(f"Added {len(new_records)} new records to MongoDB.")
    else:
        logger.info("No new records to add.")
else:
    logger.error(f"Failed to download the file: {response.status_code}")
