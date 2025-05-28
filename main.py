"""
Law Firm AI Appointment Booking System
Multi-Agent AI System for Leaptra.com

This system uses multiple specialized AI agents to handle different aspects
of appointment booking for a law firm.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
import openai
from pydantic import BaseModel, Field, validator
import sqlite3
from contextlib import asynccontextmanager

# Configure OpenAI
openai.api_key = "your-openai-api-key"  # Replace with your actual API key

class LegalPracticeArea(str, Enum):
    CORPORATE = "corporate"
    LITIGATION = "litigation"
    FAMILY = "family"
    REAL_ESTATE = "real_estate"
    CRIMINAL = "criminal"
    IMMIGRATION = "immigration"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    EMPLOYMENT = "employment"

class AppointmentType(str, Enum):
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    DOCUMENT_REVIEW = "document_review"
    COURT_PREP = "court_preparation"
    CONTRACT_REVIEW = "contract_review"

class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Pydantic Models for Data Validation
class ClientInfo(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    phone: str = Field(..., min_length=10, max_length=15)
    company: Optional[str] = None
    
    @validator('phone')
    def validate_phone(cls, v):
        # Remove non-digit characters
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return digits

class AppointmentRequest(BaseModel):
    client_info: ClientInfo
    practice_area: LegalPracticeArea
    appointment_type: AppointmentType
    urgency: UrgencyLevel
    preferred_dates: List[str] = Field(..., min_items=1, max_items=5)
    description: str = Field(..., min_length=10, max_length=1000)
    duration_minutes: int = Field(default=60, ge=30, le=240)
    
    @validator('preferred_dates')
    def validate_dates(cls, v):
        parsed_dates = []
        for date_str in v:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                if date < datetime.now():
                    raise ValueError(f'Date {date_str} is in the past')
                parsed_dates.append(date)
            except ValueError as e:
                raise ValueError(f'Invalid date format {date_str}. Use YYYY-MM-DD')
        return v

class LawyerAvailability(BaseModel):
    lawyer_id: str
    name: str
    practice_areas: List[LegalPracticeArea]
    available_slots: List[Dict[str, Any]]
    hourly_rate: float

class BookingConfirmation(BaseModel):
    booking_id: str
    client_info: ClientInfo
    lawyer_name: str
    appointment_datetime: datetime
    duration_minutes: int
    practice_area: LegalPracticeArea
    appointment_type: AppointmentType
    meeting_link: Optional[str] = None
    office_location: Optional[str] = None
    preparation_notes: Optional[str] = None

# Database Setup
class DatabaseManager:
    def __init__(self, db_path: str = "law_firm_bookings.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lawyers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    practice_areas TEXT NOT NULL,
                    hourly_rate REAL NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id TEXT PRIMARY KEY,
                    client_name TEXT NOT NULL,
                    client_email TEXT NOT NULL,
                    client_phone TEXT NOT NULL,
                    lawyer_id TEXT NOT NULL,
                    appointment_datetime TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    practice_area TEXT NOT NULL,
                    appointment_type TEXT NOT NULL,
                    status TEXT DEFAULT 'confirmed',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (lawyer_id) REFERENCES lawyers (id)
                )
            """)
            
            # Insert sample lawyers
            sample_lawyers = [
                ('lawyer_1', 'Sarah Johnson', 'corporate,contract_review', 450.0, 'sarah@leaptra.com'),
                ('lawyer_2', 'Michael Chen', 'litigation,criminal', 400.0, 'michael@leaptra.com'),
                ('lawyer_3', 'Emily Rodriguez', 'family,immigration', 350.0, 'emily@leaptra.com'),
                ('lawyer_4', 'David Kim', 'real_estate,intellectual_property', 425.0, 'david@leaptra.com'),
            ]
            
            conn.executemany("""
                INSERT OR IGNORE INTO lawyers (id, name, practice_areas, hourly_rate, email)
                VALUES (?, ?, ?, ?, ?)
            """, sample_lawyers)

