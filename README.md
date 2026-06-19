# SentimentIQ - AI-Powered Sentiment Analysis Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A modern, production-ready sentiment analysis API built with FastAPI that combines multiple NLP engines for accurate and robust sentiment detection. Perfect for analyzing customer feedback, social media content, reviews, and more.

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

## 👨‍💻 Author

Created for internship submission - SentimentIQ Team

## 📞 Support

For issues and questions, please open an issue in the repository.

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

---

**SentimentIQ** - Making sentiment analysis simple, accurate, and accessible.
