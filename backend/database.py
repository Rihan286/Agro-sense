from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from .env or use local default
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

try:
    # Initialize MongoDB Client
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    
    # Check connection
    client.server_info()
    print("Successfully connected to MongoDB")
    
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Falling back to mongomock...")
    try:
        import mongomock
        client = mongomock.MongoClient()
        print("Successfully initialized mongomock")
    except ImportError:
        print("mongomock not installed, database will be unusable")
        client = None

if client:
    # Initialize the database
    db = client.agrosense
    
    # Collections
    farmers_collection = db["farmers"]
    detection_history_collection = db["detection_history"]
    advisory_history_collection = db["advisory_history"]
    market_search_history_collection = db["market_search_history"]
    
    # Ensure unique email index for farmers
    farmers_collection.create_index("email", unique=True)
else:
    db = None
    farmers_collection = None
    detection_history_collection = None
    advisory_history_collection = None
    market_search_history_collection = None