# AI Agent Classes
class IntakeAgent:
    """Agent responsible for understanding client needs and extracting information"""
    
    def __init__(self, openai_client):
        self.client = openai_client
        self.system_prompt = """
        You are an intake specialist for a prestigious law firm. Your role is to:
        1. Understand the client's legal needs
        2. Determine the appropriate practice area
        3. Assess urgency level
        4. Extract all necessary information for booking
        
        Be professional, empathetic, and thorough. Ask clarifying questions if needed.
        Always prioritize client confidentiality and comfort.
        """
    
    async def process_initial_inquiry(self, user_message: str) -> Dict[str, Any]:
        """Process the initial client message and extract structured information"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Client inquiry: {user_message}"}
            ],
            functions=[
                {
                    "name": "extract_client_needs",
                    "description": "Extract structured information from client inquiry",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "practice_area": {
                                "type": "string",
                                "enum": [area.value for area in LegalPracticeArea]
                            },
                            "urgency": {
                                "type": "string",
                                "enum": [level.value for level in UrgencyLevel]
                            },
                            "appointment_type": {
                                "type": "string",
                                "enum": [type.value for type in AppointmentType]
                            },
                            "case_summary": {"type": "string"},
                            "questions_to_ask": {"type": "array", "items": {"type": "string"}},
                            "estimated_duration": {"type": "integer", "minimum": 30, "maximum": 240}
                        },
                        "required": ["practice_area", "urgency", "case_summary"]
                    }
                }
            ],
            function_call={"name": "extract_client_needs"}
        )
        
        function_call = response.choices[0].message.function_call
        return json.loads(function_call.arguments)

class SchedulingAgent:
    """Agent responsible for finding available appointments and scheduling"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.client = openai.OpenAI()
        
    async def find_available_lawyers(self, practice_area: LegalPracticeArea, 
                                   preferred_dates: List[str]) -> List[LawyerAvailability]:
        """Find lawyers available in the specified practice area and dates"""
        
        with sqlite3.connect(self.db.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM lawyers 
                WHERE practice_areas LIKE ?
            """, (f'%{practice_area.value}%',))
            
            lawyers = cursor.fetchall()
            
        available_lawyers = []
        for lawyer in lawyers:
            # Simulate availability check (in real implementation, integrate with calendar API)
            available_slots = self._generate_mock_availability(preferred_dates)
            
            available_lawyers.append(LawyerAvailability(
                lawyer_id=lawyer['id'],
                name=lawyer['name'],
                practice_areas=[LegalPracticeArea(area.strip()) 
                              for area in lawyer['practice_areas'].split(',')],
                available_slots=available_slots,
                hourly_rate=lawyer['hourly_rate']
            ))
        
        return available_lawyers
    
    def _generate_mock_availability(self, preferred_dates: List[str]) -> List[Dict[str, Any]]:
        """Generate mock availability slots (replace with real calendar integration)"""
        slots = []
        for date_str in preferred_dates:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            # Generate morning and afternoon slots
            for hour in [9, 10, 11, 14, 15, 16]:
                slot_time = date.replace(hour=hour, minute=0)
                if slot_time > datetime.now():
                    slots.append({
                        "datetime": slot_time.isoformat(),
                        "duration_available": 120,  # 2 hours max
                        "slot_type": "office" if hour < 12 else "virtual"
                    })
        return slots[:6]  # Return max 6 slots

class CommunicationAgent:
    """Agent responsible for client communication and confirmations"""
    
    def __init__(self):
        self.client = openai.OpenAI()
        
    async def generate_confirmation_email(self, booking: BookingConfirmation) -> str:
        """Generate a professional confirmation email"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a professional legal assistant. Generate a confirmation email 
                    that is warm, professional, and includes all necessary details. Include preparation 
                    instructions and what to bring to the appointment."""
                },
                {
                    "role": "user",
                    "content": f"""Generate a confirmation email for:
                    Client: {booking.client_info.name}
                    Lawyer: {booking.lawyer_name}
                    Date/Time: {booking.appointment_datetime}
                    Practice Area: {booking.practice_area}
                    Type: {booking.appointment_type}
                    Duration: {booking.duration_minutes} minutes
                    """
                }
            ]
        )
        
        return response.choices[0].message.content
    
    async def generate_preparation_notes(self, practice_area: LegalPracticeArea, 
                                       appointment_type: AppointmentType, 
                                       case_description: str) -> str:
        """Generate preparation notes for the client"""
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Generate helpful preparation notes for a legal consultation. 
                    Include what documents to bring, questions to prepare, and what to expect."""
                },
                {
                    "role": "user",
                    "content": f"""Practice area: {practice_area}
                    Appointment type: {appointment_type}
                    Case description: {case_description}
                    """
                }
            ]
        )
        
        return response.choices[0].message.content

