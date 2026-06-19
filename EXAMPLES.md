# SentimentIQ API Usage Examples

This file contains practical examples of how to use the SentimentIQ API.

## Prerequisites

- API running at `http://localhost:8000`
- A valid JWT token (obtained from login/register)

## Examples using cURL

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

Response:
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

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### 3. Analyze Text

```bash
TOKEN="your-jwt-token-here"

curl -X POST "http://localhost:8000/analyze/text" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I absolutely love this product! It exceeded all my expectations."
  }'
```

Response:
```json
{
  "id": 1,
  "input_text": "I absolutely love this product!...",
  "input_type": "text",
  "sentiment_label": "positive",
  "polarity": 0.8,
  "subjectivity": 0.6,
  "vader_compound": 0.82,
  "confidence": 0.85,
  "created_at": "2024-01-15T10:35:00Z"
}
```

### 4. Analyze URL

```bash
curl -X POST "http://localhost:8000/analyze/url" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article"
  }'
```

### 5. Batch Process CSV

```bash
curl -X POST "http://localhost:8000/analyze/csv" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@reviews.csv" \
  -F "text_column=review"
```

CSV file format (reviews.csv):
```csv
review,rating,product
"Great product quality!",5,Widget A
"Not satisfied with the service",2,Widget B
"Amazing experience!",5,Widget C
```

### 6. Get Analysis History

```bash
curl -X GET "http://localhost:8000/analysis/history?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Get User Statistics

```bash
curl -X GET "http://localhost:8000/analysis/stats/summary" \
  -H "Authorization: Bearer $TOKEN"
```

Response:
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

## Examples using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepassword123"
    }
)
token = response.json()["access_token"]

# Analyze text
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/analyze/text",
    headers=headers,
    json={"text": "This product is amazing!"}
)
result = response.json()
print(f"Sentiment: {result['sentiment_label']}")
print(f"Confidence: {result['confidence']}")

# Get stats
response = requests.get(
    f"{BASE_URL}/analysis/stats/summary",
    headers=headers
)
stats = response.json()
print(f"Total analyses: {stats['total_analyses']}")
```

## Interactive Documentation

Visit `http://localhost:8000/api/docs` for the interactive Swagger UI where you can:
- View all available endpoints
- See request/response schemas
- Test endpoints directly in the browser
- Get parameter descriptions and requirements

## Response Format

All responses follow this structure:

### Success Response (200-201)
```json
{
  "data": "...",
  "message": "Operation successful"
}
```

### Error Response (400-500)
```json
{
  "detail": "Error description"
}
```

## Common Error Codes

- **401 Unauthorized**: Invalid or missing token
- **400 Bad Request**: Invalid request parameters
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

## Rate Limiting (Future)

Currently not implemented, but plan to add:
- 100 requests per minute per user
- 5 CSV uploads per hour per user
