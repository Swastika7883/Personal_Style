import psycopg2
import os
from dotenv import load_dotenv  # pip install python-dotenv

def import_sql_secure():
    # Load environment variables
    load_dotenv()
    
    try:
        # Get credentials from environment variables (more secure)
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "dpg-d4hljlbuibrs73dmvvug-a.render.com"),
            dbname=os.getenv("DB_NAME", "postgres_db_yz4z"),
            user=os.getenv("DB_USER", "postgres_db_yz4z_user"),
            password=os.getenv("DB_PASSWORD"),  # This should be in your .env file
            port=os.getenv("DB_PORT", 5432)
        )
        
        # Test connection
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Connected to: {db_version[0]}")
        
        # Read and execute SQL file
        with open("outfits_postgres.sql", "r") as f:
            sql_script = f.read()
            
        # Execute the entire script
        cur.execute(sql_script)
        conn.commit()
        
        # Verify the import
        cur.execute("SELECT COUNT(*) FROM outfits;")
        count = cur.fetchone()[0]
        print(f"Successfully imported {count} records into outfits table!")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import_sql_secure()