# Main Booking System Orchestrator
class LawFirmBookingSystem:
    """Main system that orchestrates all agents"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.openai_client = openai.OpenAI()
        self.intake_agent = IntakeAgent(self.openai_client)
        self.scheduling_agent = SchedulingAgent(self.db)
        self.communication_agent = CommunicationAgent()
    
    async def process_booking_request(self, user_message: str, 
                                    client_info: Optional[ClientInfo] = None) -> Dict[str, Any]:
        """Main method to process a complete booking request"""
        
        try:
            # Step 1: Process initial inquiry
            intake_result = await self.intake_agent.process_initial_inquiry(user_message)
            
            if not client_info:
                return {
                    "status": "needs_client_info",
                    "message": "Please provide your contact information to proceed with booking.",
                    "intake_analysis": intake_result,
                    "questions": intake_result.get("questions_to_ask", [])
                }
            
            # Step 2: Find available lawyers
            practice_area = LegalPracticeArea(intake_result["practice_area"])
            # For demo, use next 7 days as preferred dates
            preferred_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') 
                             for i in range(1, 8)]
            
            available_lawyers = await self.scheduling_agent.find_available_lawyers(
                practice_area, preferred_dates
            )
            
            if not available_lawyers:
                return {
                    "status": "no_availability",
                    "message": "No lawyers available in the requested practice area and timeframe.",
                    "alternative_dates": True
                }
            
            # Step 3: Present options to client
            return {
                "status": "options_available",
                "message": "Found available lawyers for your consultation.",
                "intake_analysis": intake_result,
                "available_lawyers": [
                    {
                        "name": lawyer.name,
                        "rate": lawyer.hourly_rate,
                        "available_slots": lawyer.available_slots[:3]  # Show top 3 slots
                    }
                    for lawyer in available_lawyers
                ],
                "next_step": "client_selection"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"An error occurred while processing your request: {str(e)}"
            }
    
    async def confirm_booking(self, client_info: ClientInfo, lawyer_name: str, 
                            appointment_datetime: str, intake_analysis: Dict) -> BookingConfirmation:
        """Confirm and finalize the booking"""
        
        # Generate booking ID
        booking_id = f"LEG-{datetime.now().strftime('%Y%m%d')}-{hash(client_info.email) % 10000:04d}"
        
        # Create booking confirmation
        booking = BookingConfirmation(
            booking_id=booking_id,
            client_info=client_info,
            lawyer_name=lawyer_name,
            appointment_datetime=datetime.fromisoformat(appointment_datetime),
            duration_minutes=intake_analysis.get("estimated_duration", 60),
            practice_area=LegalPracticeArea(intake_analysis["practice_area"]),
            appointment_type=AppointmentType(intake_analysis.get("appointment_type", "consultation")),
            meeting_link="https://meet.google.com/abc-defg-hij" if "virtual" in appointment_datetime else None,
            office_location="Leaptra Law Offices, 123 Legal Blvd, Suite 100" if "office" in appointment_datetime else None
        )
        
        # Generate preparation notes
        booking.preparation_notes = await self.communication_agent.generate_preparation_notes(
            booking.practice_area,
            booking.appointment_type,
            intake_analysis["case_summary"]
        )
        
        # Save to database
        with sqlite3.connect(self.db.db_path) as conn:
            conn.execute("""
                INSERT INTO appointments 
                (id, client_name, client_email, client_phone, lawyer_id, 
                 appointment_datetime, duration_minutes, practice_area, 
                 appointment_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                booking_id,
                client_info.name,
                client_info.email,
                client_info.phone,
                "lawyer_1",  # In real implementation, get from lawyer selection
                booking.appointment_datetime.isoformat(),
                booking.duration_minutes,
                booking.practice_area.value,
                booking.appointment_type.value,
                datetime.now().isoformat()
            ))
        
        return booking

# Example Usage and Testing
async def main():
    """Example usage of the booking system"""
    
    booking_system = LawFirmBookingSystem()
    
    # Example 1: Initial inquiry
    user_message = """
    Hi, I need legal help. My business partner and I are having a dispute about 
    our partnership agreement. He wants to dissolve the partnership but I think 
    he's violating our contract. This is urgent as we have a board meeting next week.
    """
    
    print("=== Processing Initial Inquiry ===")
    result = await booking_system.process_booking_request(user_message)
    print(json.dumps(result, indent=2, default=str))
    
    # Example 2: Complete booking with client info
    client_info = ClientInfo(
        name="John Smith",
        email="john.smith@example.com",
        phone="555-123-4567",
        company="Smith & Associates"
    )
    
    print("\n=== Processing with Client Info ===")
    result_with_client = await booking_system.process_booking_request(
        user_message, client_info
    )
    print(json.dumps(result_with_client, indent=2, default=str))
    
    # Example 3: Confirm booking
    if result_with_client["status"] == "options_available":
        available_slots = result_with_client["available_lawyers"][0]["available_slots"]
        if available_slots:
            print("\n=== Confirming Booking ===")
            booking = await booking_system.confirm_booking(
                client_info=client_info,
                lawyer_name=result_with_client["available_lawyers"][0]["name"],
                appointment_datetime=available_slots[0]["datetime"],
                intake_analysis=result_with_client["intake_analysis"]
            )
            
            # Generate confirmation email
            confirmation_email = await booking_system.communication_agent.generate_confirmation_email(booking)
            
            print(f"Booking confirmed: {booking.booking_id}")
            print("\nConfirmation Email:")
            print(confirmation_email)
            print("\nPreparation Notes:")
            print(booking.preparation_notes)

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
