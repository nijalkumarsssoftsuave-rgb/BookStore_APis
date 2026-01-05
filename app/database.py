from motor.motor_asyncio import  AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get('DB_URL')

def get_db():
    try:
        client = AsyncIOMotorClient(DB_URL)
        yield client['refernce_db']
    except Exception as e:
        raise  e
    # finally:
    #     client.close()