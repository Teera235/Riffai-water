"""
Setup PostGIS extension on Cloud SQL instance
Run: python setup_postgis.py
"""
import psycopg2
import sys

# Cloud SQL connection details
DB_HOST = "34.21.160.173"  # Public IP of riffai-db
DB_PORT = "5432"
DB_NAME = "riffai"
DB_USER = "postgres"
DB_PASSWORD = "riffai123"  # Change this if different

def setup_postgis():
    try:
        print("Connecting to Cloud SQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=10
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Installing PostGIS extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        print("✅ PostGIS installed")
        
        cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology;")
        print("✅ PostGIS Topology installed")
        
        print("\nGranting permissions to 'riffai' user...")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE riffai TO riffai;")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO riffai;")
        cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO riffai;")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO riffai;")
        cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO riffai;")
        print("✅ Permissions granted")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 PostGIS setup completed successfully!")
        return 0
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your IP is whitelisted in Cloud SQL")
        print("2. Check if the instance is running")
        print("3. Verify the connection details")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(setup_postgis())
