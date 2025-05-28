# appointment-booking-app

# Law Firm AI Booking System

A sophisticated multi-agent AI system for automating legal appointment booking using OpenAI's GPT-4 and Pydantic validation frameworks. Designed specifically for modern law firms like Leaptra.com.

## 🏛️ Overview

This system revolutionizes legal appointment booking by using multiple specialized AI agents that work together to understand client needs, match them with appropriate lawyers, and handle all communication seamlessly.

## 🎯 Key Features

### Multi-Agent Architecture
- **Intake Agent**: Natural language processing for client inquiry analysis
- **Scheduling Agent**: Intelligent lawyer matching and availability management
- **Communication Agent**: Professional email generation and client communication

### Advanced AI Capabilities
- **Natural Language Understanding**: Processes client inquiries in plain English
- **Practice Area Classification**: Automatically identifies legal specialization needed
- **Urgency Assessment**: Prioritizes appointments based on case sensitivity
- **Smart Matching**: Finds optimal lawyer-client pairings

### Professional Features
- **Automated Confirmations**: Generates professional appointment confirmations
- **Preparation Guidance**: Provides case-specific preparation notes
- **Multi-channel Support**: Web, mobile, API, and voice interfaces
- **Real-time Scheduling**: Instant availability checking and booking

## 🔧 Technical Stack

- **AI Framework**: OpenAI GPT-4 with Function Calling
- **Data Validation**: Pydantic models for type safety
- **Database**: SQLite with async support
- **Language**: Python 3.8+
- **Architecture**: Event-driven, microservices-ready

## 📋 Prerequisites

Before installation, ensure you have:

- Python 3.8 or higher
- OpenAI API key
- pip package manager
- Git (for cloning)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/law-firm-booking-system.git
cd law-firm-booking-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///law_firm_bookings.db
DEBUG=True
LOG_LEVEL=INFO
```

### 5. Initialize Database
```bash
python -c "from law_firm_booking import DatabaseManager; DatabaseManager().init_database()"
```

## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
openai>=1.0.0
pydantic>=2.0.0
sqlite3
asyncio
python-dotenv>=1.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
email-validator>=2.1.0
```

## 🎮 Quick Start

### Basic Usage Example

```python
import asyncio
from law_firm_booking import LawFirmBookingSystem, ClientInfo

async def main():
    # Initialize the system
    booking_system = LawFirmBookingSystem()
    
    # Process client inquiry
    user_message = """
    I need help with a contract dispute. My vendor is not 
    delivering as promised and I need legal advice urgently.
    """
    
    # Get initial analysis
    result = await booking_system.process_booking_request(user_message)
    print("Analysis:", result)
    
    # Provide client information
    client_info = ClientInfo(
        name="Jane Doe",
        email="jane@example.com",
        phone="555-0123",
        company="Doe Enterprises"
    )
    
    # Complete booking process
    booking_result = await booking_system.process_booking_request(
        user_message, client_info
    )
    print("Booking Options:", booking_result)

# Run the example
asyncio.run(main())
```

### Web API Integration

```python
from fastapi import FastAPI, HTTPException
from law_firm_booking import LawFirmBookingSystem

app = FastAPI(title="Law Firm Booking API")
booking_system = LawFirmBookingSystem()

@app.post("/api/book-consultation")
async def book_consultation(request: dict):
    try:
        result = await booking_system.process_booking_request(
            request["message"], 
            request.get("client_info")
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/lawyers/{practice_area}")
async def get_lawyers(practice_area: str):
    lawyers = await booking_system.scheduling_agent.find_available_lawyers(
        practice_area, ["2024-01-15", "2024-01-16"]
    )
    return {"lawyers": lawyers}
```

## 📊 System Architecture

The system follows a layered architecture:

1. **Client Interface Layer**: Web, mobile, API endpoints
2. **Orchestrator Layer**: Main business logic and coordination
3. **AI Agent Layer**: Specialized AI agents for different tasks
4. **Data Layer**: Database and validation components
5. **External Services**: OpenAI API and third-party integrations

## 🔄 Process Flow

1. **Client Input**: User describes their legal need
2. **Intake Analysis**: AI extracts case details and requirements
3. **Lawyer Matching**: System finds available qualified lawyers
4. **Booking Options**: Present choices to client
5. **Confirmation**: Generate confirmations and preparation notes

## 🏗️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `DATABASE_URL` | Database connection string | No | `sqlite:///bookings.db` |
| `DEBUG` | Enable debug mode | No | `False` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `MAX_BOOKING_DAYS` | Maximum days ahead for booking | No | `90` |

