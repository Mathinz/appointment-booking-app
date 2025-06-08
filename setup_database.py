#!/usr/bin/env python3
"""
Simple database setup script for Law Firm Booking System
Run this script to initialize the database with required tables and sample data.

Usage:
    python setup_database.py
"""

import sqlite3
import os
from datetime import datetime

def init_database(db_path="law_firm_bookings.db"):
    """Initialize the database with required tables and sample data"""
    
    print(f"🔧 Initializing database at: {db_path}")
    
    # Check if database already exists
    db_exists = os.path.exists(db_path)
    if db_exists:
        print(f"⚠️  Database already exists at {db_path}")
        response = input("Do you want to continue? This will add missing tables/data but won't overwrite existing data (y/n): ")
        if response.lower() != 'y':
            print("❌ Database initialization cancelled")
            return
    
    try:
        with sqlite3.connect(db_path) as conn:
            print("📊 Creating tables...")
            
            # Create lawyers table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lawyers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    practice_areas TEXT NOT NULL,
                    hourly_rate REAL NOT NULL,
                    email TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create appointments table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id TEXT PRIMARY KEY,
                    client_name TEXT NOT NULL,
                    client_email TEXT NOT NULL,
                    client_phone TEXT NOT NULL,
                    client_company TEXT,
                    lawyer_id TEXT NOT NULL,
                    appointment_datetime TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    practice_area TEXT NOT NULL,
                    appointment_type TEXT NOT NULL,
                    urgency_level TEXT NOT NULL,
                    case_description TEXT,
                    status TEXT DEFAULT 'confirmed',
                    meeting_link TEXT,
                    office_location TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)
            
            # Create clients table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT NOT NULL,
                    company TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("👥 Adding sample lawyers...")
            
            # Insert sample lawyers
            sample_lawyers = [
                ('lawyer_1', 'Sarah Johnson', 'corporate,contract_review', 450.0, 'sarah@leaptra.com'),
                ('lawyer_2', 'Michael Chen', 'litigation,criminal', 400.0, 'michael@leaptra.com'),
                ('lawyer_3', 'Emily Rodriguez', 'family,immigration', 350.0, 'emily@leaptra.com'),
                ('lawyer_4', 'David Kim', 'real_estate,intellectual_property', 425.0, 'david@leaptra.com'),
                ('lawyer_5', 'Jennifer Wu', 'employment,intellectual_property', 375.0, 'jennifer@leaptra.com'),
            ]
            
            cursor = conn.cursor()
            lawyers_added = 0
            for lawyer in sample_lawyers:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO lawyers (id, name, practice_areas, hourly_rate, email)
                        VALUES (?, ?, ?, ?, ?)
                    """, lawyer)
                    if cursor.rowcount > 0:
                        lawyers_added += 1
                        print(f"  ✅ Added lawyer: {lawyer[1]} ({lawyer[2]})")
                except sqlite3.Error as e:
                    print(f"  ❌ Error adding lawyer {lawyer[1]}: {e}")
            
            print("🚀 Creating performance indexes...")
            
            # Create indexes for better performance
            indexes = [
                ("idx_appointments_datetime", "appointments", "appointment_datetime"),
                ("idx_appointments_lawyer_id", "appointments", "lawyer_id"),
                ("idx_lawyers_practice_areas", "lawyers", "practice_areas"),
                ("idx_clients_email", "clients", "email"),
            ]
            
            for index_name, table, column in indexes:
                conn.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column})")
            
            conn.commit()
            
            # Get final counts
            lawyer_count = conn.execute("SELECT COUNT(*) FROM lawyers").fetchone()[0]
            appointment_count = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
            
            print("\n✅ Database initialization complete!")
            print(f"📈 Database Statistics:")
            print(f"   • Database file: {db_path}")
            print(f"   • Total lawyers: {lawyer_count}")
            print(f"   • Total appointments: {appointment_count}")
            print(f"   • New lawyers added: {lawyers_added}")
            print(f"   • Tables created: lawyers, appointments, clients")
            print(f"   • Indexes created: {len(indexes)}")
            
            return True
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_database_status(db_path="law_firm_bookings.db"):
    """Check and display database status"""
    
    if not os.path.exists(db_path):
        print(f"❌ Database does not exist at {db_path}")
        return False
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            print(f"\n📊 Database Status Report for {db_path}")
            print("=" * 50)
            
            # Check tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Tables: {', '.join(tables)}")
            
            # Count records
            if 'lawyers' in tables:
                lawyer_count = cursor.execute("SELECT COUNT(*) FROM lawyers").fetchone()[0]
                print(f"👥 Lawyers: {lawyer_count}")
                
                # Show lawyer details
                cursor.execute("SELECT name, practice_areas, hourly_rate FROM lawyers")
                for name, areas, rate in cursor.fetchall():
                    print(f"   • {name} - {areas} (${rate}/hour)")
            
            if 'appointments' in tables:
                appointment_count = cursor.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
                print(f"📅 Appointments: {appointment_count}")
            
            if 'clients' in tables:
                client_count = cursor.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
                print(f"🤝 Clients: {client_count}")
            
            print("✅ Database is healthy and ready to use!")
            return True
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("🏛️  Law Firm Booking System - Database Setup")
    print("=" * 50)
    
    # Initialize database
    success = init_database()
    
    if success:
        # Show status
        check_database_status()
        
        print("\n🎉 You can now run the booking system!")
        print("💡 Next steps:")
        print("   1. Install required packages: pip install openai pydantic")
        print("   2. Set your OpenAI API key in .env file")
        print("   3. Run the main booking system")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")
