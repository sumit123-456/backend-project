#!/usr/bin/env python
"""
Create MySQL database for HRMS project
"""
import pymysql
from django.conf import settings

def create_database():
    # Connect to MySQL server (without specifying database)
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',  # XAMPP default
        port=3306
    )
    
    try:
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            db_name = 'hrms_database'
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{db_name}' created successfully!")
            
            # Show all databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print("Available databases:")
            for db in databases:
                print(f"  - {db[0]}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    create_database()