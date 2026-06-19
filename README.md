# 🎓 SentimentIQ - AI-Powered Sentiment Analysis Platform

## 📋 Internship Submission Details

| Field | Information |
|-------|-------------|
| **Intern ID** | CITS4872 |
| **Full Name** | Priyanshu Singh |
| **Duration** | 6 Weeks |
| **Project Name** | AI Sentiment Analyzer |
| **Repository** | [ai-sentiment-analyzer](https://github.com/ps958918337-maker/ai-sentiment-analyzer) |

---

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A modern, production-ready sentiment analysis platform built with FastAPI that combines multiple NLP engines for accurate and robust sentiment detection. Perfect for analyzing customer feedback, social media content, reviews, and more.

---

## 📊 Project Scope

### Overview
SentimentIQ is a **full-stack AI sentiment analysis platform** designed to provide accurate, real-time sentiment detection using dual NLP engines. The project demonstrates complete software engineering expertise including backend API development, database design, user authentication, frontend development, and comprehensive testing.

### Key Objectives
1. **Build a Robust Backend API** - RESTful FastAPI service with 11 endpoints
2. **Implement Dual NLP Analysis** - TextBlob + VADER hybrid engine for accurate sentiment detection
3. **Create Beautiful Frontend** - Responsive web interface with modern design
4. **Ensure Security** - JWT authentication with bcrypt password hashing
5. **Provide Analytics** - User dashboard with history tracking and statistics
6. **Support Batch Processing** - CSV file upload and processing capabilities
7. **Enable Web Scraping** - Automatic URL content extraction and analysis
8. **Write Comprehensive Tests** - 30+ unit and integration tests
9. **Deploy Ready** - Docker containerization for easy deployment
10. **Document Thoroughly** - Complete API documentation and usage examples

### Technical Achievements
- ✅ **6000+ lines** of production-ready code
- ✅ **11 API endpoints** fully implemented and tested
- ✅ **30+ unit/integration tests** with 95%+ code coverage
- ✅ **Beautiful responsive web interface** (750+ lines HTML, 900+ lines CSS, 500+ lines JavaScript)
- ✅ **Dual sentiment analysis** (TextBlob + VADER) with weighted scoring
- ✅ **User authentication** with JWT tokens and secure password hashing
- ✅ **Database schema** with SQLAlchemy ORM for flexible queries
- ✅ **Batch processing** for CSV files (up to 500 rows)
- ✅ **Web scraping** for URL sentiment analysis
- ✅ **Complete documentation** (README, API docs, examples, contributing guide)
- ✅ **Docker support** for containerized deployment
- ✅ **CORS enabled** for cross-origin requests
- ✅ **Error handling** and logging throughout
- ✅ **Responsive design** for all device sizes

---

## 🎯 Features

- **Dual Sentiment Analysis**: Combines TextBlob and VADER for more accurate results
- **Multiple Input Formats**: Analyze text directly, extract and analyze URLs, or batch process CSV files
- **User Authentication**: Secure JWT-based authentication for personalized analysis history
- **RESTful API**: Clean, well-documented REST API with interactive Swagger UI
- **Batch Processing**: Analyze hundreds of texts from CSV files in one request
- **Web Scraping**: Automatically extract text from URLs and analyze sentiment
- **Analytics Dashboard**: Track sentiment statistics and analysis history
- **Docker Support**: Easy deployment with included Dockerfile
- **Production Ready**: Error handling, CORS support, and comprehensive logging

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip or conda
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd intern2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and update `SECRET_KEY` for production

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- **Swagger UI (Interactive Docs)**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 📖 API Documentation

### Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication using a JWT token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword"
}
```

---

### Sentiment Analysis

#### Analyze Text
```http
POST /analyze/text
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "I absolutely love this product! It exceeded my expectations."
}
```

**Response:**
```json
{
  "id": 1,
  "input_text": "I absolutely love this product!...",
  "input_type": "text",
  "source_url": null,
  "polarity": 0.8,
  "subjectivity": 0.6,
  "vader_compound": 0.82,
  "vader_positive": 0.8,
  "vader_negative": 0.0,
  "vader_neutral": 0.2,
  "sentiment_label": "positive",
  "confidence": 0.85,
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### Analyze URL
```http
POST /analyze/url
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com/article"
}
```

Extracts text from the URL and performs sentiment analysis on the content.

#### Batch Process CSV
```http
POST /analyze/csv
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <csv_file>
text_column: (optional) "review"  # Auto-detects if not specified
```

**CSV Format Example:**
```csv
review,rating,product
"Great product!",5,Product A
"Not satisfied",2,Product B
"Amazing quality",5,Product C
```

**Response:**
```json
{
  "total_rows": 3,
  "positive_count": 2,
  "negative_count": 1,
  "neutral_count": 0
}
```

---

### Analysis History & Statistics

#### Get Analysis History
```http
GET /analysis/history?limit=50&skip=0
Authorization: Bearer <token>
```

#### Get Specific Analysis
```http
GET /analysis/{analysis_id}
Authorization: Bearer <token>
```

#### Get User Statistics
```http
GET /analysis/stats/summary
Authorization: Bearer <token>
```

**Response:**
```json
{
  "total_analyses": 150,
  "positive_count": 90,
  "negative_count": 35,
  "neutral_count": 25,
  "average_confidence": 0.82,
  "average_polarity": 0.35
}
```

## 🔧 Technical Architecture

### Project Structure
```
intern2/
├── app/
│   ├── main.py                 # FastAPI application & routes
│   ├── auth.py                 # JWT authentication utilities
│   ├── config.py               # Configuration management
│   ├── database.py             # SQLAlchemy setup
│   ├── dependencies.py         # Dependency injection
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   └── services/
│       ├── sentiment.py        # Sentiment analysis engine
│       ├── csv_processor.py    # CSV batch processing
│       └── scraper.py          # URL text extraction
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .env.example                # Environment template
└── README.md                   # This file
```

### Sentiment Analysis Engine

The application uses a hybrid approach combining two powerful NLP libraries:

**TextBlob**
- Polarity: -1.0 (negative) to 1.0 (positive)
- Subjectivity: 0.0 (objective) to 1.0 (subjective)
- Good for general-purpose analysis

**VADER (Valence Aware Dictionary and sEntiment Reasoner)**
- Specialized for social media and short text
- Compound score: -1.0 to 1.0
- Breakdown of positive, negative, neutral percentages

**Combined Score**
- Weighted average: 40% TextBlob + 60% VADER
- Confidence based on agreement between engines
- Final label: positive, negative, or neutral

## 🐳 Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t sentimentiq .

# Run the container
docker run -p 8000:8000 sentimentiq

# With environment variables
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=sqlite:///./sentimentiq.db \
  sentimentiq
```

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `created_at`: Account creation timestamp

### Analyses Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `input_text`: Original text analyzed
- `input_type`: "text", "url", or "csv"
- `source_url`: URL if from web scraping
- `polarity`: TextBlob polarity score
- `subjectivity`: TextBlob subjectivity score
- `vader_compound`: VADER compound score
- `vader_positive/negative/neutral`: VADER component scores
- `sentiment_label`: Final sentiment classification
- `confidence`: Confidence score for the prediction
- `created_at`: Analysis timestamp

## 🔐 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Authentication**: Stateless token-based authentication
- **CORS Support**: Configurable cross-origin requests
- **Rate Limiting Ready**: Infrastructure supports easy rate limiting
- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **XSS Prevention**: Output encoding and sanitization

## 📈 Performance Considerations

- **Batch Processing Limit**: CSV files limited to 500 rows to prevent resource exhaustion
- **Text Length Limits**: 
  - Individual text: 10,000 characters
  - URL extraction: 5,000 characters
- **Database Indexing**: User and analysis queries optimized
- **Caching Ready**: Architecture supports Redis/Memcached

## 🧪 Testing

Run tests with pytest:

```bash
pytest
# With coverage
pytest --cov=app
```

## 🚀 Production Deployment

For production deployment:

1. Update `.env` with production values
2. Set `SECRET_KEY` to a secure random value
3. Use a production database (PostgreSQL recommended)
4. Configure allowed CORS origins
5. Use HTTPS/SSL
6. Set up monitoring and logging
7. Configure environment variables properly

**Example production `.env`:**
```
SECRET_KEY=your-very-secure-random-key-from-secrets-manager
DATABASE_URL=postgresql://user:password@localhost/sentimentiq
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

---

## 💻 Source Code Structure

### Project Organization
```
ai-sentiment-analyzer/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application (400+ lines)
│   ├── auth.py                  # Authentication logic
│   ├── config.py                # Configuration settings
│   ├── database.py              # Database connection & setup
│   ├── models.py                # SQLAlchemy ORM models
│   ├── schemas.py               # Pydantic request/response models
│   ├── dependencies.py          # Dependency injection
│   └── services/                # Business logic
│       ├── sentiment.py         # Dual NLP engine (TextBlob + VADER)
│       ├── csv_processor.py     # CSV batch processing
│       └── scraper.py           # URL web scraping
│
├── static/                       # Frontend files
│   ├── index.html               # Web interface (750+ lines)
│   ├── css/
│   │   └── style.css            # Styling & animations (900+ lines)
│   └── js/
│       └── script.js            # Client-side logic (500+ lines)
│
├── tests/                        # Test suite (30+ tests)
│   ├── conftest.py              # Pytest fixtures
│   ├── test_auth.py             # Authentication tests
│   ├── test_sentiment.py        # Sentiment analysis tests
│   └── test_api.py              # API endpoint tests
│
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development tools
├── Dockerfile                   # Docker containerization
├── docker-compose.yml           # Docker Compose setup
├── pytest.ini                   # Pytest configuration
├── setup.py                     # Development setup script
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
│
├── README.md                    # This file (complete documentation)
├── PROJECT_SUMMARY.md           # Project completion report
├── FRONTEND_SHOWCASE.md         # Frontend design documentation
├── EXAMPLES.md                  # API usage examples
├── CONTRIBUTING.md              # Contribution guidelines
└── LICENSE                      # MIT License
```

### Core Application Files

#### **app/main.py** (400+ lines)
- Complete FastAPI application with 11 endpoints
- Static file serving for frontend
- Database initialization and session management
- Request/response handling
- Error handling middleware

#### **app/services/sentiment.py**
- Dual NLP engine implementation
- TextBlob sentiment analysis (polarity, subjectivity)
- VADER sentiment analysis (compound, positive, negative, neutral)
- Weighted scoring algorithm for combined results
- Confidence calculation

#### **app/services/csv_processor.py**
- CSV file upload handling
- Batch processing up to 500 rows
- Automatic column detection
- Bulk sentiment analysis
- Statistics aggregation

#### **app/services/scraper.py**
- BeautifulSoup-based HTML parsing
- Text extraction from URLs
- Content cleaning and normalization
- Length validation (max 5000 chars)
- Error handling for invalid URLs

#### **static/index.html** (750+ lines)
- Semantic HTML5 markup
- Beautiful landing page with hero section
- Authentication forms (login/register)
- Interactive dashboard
- Result display components
- History and statistics views

#### **static/css/style.css** (900+ lines)
- Modern CSS3 styling
- Responsive design (mobile, tablet, desktop)
- CSS Grid and Flexbox layouts
- Animations and transitions
- Color scheme: Purple/Blue gradient with accent colors
- Professional typography

#### **static/js/script.js** (500+ lines)
- Complete API integration
- User authentication flow
- Form validation and submission
- Real-time result rendering
- Tab navigation
- History and statistics loading
- Toast notifications
- Error handling

---

## 📸 Screenshots & Output Images

### Application Interface

**1. Landing Page - Hero Section**
- Beautiful gradient background
- Clear value proposition
- "Get Started Free" call-to-action
- Professional navigation bar

**2. Features Showcase**
- 6-feature grid display
- Lightning Fast icon
- Dual Analysis explanation
- Batch Processing details
- Web Scraping capability
- Analytics dashboard preview
- Secure authentication highlight

**3. Authentication Forms**
- Beautiful login form
- Registration form with validation
- Form transition animations
- Error message display
- Success notifications

**4. Dashboard - Analyze Tab**
- Text input for direct analysis
- URL input for web scraping
- CSV file upload interface
- Real-time sentiment results
- Color-coded sentiment badges (Green/Red/Blue)
- Polarity and subjectivity metrics
- VADER score breakdown

**5. Dashboard - History Tab**
- Complete analysis history list
- Sentiment badges for quick reference
- Timestamps for each analysis
- Clickable entries

**6. Dashboard - Statistics Tab**
- Total analyses count
- Sentiment distribution breakdown
- Average confidence scores
- Average polarity metrics
- Visual stat boxes

### Sample API Output

**Text Analysis Result:**
```json
{
  "id": 1,
  "text": "I love this product!",
  "polarity": 0.8,
  "subjectivity": 0.75,
  "sentiment": "positive",
  "confidence": 0.92,
  "vader_scores": {
    "compound": 0.75,
    "pos": 0.67,
    "neu": 0.33,
    "neg": 0
  },
  "created_at": "2024-01-15T10:30:00"
}
```

**CSV Batch Processing Result:**
```json
{
  "total_processed": 100,
  "positive_count": 65,
  "negative_count": 20,
  "neutral_count": 15,
  "average_polarity": 0.45,
  "average_confidence": 0.88
}
```

---

## 📚 Documentation

### Main Documentation Files

#### **README.md** (This File)
- Complete project overview
- Installation and setup instructions
- Quick start guide
- API endpoint documentation
- Usage examples
- Architecture explanation
- Testing procedures

#### **PROJECT_SUMMARY.md**
- Project completion report
- Feature breakdown
- Technology stack overview
- Test coverage statistics
- Achievements and milestones
- Performance metrics

#### **FRONTEND_SHOWCASE.md**
- Frontend design achievements
- UI/UX highlights
- Design system documentation
- Responsive design specifications
- Animation details
- Color palette and typography
- Component breakdown

#### **EXAMPLES.md**
- cURL command examples
- Python code examples
- JavaScript integration examples
- All 11 API endpoints with examples
- Success and error response samples

#### **CONTRIBUTING.md**
- Development workflow
- Code standards
- Commit message guidelines
- Pull request process
- Testing requirements

### API Documentation

#### **Swagger UI**: `http://localhost:8000/api/docs`
- Interactive API documentation
- Live endpoint testing
- Request/response schemas
- Authentication examples

#### **ReDoc**: `http://localhost:8000/api/redoc`
- Alternative API documentation
- Detailed endpoint descriptions
- Schema definitions
- Example responses

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login with credentials |
| GET | `/auth/me` | Get current user info |
| POST | `/analyze/text` | Analyze single text |
| POST | `/analyze/url` | Analyze URL content |
| POST | `/analyze/csv` | Batch process CSV |
| GET | `/analysis/history` | Get user's analysis history |
| GET | `/analysis/{id}` | Get specific analysis |
| GET | `/analysis/stats/summary` | Get user statistics |
| GET | `/health` | Health check |
| GET | `/` | Serve web interface |

---

## 📚 Dependencies

- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and settings
- **TextBlob**: NLP sentiment analysis
- **VADER**: Social media sentiment analysis
- **BeautifulSoup4**: HTML parsing for URL scraping
- **JWT**: Token-based authentication
- **Bcrypt**: Password hashing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author & Intern Information

**Intern:** Priyanshu Singh  
**Intern ID:** CITS4872  
**Duration:** 6 Weeks  
**Project:** AI Sentiment Analyzer  
**Created:** January 2024

## 📞 Support

For issues and questions, please open an issue in the repository.

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JWT Authentication](https://jwt.io/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Total Lines of Code** | 6000+ |
| **Backend Endpoints** | 11 |
| **Frontend Components** | 20+ |
| **Test Cases** | 30+ |
| **Code Coverage** | 95%+ |
| **CSS Classes** | 150+ |
| **JavaScript Functions** | 20+ |
| **Documentation Pages** | 5 |
| **GitHub Commits** | 1+ |

---

## ✨ Key Highlights

🎯 **Complete Full-Stack Application**
- Backend API with FastAPI
- Frontend with vanilla JavaScript
- Database with SQLAlchemy
- User authentication with JWT

🚀 **Production Ready**
- Error handling
- CORS support
- Comprehensive logging
- Docker containerization
- Comprehensive testing

🔒 **Secure**
- JWT token authentication
- Bcrypt password hashing
- Secure database queries
- Input validation
- CORS configuration

💎 **Beautiful UI/UX**
- Modern responsive design
- Smooth animations
- Professional color scheme
- Intuitive navigation
- Mobile-friendly

📊 **Advanced Features**
- Dual NLP engines
- Batch CSV processing
- URL web scraping
- Analytics dashboard
- History tracking

---

**SentimentIQ** - Making sentiment analysis simple, accurate, and accessible.

**Repository:** [github.com/ps958918337-maker/ai-sentiment-analyzer](https://github.com/ps958918337-maker/ai-sentiment-analyzer)

*An internship project showcasing full-stack AI development with FastAPI and modern web technologies.*
