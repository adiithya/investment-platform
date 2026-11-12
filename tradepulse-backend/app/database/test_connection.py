from sqlalchemy import text

from app.database.session import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database()"))
        print("Connected to database:", result.scalar())

except Exception as error:
    print("Database connection failed:", error)