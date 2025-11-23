from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ⚠️ Use your XAMPP defaults: 'root' user, no password, 'localhost'
# The connection string format is: "mysql+pymysql://USER:PASSWORD@HOST/DB_NAME"


# Example for port 3307
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3307/fashion_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get a DB session for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()