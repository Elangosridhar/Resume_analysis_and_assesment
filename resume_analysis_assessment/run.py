from app import app  # Import the Flask app instance
from config import get_database

# Test database connection
def test_database_connection():
    db = get_database()  # Test database connection
    if db is not None:
        print(f"Connected to database: {db.name}")
    else:
        print("Failed to connect to database.")

# Run the app
if __name__ == "__main__":
    test_database_connection()  # Test the database connection before running the app
    app.run(debug=True)
