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
cd appt-booking-system
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
class NotificationService:
    def __init__(self):
        self.channels = []
    
    async def send_booking_confirmation(self, booking: BookingConfirmation):
        # Email notification
        await self.send_email(booking)
        # SMS notification
        await self.send_sms(booking)
        # Slack notification to law firm
        await self.send_slack_notification(booking)
    
    async def send_email(self, booking: BookingConfirmation):
        # Implementation for email sending
        pass
```

### Analytics Integration
```python
class BookingAnalytics:
    def __init__(self):
        self.metrics = {}
    
    def track_booking(self, booking: BookingConfirmation):
        practice_area = booking.practice_area.value
        self.metrics[practice_area] = self.metrics.get(practice_area, 0) + 1
    
    def get_popular_practice_areas(self):
        return sorted(self.metrics.items(), key=lambda x: x[1], reverse=True)
```

## 🐛 Troubleshooting

### Common Issues

#### Issue: OpenAI API Rate Limits
```python
# Solution: Implement exponential backoff
import time
import random

async def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except openai.RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(wait_time)
```

#### Issue: Database Connection Errors
```python
# Solution: Connection pooling and retry logic
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(database_url, timeout=30.0)
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
```

#### Issue: Invalid Client Data
```python
# Solution: Enhanced validation with custom messages
from pydantic import validator, ValidationError

