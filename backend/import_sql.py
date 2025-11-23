import psycopg2
import os
from dotenv import load_dotenv
import sys

def import_sql_secure():
    # Load environment variables
    load_dotenv()
    
    conn = None
    cur = None
    
    try:
        # Get credentials from environment variables
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        
        # Test connection
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"✅ Connected to: {db_version[0]}")
        
        # Check if SQL file exists
        sql_file_path = "outfits_postgres.sql"
        if not os.path.exists(sql_file_path):
            print(f"❌ SQL file not found: {sql_file_path}")
            return False
        
        # Read and execute SQL file
        with open(sql_file_path, "r") as f:
            sql_script = f.read()
        
        print("📦 Executing SQL script...")
        cur.execute(sql_script)
        conn.commit()
        
        # Verify the import
        cur.execute("SELECT COUNT(*) FROM outfits;")
        count = cur.fetchone()[0]
        print(f"✅ Successfully imported {count} records into outfits table!")
        
        # Show table structure
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'outfits';
        """)
        columns = cur.fetchall()
        print("\n📊 Table structure:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection error: {e}")
        return False
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        # Ensure resources are closed properly
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
    success = import_sql_secure()
    sys.exit(0 if success else 1)