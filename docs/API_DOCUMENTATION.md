# AgroSense API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "AgroSense API",
  "version": "1.0.0",
  "timestamp": "2024-02-01T10:30:00"
}
```

---

### 2. Disease Detection

Detect plant diseases from leaf images.

**Endpoint:** `POST /api/detect-disease`

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `image`: File (required) - Plant leaf image (PNG, JPG, JPEG)

**Response:**
```json
{
  "success": true,
  "prediction": {
    "disease": "Tomato Early Blight",
    "confidence": 94.5,
    "severity": "Medium",
    "treatment": "Apply fungicides (Chlorothalonil, Mancozeb). Remove affected leaves.",
    "prevention": "Crop rotation, mulching, proper spacing",
    "organic_treatment": "Baking soda spray, neem oil"
  },
  "visualization": {
    "original_image": "data:image/png;base64,...",
    "heatmap": "data:image/png;base64,..."
  },
  "timestamp": "2024-02-01T10:30:00"
}
```

**Severity Levels:**
- `None` - Healthy plant
- `Low` - Minor issue
- `Medium` - Moderate attention needed
- `High` - Urgent action required

---

### 3. Weather Data

Get weather information and agricultural advisories.

**Endpoint:** `GET /api/weather`

**Query Parameters:**
- `lat` (optional) - Latitude (default: 12.9716)
- `lon` (optional) - Longitude (default: 77.5946)
- `location` (optional) - Location name (default: "Bangalore")

**Response:**
```json
{
  "success": true,
  "data": {
    "location": "Bangalore",
    "coordinates": {
      "lat": 12.9716,
      "lon": 77.5946
    },
    "current": {
      "temperature": 28.5,
      "feels_like": 30.2,
      "humidity": 65,
      "conditions": "Partly Cloudy",
      "wind_speed": 12.5,
      "precipitation": 0,
      "uv_index": 7
    },
    "forecast_3day": [
      {
        "day": "Today",
        "high": 32,
        "low": 24,
        "conditions": "Sunny",
        "rain_chance": 10
      }
    ],
    "agricultural_advisory": {
      "irrigation": "Moderate irrigation recommended",
      "spraying": "Good conditions for pesticide application",
      "disease_risk": "Moderate - Monitor for fungal diseases",
      "harvesting": "Favorable conditions"
    }
  }
}
```

---

### 4. Market Prices

Get crop market prices and selling recommendations.

**Endpoint:** `GET /api/market-prices`

**Query Parameters:**
- `crop` (optional) - Crop name (default: "tomato")
  - Supported: tomato, potato, onion, chili, rice

**Response:**
```json
{
  "success": true,
  "data": {
    "crop": "Tomato",
    "unit": "quintal",
    "current_price": 2550.00,
    "min_price": 2000.00,
    "max_price": 3200.00,
    "average_price": 2600.00,
    "trend": "increasing",
    "change_percent": 8.5,
    "forecast": {
      "next_week": 2700.00,
      "next_month": 2900.00,
      "confidence": "High"
    },
    "top_markets": [
      {
        "name": "APMC Bangalore",
        "price": 2800.00,
        "arrival": "125 quintals"
      }
    ],
    "recommendation": {
      "action": "HOLD",
      "reason": "Prices expected to rise 8-10% in next 2 weeks",
      "optimal_selling_time": "10-14 days"
    }
  }
}
```

**Recommendation Actions:**
- `BUY` - Good time to purchase inputs
- `HOLD` - Wait for better prices
- `SELL` - Current prices are favorable

---

### 5. AI Advisory

Get AI-powered agricultural advice.

**Endpoint:** `POST /api/advisory`

**Request:**
```json
{
  "query": "How to treat early blight in tomatoes?",
  "context": {
    "crop": "tomato",
    "disease": "early_blight",
    "severity": "medium"
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "Based on the detected disease, here's my recommendation:\n\n1. **Immediate Action**: Remove and destroy all infected plant parts...",
  "suggestions": [
    "How do I prevent this disease in future?",
    "Show me organic treatment options",
    "What's the best time to spray?"
  ],
  "timestamp": "2024-02-01T10:30:00"
}
```

---

### 6. Crop Recommendations

Get crop recommendations based on soil and season.

**Endpoint:** `POST /api/crop-recommendations`

**Request:**
```json
{
  "soil_type": "loamy",
  "season": "kharif",
  "region": "Karnataka"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recommended_crops": [
      {
        "name": "Tomato",
        "suitability": "Excellent",
        "expected_yield": "25-30 tons/hectare",
        "market_demand": "High",
        "profitability": "High",
        "season": "Year-round with irrigation"
      }
    ],
    "soil_management": {
      "ph_range": "6.0-7.0",
      "organic_matter": "Add 10-15 tons compost/hectare",
      "nutrients": "NPK as per soil test",
      "drainage": "Ensure good drainage system"
    },
    "irrigation": {
      "method": "Drip irrigation recommended",
      "frequency": "Every 2-3 days in summer",
      "quantity": "25-30mm per week"
    },
    "fertilizer_schedule": [
      {
        "stage": "Basal",
        "npk": "19:19:19",
        "quantity": "100 kg/ha"
      }
    ]
  }
}
```

---

## Error Responses

All endpoints may return error responses:

```json
{
  "error": "Error message description",
  "type": "error_type"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found
- `500` - Internal Server Error

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- 100 requests per minute per IP
- 1000 requests per day per user

---

## Authentication

Current version does not require authentication. For production deployment, implement:
- API Key authentication
- JWT tokens
- OAuth 2.0

---

## CORS

The API allows cross-origin requests from:
- http://localhost:3000
- http://localhost:8000
- http://127.0.0.1:8000

---

## Testing with cURL

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Disease Detection
```bash
curl -X POST \
  -F "image=@/path/to/leaf.jpg" \
  http://localhost:5000/api/detect-disease
```

### Weather Data
```bash
curl "http://localhost:5000/api/weather?location=Bangalore"
```

### Market Prices
```bash
curl "http://localhost:5000/api/market-prices?crop=tomato"
```

### AI Advisory
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"How to prevent fungal diseases?"}' \
  http://localhost:5000/api/advisory
```

---

## Future Enhancements

1. **Authentication System**
   - User registration and login
   - JWT-based authentication
   - Role-based access control

2. **Database Integration**
   - User history tracking
   - Disease detection logs
   - Crop recommendation history

3. **Real-time Features**
   - WebSocket support for live updates
   - Push notifications
   - Real-time market alerts

4. **Advanced ML Features**
   - Multi-crop disease detection
   - Pest identification
   - Yield prediction

5. **Mobile API**
   - Optimized endpoints for mobile apps
   - Offline mode support
   - Image compression

---

For questions or support, contact the development team.