class ClientInfo(BaseModel):
    # ... existing fields ...
    
    @validator('email')
    def validate_email_domain(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        domain = v.split('@')[1]
        # Add domain validation logic
        return v
```

### Debug Mode
Enable detailed logging:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('law_firm_booking.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

## 📊 Performance Optimization

### Caching Strategy
```python
from functools import lru_cache
import redis

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    @lru_cache(maxsize=100)
    def get_lawyer_availability(self, lawyer_id: str, date: str):
        # Cache lawyer availability for frequently accessed data
        return self.redis_client.get(f"availability:{lawyer_id}:{date}")
```

### Database Optimization
```sql
-- Add indexes for better query performance
CREATE INDEX idx_appointments_datetime ON appointments(appointment_datetime);
CREATE INDEX idx_appointments_lawyer_id ON appointments(lawyer_id);
CREATE INDEX idx_lawyers_practice_areas ON lawyers(practice_areas);
```

### Async Processing
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncBookingProcessor:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_booking_batch(self, bookings: List[dict]):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self.process_single_booking, booking)
            for booking in bookings
        ]
        return await asyncio.gather(*tasks)
```

## 🔐 Advanced Security

### JWT Authentication
```python
import jwt
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def generate_token(self, user_id: str) -> str:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
```

### Input Sanitization
```python
import html
import re

class InputSanitizer:
    @staticmethod
    def sanitize_text(text: str) -> str:
        # Remove HTML tags and escape special characters
        text = re.sub(r'<[^>]+>', '', text)
        text = html.escape(text)
        return text.strip()
    
    @staticmethod
    def validate_phone(phone: str) -> str:
        # Remove all non-digit characters
        digits = re.sub(r'[^\d]', '', phone)
        if len(digits) < 10:
            raise ValueError("Invalid phone number")
        return digits
```

## 📱 Mobile Integration

### React Native Component
```javascript
// BookingComponent.js
import React, { useState } from 'react';
import { View, TextInput, Button, Alert } from 'react-native';

const BookingComponent = () => {
  const [message, setMessage] = useState('');
  const [clientInfo, setClientInfo] = useState({});

  const submitBooking = async () => {
    try {
      const response = await fetch('https://api.leaptra.com/api/book-consultation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, client_info: clientInfo })
      });
      const result = await response.json();
      Alert.alert('Success', 'Booking request processed');
    } catch (error) {
      Alert.alert('Error', 'Failed to process booking');
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Describe your legal need..."
        value={message}
        onChangeText={setMessage}
        multiline
      />
      <Button title="Book Consultation" onPress={submitBooking} />
    </View>
  );
};

export default BookingComponent;
```

## 🔄 Webhook Integration

### Webhook Handler
```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhooks/calendar-update', methods=['POST'])
def handle_calendar_update():
    # Verify webhook signature
    signature = request.headers.get('X-Webhook-Signature')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    data = request.json
    # Process calendar update
    booking_id = data.get('booking_id')
    new_status = data.get('status')
    
    # Update booking status in database
    update_booking_status(booking_id, new_status)
    
    return jsonify({'status': 'success'})

def verify_signature(payload, signature):
    expected = hmac.new(
        webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## 📈 Scaling Considerations

### Load Balancing
```python
# nginx.conf
upstream law_firm_api {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://law_firm_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Database Sharding
```python
class ShardedDatabase:
    def __init__(self, shard_configs):
        self.shards = {}
        for name, config in shard_configs.items():
            self.shards[name] = sqlite3.connect(config['path'])
    
    def get_shard(self, client_id: str):
        # Simple hash-based sharding
        shard_key = hash(client_id) % len(self.shards)
        return list(self.shards.values())[shard_key]
```

### Microservices Architecture
```python
# services/intake_service.py
from fastapi import FastAPI

app = FastAPI(title="Intake Service")

@app.post("/analyze-inquiry")
async def analyze_inquiry(inquiry: dict):
    # Intake agent logic
    return {"analysis": "result"}

# services/scheduling_service.py
app = FastAPI(title="Scheduling Service")

@app.post("/find-availability")
async def find_availability(request: dict):
    # Scheduling agent logic
    return {"availability": "slots"}
```

## 🧪 Testing Strategy

### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch
from law_firm_booking import IntakeAgent, ClientInfo

@pytest.fixture
def mock_openai_client():
    client = Mock()
    client.chat.completions.create.return_value.choices[0].message.function_call.arguments = """
    {
        "practice_area": "corporate",
        "urgency": "high",
        "case_summary": "Contract dispute"
    }
    """
    return client

@pytest.mark.asyncio
async def test_intake_agent_analysis(mock_openai_client):
    agent = IntakeAgent(mock_openai_client)
    result = await agent.process_initial_inquiry("I have a contract dispute")
    
    assert result["practice_area"] == "corporate"
    assert result["urgency"] == "high"
    assert "contract dispute" in result["case_summary"].lower()
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_complete_booking_flow():
    booking_system = LawFirmBookingSystem()
    
    # Test complete flow
    inquiry = "I need help with a divorce case"
    client_info = ClientInfo(
        name="Test Client",
        email="test@example.com",
        phone="5551234567"
    )
    
    result = await booking_system.process_booking_request(inquiry, client_info)
    assert result["status"] in ["options_available", "needs_client_info"]
```

### Load Testing
```python
import asyncio
import aiohttp
import time

async def load_test_booking_endpoint():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):  # 100 concurrent requests
            task = session.post(
                'http://localhost:8000/api/book-consultation',
                json={
                    "message": f"Test inquiry {i}",
                    "client_info": {
                        "name": f"Test Client {i}",
                        "email": f"test{i}@example.com",
                        "phone": "5551234567"
                    }
                }
            )
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        success_count = sum(1 for r in responses if not isinstance(r, Exception))
        print(f"Completed {success_count}/100 requests in {end_time - start_time:.2f}s")
```

## 📚 Best Practices

### Code Organization
```
law_firm_booking/
├── __init__.py
├── agents/
│   ├── __init__.py
│   ├── intake_agent.py
│   ├── scheduling_agent.py
│   └── communication_agent.py
├── models/
│   ├── __init__.py
│   ├── client.py
│   ├── appointment.py
│   └── lawyer.py
├── services/
│   ├── __init__.py
│   ├── database.py
│   ├── notifications.py
│   └── integrations.py
├── utils/
│   ├── __init__.py
│   ├── validators.py
│   └── helpers.py
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

### Error Handling
```python
class BookingSystemError(Exception):
    """Base exception for booking system"""
    pass

class ValidationError(BookingSystemError):
    """Raised when validation fails"""
    pass

class AvailabilityError(BookingSystemError):
    """Raised when no availability found"""
    pass

class AIProcessingError(BookingSystemError):
    """Raised when AI processing fails"""
    pass

# Usage
try:
    result = await booking_system.process_booking_request(message)
except ValidationError as e:
    return {"error": "Invalid input", "details": str(e)}
except AvailabilityError as e:
    return {"error": "No availability", "alternatives": True}
```

### Configuration Management
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str = "sqlite:///bookings.db"
    debug: bool = False
    log_level: str = "INFO"
    max_booking_days: int = 90
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Add docstrings for public methods
- Maximum line length: 88 characters
- Use Black for code formatting: `black .`

### Commit Messages
Follow conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding tests
- `refactor:` for code refactoring

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Pydantic team for excellent data validation
- FastAPI for the modern web framework
- The open-source community for various tools and libraries

## 📞 Support

For support and questions:

- **Issues**: https://github.com/Mathinz/appointment-booking-app/issues
- **Discussions**: https://github.com/Mathinz/appointment-booking-app/discussions

## 🗺️ Roadmap

### Version 2.0 (Q2 2024)
- [ ] Voice-to-text integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (iOS/Android)

### Version 2.1 (Q3 2024)
- [ ] Machine learning for better lawyer matching
- [ ] Integration with major CRM systems
- [ ] Automated follow-up sequences
- [ ] Video consultation platform

### Version 3.0 (Q4 2024)
- [ ] Blockchain-based smart contracts
- [ ] AI-powered legal document generation
- [ ] Advanced reporting and insights
- [ ] Enterprise-grade security features

---

**Built with ❤️ for the legal industry by the Leaptra team**
