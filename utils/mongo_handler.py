import urllib.parse
import re
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, OperationFailure, ServerSelectionTimeoutError

def sanitize_uri(raw_uri):
    try:
        pattern = r"^(mongodb(?:\+srv)?://)(.+):(.+)@(.+)$"
        match = re.match(pattern, raw_uri)
        if match:
            protocol, user, password, rest = match.groups()
            safe_user = urllib.parse.quote_plus(user)
            safe_pass = urllib.parse.quote_plus(password)
            return f"{protocol}{safe_user}:{safe_pass}@{rest}"
        return raw_uri
    except Exception:
        return raw_uri

def get_mongo_data(uri, db_name=None, coll_name=None, action="list_dbs"):
    clean_uri = sanitize_uri(uri)
    client = MongoClient(clean_uri, serverSelectionTimeoutMS=5000)
    try:
        if action == "list_dbs":
            return client.list_database_names()
        
        db = client[db_name]
        if action == "list_colls":
            return db.list_collection_names()
        
        coll = db[coll_name]
        if action == "fetch":
            return list(coll.find().limit(100))
    except ServerSelectionTimeoutError:
        raise Exception("Timeout: Is your IP whitelisted in MongoDB Atlas (0.0.0.0/0)?")
    except (ConfigurationError, OperationFailure) as e:
        raise Exception(f"Connection Error: {e}")
    finally:
        client.close()

def test_connection(uri):
    clean_uri = sanitize_uri(uri)
    client = MongoClient(clean_uri, serverSelectionTimeoutMS=3000)
    try:
        client.admin.command('ping')
        return True, "Connection Successful!"
    except Exception as e:
        return False, str(e)
    finally:
        client.close()
        