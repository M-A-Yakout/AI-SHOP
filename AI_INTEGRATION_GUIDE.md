# AI Integration Guide

Complete guide for the OpenAI API integration in the Django ecommerce project.

---

## Overview

The AI integration provides two main features:
1. **Product Assistant** - Enhances product information with AI
2. **Store Generator** - Creates complete store structures from ideas

Both features support:
- ✅ OpenAI API integration
- ✅ Automatic fallback to mock mode
- ✅ Comprehensive error handling
- ✅ Usage tracking and analytics

---

## Architecture

### Service Layer (`ai_assistant/services.py`)

**AIService Class**:
- Handles OpenAI API communication
- Provides automatic fallback to mock mode
- Logs all requests to database
- Tracks token usage and processing time

**Key Methods**:
- `product_assist(product_data, user)` - Enhance product information
- `store_generator(store_idea, user)` - Generate store structure

### API Endpoints (`ai_assistant/views.py`)

**Endpoints**:
1. `POST /api/ai/product-assist/` - Product enhancement
2. `POST /api/ai/store-generator/` - Store generation
3. `GET /api/ai/usage-stats/` - Usage statistics

---

## Configuration

### Environment Variables

Add to `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
AI_MOCK_MODE=False
```

**Variables**:
- `OPENAI_API_KEY` - Your OpenAI API key (get from https://platform.openai.com/)
- `OPENAI_MODEL` - Model to use (default: gpt-3.5-turbo, can use gpt-4)
- `AI_MOCK_MODE` - Force mock mode (True/False)

### Settings (`config/settings.py`)

Already configured:

```python
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
OPENAI_MODEL = config('OPENAI_MODEL', default='gpt-3.5-turbo')
AI_MOCK_MODE = config('AI_MOCK_MODE', default=not bool(OPENAI_API_KEY), cast=bool)
```

---

## Usage

### 1. Product Assistant

**Endpoint**: `POST /api/ai/product-assist/`

**Request**:
```json
{
  "name": "Wireless Bluetooth Headphones",
  "description": "High quality headphones with noise cancellation",
  "category": "Electronics",
  "price": "79.99"
}
```

**Response**:
```json
{
  "improved_title": "Premium Wireless Bluetooth Headphones - Noise Cancelling",
  "seo_description": "Experience superior sound quality with our Premium Wireless Bluetooth Headphones featuring advanced noise cancellation technology...",
  "category_suggestions": [
    "Electronics",
    "Audio & Headphones",
    "Wireless Accessories",
    "Consumer Electronics"
  ],
  "tags": [
    "wireless",
    "bluetooth",
    "noise-cancelling",
    "premium",
    "audio",
    "headphones"
  ],
  "meta_title": "Buy Premium Wireless Headphones | Noise Cancelling",
  "meta_description": "Shop premium wireless Bluetooth headphones with noise cancellation. Superior sound quality, long battery life, and comfortable design.",
  "tokens_used": 245,
  "mode": "openai",
  "processing_time": 1.23,
  "success": true
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/ai/product-assist/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "description": "Bluetooth headphones with noise cancellation"
  }'
```

### 2. Store Generator

**Endpoint**: `POST /api/ai/store-generator/`

**Request**:
```json
{
  "idea": "organic skincare products"
}
```

**Response**:
```json
{
  "store": {
    "name": "Organic Skincare Store",
    "description": "Your trusted source for natural, organic skincare products. We offer premium, eco-friendly beauty solutions for all skin types.",
    "tagline": "Natural beauty, naturally"
  },
  "categories": [
    {
      "name": "Cleansers",
      "description": "Gentle organic face and body cleansers"
    },
    {
      "name": "Moisturizers",
      "description": "Hydrating organic creams and lotions"
    },
    {
      "name": "Serums",
      "description": "Concentrated organic treatment serums"
    }
  ],
  "sample_products": [
    {
      "name": "Organic Rose Water Toner",
      "description": "Pure rose water toner for all skin types",
      "price": 24.99,
      "category": "Toners"
    },
    {
      "name": "Vitamin C Serum",
      "description": "Brightening organic vitamin C serum",
      "price": 39.99,
      "category": "Serums"
    }
  ],
  "tokens_used": 450,
  "mode": "openai",
  "processing_time": 2.15,
  "success": true
}
```

### 3. Usage Statistics

**Endpoint**: `GET /api/ai/usage-stats/`

**Response**:
```json
{
  "total_requests": 15,
  "product_assist_count": 10,
  "store_generator_count": 5,
  "total_tokens_used": 3250,
  "avg_processing_time": 1.45,
  "success": true
}
```

---

## Modes of Operation

### OpenAI API Mode

**When Active**:
- `OPENAI_API_KEY` is set
- `AI_MOCK_MODE=False`
- OpenAI package is installed

**Features**:
- Real AI-generated content
- Token usage tracking
- Higher quality responses
- Costs money (per token)

**Response Indicator**:
```json
{
  "mode": "openai",
  "tokens_used": 245
}
```

### Mock Mode

**When Active**:
- No `OPENAI_API_KEY` set
- `AI_MOCK_MODE=True`
- OpenAI API fails
- OpenAI package not installed

**Features**:
- Free to use
- Instant responses
- Template-based generation
- No API calls

**Response Indicator**:
```json
{
  "mode": "mock",
  "tokens_used": 0
}
```

### Automatic Fallback

If OpenAI API fails, the system automatically falls back to mock mode:

```json
{
  "mode": "mock",
  "fallback_used": true,
  "error_message": "OpenAI API error: Rate limit exceeded",
  "improved_title": "Premium Wireless Headphones - High Quality",
  ...
}
```

---

## Error Handling

### Input Validation Errors (400)

```json
{
  "error": "Invalid input",
  "details": {
    "name": ["This field is required."]
  },
  "success": false
}
```

### Service Errors (500)

```json
{
  "error": "AI service error",
  "message": "OpenAI API error: Invalid API key",
  "success": false
}
```

### Automatic Recovery

The service automatically:
1. Catches OpenAI API errors
2. Falls back to mock mode
3. Returns valid response
4. Logs the error

---

## Testing

### Run Test Suite

```bash
python test_ai_integration.py
```

**Tests**:
- ✅ Mock mode functionality
- ✅ OpenAI API mode (if key configured)
- ✅ Error handling and fallback
- ✅ Input validation

### Manual Testing with Swagger UI

1. Go to http://localhost:8000/api/docs/
2. Click "Authorize" and enter your JWT token
3. Navigate to "AI Assistant" section
4. Try "POST /api/ai/product-assist/"
5. Click "Try it out"
6. Enter test data
7. Click "Execute"

### Test with cURL

**Get Access Token**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Test Product Assist**:
```bash
curl -X POST http://localhost:8000/api/ai/product-assist/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smart Watch",
    "description": "Fitness tracking watch"
  }'
```

---

## OpenAI API Setup

### 1. Get API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new secret key
5. Copy the key (you won't see it again!)

### 2. Configure Project

Add to `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
AI_MOCK_MODE=False
```

### 3. Verify Configuration

```bash
python test_ai_integration.py
```

Should show:
```
✓ Service initialized with OpenAI API
✓ OpenAI response received
```

---

## Cost Management

### Token Usage

**Approximate costs** (GPT-3.5-turbo):
- Product Assist: ~200-300 tokens (~$0.0003)
- Store Generator: ~400-600 tokens (~$0.0006)

**Track usage**:
```bash
curl http://localhost:8000/api/ai/usage-stats/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Cost Optimization

1. **Use Mock Mode for Development**:
   ```env
   AI_MOCK_MODE=True
   ```

2. **Set Token Limits**:
   ```python
   # In services.py
   max_tokens=500  # Limit response length
   ```

3. **Cache Results**:
   - Store AI responses in database
   - Reuse for similar requests

4. **Use GPT-3.5 Instead of GPT-4**:
   ```env
   OPENAI_MODEL=gpt-3.5-turbo  # Cheaper
   # vs
   OPENAI_MODEL=gpt-4  # More expensive
   ```

---

## Database Tracking

### AIRequest Model

All AI requests are logged:

```python
class AIRequest(models.Model):
    user = ForeignKey(User)
    request_type = CharField()  # 'product_assist' or 'store_generator'
    input_data = JSONField()
    output_data = JSONField()
    tokens_used = IntegerField()
    processing_time = FloatField()
    created_at = DateTimeField()
```

### View Logs in Admin

1. Go to http://localhost:8000/admin/
2. Navigate to "AI Requests"
3. View all AI interactions

---

## Troubleshooting

### Issue: "Service in mock mode despite API key"

**Causes**:
- Invalid API key
- OpenAI package not installed
- Network issues

**Solutions**:
```bash
# Check API key
echo $OPENAI_API_KEY

# Reinstall OpenAI
pip install --upgrade openai

# Test connection
python test_ai_integration.py
```

### Issue: "Rate limit exceeded"

**Solution**:
- Wait a few minutes
- Upgrade OpenAI plan
- Use mock mode temporarily

### Issue: "Invalid JSON response"

**Cause**: OpenAI returned non-JSON

**Solution**: Already handled - falls back to mock mode

### Issue: "Tokens used is 0"

**Cause**: Running in mock mode

**Check**:
```bash
# View response
curl http://localhost:8000/api/ai/product-assist/ \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"Test"}' | jq '.mode'

# Should show "openai" not "mock"
```

---

## Best Practices

### 1. Development

```env
# Use mock mode for development
AI_MOCK_MODE=True
```

### 2. Testing

```env
# Use real API for testing
AI_MOCK_MODE=False
OPENAI_API_KEY=your-test-key
```

### 3. Production

```env
# Use real API with monitoring
AI_MOCK_MODE=False
OPENAI_API_KEY=your-production-key
OPENAI_MODEL=gpt-3.5-turbo
```

### 4. Error Handling

Always check response:
```python
result = ai_service.product_assist(data)

if result.get('fallback_used'):
    # Handle fallback case
    logger.warning(f"AI fallback used: {result.get('error_message')}")

if result.get('mode') == 'mock':
    # Running in mock mode
    pass
```

---

## API Reference

### ProductAssistRequestSerializer

**Fields**:
- `name` (required): Product name
- `description` (optional): Product description
- `category` (optional): Product category
- `price` (optional): Product price

### ProductAssistResponseSerializer

**Fields**:
- `improved_title`: Enhanced product title
- `seo_description`: SEO-optimized description
- `category_suggestions`: List of categories
- `tags`: List of product tags
- `meta_title`: SEO meta title
- `meta_description`: SEO meta description
- `tokens_used`: Tokens consumed
- `mode`: 'openai' or 'mock'
- `processing_time`: Time in seconds
- `success`: Boolean
- `fallback_used` (optional): Boolean
- `error_message` (optional): Error details

---

## Summary

✅ **Fully Integrated**: OpenAI API with automatic fallback
✅ **Error Handling**: Comprehensive error handling and recovery
✅ **Mock Mode**: Works without API key
✅ **Tracking**: All requests logged to database
✅ **Documentation**: Complete API documentation in Swagger
✅ **Testing**: Test suite included

**The AI integration is production-ready and fully functional!**
