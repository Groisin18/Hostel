import os
import json
import config

database_name = config.USER_DATA_FILE

if not os.path.exists(database_name):
    with open(database_name, "w", encoding='UTF-8') as f:
        json.dump({}, f)

def load_user_data():
    with open(database_name, "r", encoding='UTF-8') as f:
        return json.load(f)

def save_user_data(data):
    with open(database_name, "w", encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)