#!/usr/bin/env python

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    db_name = os.environ.get('DB_NAME', 'tripbudget_db')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'postgres')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
            print(f"{db_name} utworzone")
        else:
            print(f"{db_name} już istnieje")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Błąd połączenia z PostgreSQL: {e}")
        return False

def run_migrations():
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Błąd migracji: {e}")
        return False

if __name__ == "__main__":
    if not create_database():
        print("Problem z bazą danych")
        sys.exit(1)
    
    if not run_migrations():
        print("Problem z migracjami")
        sys.exit(1)