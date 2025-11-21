# 📦 Project Setup
# FastAPI Calculator Application - Module 12

A production-ready REST API application with user authentication and calculation management, featuring complete CRUD operations, JWT authentication, and comprehensive testing.

## 🚀 Features

- ✅ User registration and authentication with JWT tokens
- ✅ Password hashing with bcrypt
- ✅ Calculation CRUD operations (BREAD pattern)
- ✅ Polymorphic calculation types (Addition, Subtraction, Multiplication, Division)
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Redis for token blacklisting
- ✅ Docker containerization
- ✅ Comprehensive test suite (105 tests)
- ✅ CI/CD pipeline with GitHub Actions
- ✅ API documentation with OpenAPI/Swagger

## 📋 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT tokens
- `POST /auth/token` - OAuth2 form-based login

### Calculations (BREAD)
- `POST /calculations` - **Add** a new calculation
- `GET /calculations` - **Browse** all calculations for current user
- `GET /calculations/{id}` - **Read** a specific calculation
- `PUT /calculations/{id}` - **Edit** a calculation (inputs and/or type)
- `DELETE /calculations/{id}` - **Delete** a calculation

### Health Check
- `GET /health` - Check API status

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115.8
- **Database**: PostgreSQL 17
- **ORM**: SQLAlchemy 2.0.38
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt (passlib)
- **Caching**: Redis 7
- **Testing**: pytest, pytest-cov
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Python Version**: 3.10

## 📦 Project Structure

```
kaw393939-module12_is601/
├── app/
│   ├── auth/           # Authentication logic (JWT, Redis)
│   ├── core/           # Configuration
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   └── main.py         # FastAPI application
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── e2e/            # End-to-end API tests
├── docker-compose.yml  # Multi-container setup
├── Dockerfile          # Application container
└── requirements.txt    # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.10+ (for local development)

### Installation & Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd kaw393939-module12_is601
```

2. **Start the application**
```bash
docker-compose up --build
```

This will start:
- **Web API** on http://localhost:8000
- **PostgreSQL** on localhost:5432
- **Redis** on localhost:6379
- **pgAdmin** on http://localhost:5050

3. **Access the API documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Running Tests

### Option 1: Using Docker (Recommended)

```bash
# Start services
docker-compose up -d

# Run all tests
docker-compose exec web pytest

# Run with coverage report
docker-compose exec web pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec web pytest tests/integration/test_user_auth.py -v
```

### Option 2: Local Testing

```bash
# Create virtual environment with Python 3.10
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Coverage

Current test coverage: **67%**

```
Name                         Coverage
------------------------------------------
app/models/calculation.py    92%
app/models/user.py           89%
app/schemas/calculation.py   92%
app/operations/__init__.py   100%
```

## 🔧 Configuration

Environment variables (set in `docker-compose.yml` or `.env`):

```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
JWT_SECRET_KEY=super-secret-key-for-jwt-min-32-chars
JWT_REFRESH_SECRET_KEY=super-refresh-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUNDS=12
REDIS_URL=redis://redis:6379/0
```

## 📖 API Usage Examples

### Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### Create a Calculation

```bash
curl -X POST "http://localhost:8000/calculations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "type": "addition",
    "inputs": [10.5, 3, 2]
  }'
```

### Update Calculation Type (NEW FEATURE)

```bash
curl -X PUT "http://localhost:8000/calculations/{calc_id}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "type": "multiplication",
    "inputs": [5, 4]
  }'
```

## 🐛 Issues Found & Fixed

### Issue #1: Calculation Type Update Not Supported

**Problem**: The PUT endpoint for updating calculations only allowed changing inputs, not the calculation type.

**Root Cause**: The `CalculationUpdate` schema didn't include a `type` field.

**Solution**: 
- Added optional `type` field to `CalculationUpdate` schema
- Modified endpoint logic to handle polymorphic type changes
- Preserves calculation ID and creation timestamp during type changes

**Testing**: Added comprehensive tests in `test_calculation_schema.py`

### Issue #2: Python 3.12 Compatibility

**Problem**: Tests failing with `ModuleNotFoundError: No module named 'distutils'`

**Root Cause**: 
- Local environment using Python 3.12
- `aioredis==2.0.1` requires `distutils` (removed in Python 3.11+)

**Solution**: Use Python 3.10 for consistency with Docker environment

## 🚢 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/test.yml`):

1. **Test Stage**:
   - Sets up PostgreSQL database
   - Runs unit tests
   - Runs integration tests
   - Runs E2E tests
   - Generates coverage report

2. **Security Stage**:
   - Builds Docker image
   - Scans for vulnerabilities with Trivy
   - Fails on CRITICAL/HIGH severity issues

3. **Deploy Stage** (main branch only):
   - Builds multi-platform Docker image
   - Pushes to Docker Hub
   - Tags with `latest` and commit SHA

## 🐳 Docker Hub

**Repository**: saimquadri/601_module12

**Pull the image**:
```bash
docker pull saimquadri/601_module12:latest
```

**Run the container**:
```bash
docker run -p 8000:8000 saimquadri/601_module12:latest
```

## 📝 Development Notes

### Database Schema

- **Users Table**: Stores user accounts with hashed passwords
- **Calculations Table**: Polymorphic table storing all calculation types
- **Relationships**: One-to-Many (User → Calculations) with cascade delete

### Authentication Flow

1. User registers → Password hashed with bcrypt
2. User logs in → JWT access token + refresh token generated
3. Protected endpoints → Verify JWT token via dependency injection
4. Token expiration → Access: 30 minutes, Refresh: 7 days

### Calculation Types

All calculations use polymorphic inheritance:
- **Addition**: Sum of all inputs
- **Subtraction**: Sequential subtraction from first input
- **Multiplication**: Product of all inputs
- **Division**: Sequential division from first input (prevents division by zero)

## 🎓 Learning Outcomes Achieved

- ✅ CLO3: Python applications with automated testing
- ✅ CLO4: GitHub Actions for CI/CD
- ✅ CLO9: Docker containerization
- ✅ CLO10: REST API creation and testing
- ✅ CLO11: SQL database integration
- ✅ CLO12: JSON serialization with Pydantic
- ✅ CLO13: Secure authentication (JWT, bcrypt)

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Links

- [Docker Hub Repository](https://hub.docker.com/r/saimquadri/601_module12)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)