### Practice Areas Configuration

The system supports these legal practice areas:
- Corporate Law
- Litigation
- Family Law
- Real Estate
- Criminal Law
- Immigration
- Intellectual Property
- Employment Law

### Appointment Types
- Initial Consultation
- Follow-up Meeting
- Document Review
- Court Preparation
- Contract Review

## 🔌 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/book-consultation` | POST | Process booking request |
| `/api/lawyers/{practice_area}` | GET | Get available lawyers |
| `/api/appointments/{booking_id}` | GET | Get appointment details |
| `/api/appointments/{booking_id}/cancel` | DELETE | Cancel appointment |
| `/api/availability` | GET | Check lawyer availability |

### Request/Response Examples

#### Book Consultation
```json
// Request
{
  "message": "I need help with a divorce case",
  "client_info": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "555-0123"
  }
}

// Response
{
  "status": "options_available",
  "available_lawyers": [
    {
      "name": "Emily Rodriguez",
      "rate": 350.0,
      "available_slots": [
        {"datetime": "2024-01-15T10:00:00", "duration_available": 120}
      ]
    }
  ]
}
```

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Run Integration Tests
```bash
pytest tests/integration/ -v
```

### Test Coverage
```bash
pytest --cov=law_firm_booking tests/
```

### Manual Testing
```bash
python examples/test_booking_flow.py
```

## 📈 Monitoring & Logging

### Application Logs
The system generates structured logs for:
- Client interactions
- AI agent decisions
- Booking confirmations
- Error tracking
- Performance metrics

### Health Checks
```bash
curl http://localhost:8000/health
```

### Metrics Endpoints
- `/metrics/bookings` - Booking statistics
- `/metrics/agents` - AI agent performance
- `/metrics/errors` - Error rates and types

## 🔒 Security

### Data Protection
- Client information encrypted at rest
- API endpoints secured with JWT tokens
- Input validation using Pydantic models
- SQL injection prevention
- Rate limiting implemented

### Privacy Compliance
- GDPR compliant data handling
- Client consent management
- Data retention policies
- Audit trail logging

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --port 8000
```

### Production
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment-Specific Configs

#### Staging
```yaml
# docker-compose.staging.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - DEBUG=False
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
```

#### Production
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - DEBUG=False
      - LOG_LEVEL=WARNING
    ports:
      - "80:8000"
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
```

## 🔧 Customization

### Adding New Practice Areas
```python
class LegalPracticeArea(str, Enum):
    # Existing areas...
    TAX_LAW = "tax_law"
    BANKRUPTCY = "bankruptcy"
    ENVIRONMENTAL = "environmental"
```

### Custom AI Prompts
```python
class CustomIntakeAgent(IntakeAgent):
    def __init__(self, openai_client):
        super().__init__(openai_client)
        self.system_prompt = """
        Your custom prompt for specific law firm needs...
        """
```

### Database Schema Extensions
```sql
-- Add custom fields to appointments table
ALTER TABLE appointments ADD COLUMN case_type TEXT;
ALTER TABLE appointments ADD COLUMN estimated_value DECIMAL(10,2);
```

## 🔄 Integration Examples

### Calendar Integration (Google Calendar)
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class GoogleCalendarIntegration:
    def __init__(self, credentials):
        self.service = build('calendar', 'v3', credentials=credentials)
    
    async def create_event(self, booking: BookingConfirmation):
        event = {
            'summary': f'Legal Consultation - {booking.client_info.name}',
            'start': {'dateTime': booking.appointment_datetime.isoformat()},
            'end': {'dateTime': (booking.appointment_datetime + 
                   timedelta(minutes=booking.duration_minutes)).isoformat()}
        }
        return self.service.events().insert(calendarId='primary', body=event).execute()
```

### CRM Integration (Salesforce)
```python
from simple_salesforce import Salesforce

class SalesforceIntegration:
    def __init__(self, username, password, security_token):
        self.sf = Salesforce(username=username, password=password, 
                           security_token=security_token)
    
    async def create_lead(self, client_info: ClientInfo):
        return self.sf.Lead.create({
            'FirstName': client_info.name.split()[0],
            'LastName': ' '.join(client_info.name.split()[1:]),
            'Email': client_info.email,
            'Phone': client_info.phone,
            'Company': client_info.company or 'Individual'
        })
```

## 📚 Advanced Usage

### Batch Processing
```python
async def process_multiple_inquiries(inquiries: List[str]):
    results = []
    for inquiry in inquiries:
        result = await booking_system.process_booking_request(inquiry)
        results.append(result)
    return results
```

### Custom Notifications
```python
