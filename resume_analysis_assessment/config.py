from pymongo import MongoClient

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "resume_analysis"

def get_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        print("Database connected successfully!")
        return db
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
