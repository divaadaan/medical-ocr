# Architecture Overview

## System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Medical Form Input                            │
│                      (PDF, PNG, JPG, URL)                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                             │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  POST /api/v1/process/upload  or  /process/url                │ │
│  └───────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    File Handler (app/utils)                          │
│  • PDF → Images conversion                                          │
│  • Image validation                                                 │
│  • Base64 encoding                                                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│               OCR Connector (app/connectors/ocr_connector.py)        │
│                                                                      │
│  DeepSeek-OCR via HuggingFace Inference                             │
│  • Image → Text extraction                                          │
│  • Preserves layout/structure                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼ OCR Text
┌─────────────────────────────────────────────────────────────────────┐
│           TOON Converter (app/utils/toon_converter.py)               │
│  • Convert to efficient format (TODO)                               │
│  • Reduce token count by 30-60%                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼ TOON Formatted Text
┌─────────────────────────────────────────────────────────────────────┐
│        Extraction Agent (app/agents/extraction_agent.py)             │
│                                                                      │
│  LangGraph Workflow (TODO):                                         │
│  ┌─────────────────┐      ┌──────────────────┐                     │
│  │ Validate Form   │─────▶│ Identify Fields  │                     │
│  └─────────────────┘      └──────────────────┘                     │
│           │                        │                                │
│           ▼                        ▼                                │
│  ┌─────────────────┐      ┌──────────────────┐                     │
│  │ Extract Values  │─────▶│ Validate X-Field │                     │
│  └─────────────────┘      └──────────────────┘                     │
│           │                        │                                │
│           ▼                        ▼                                │
│  ┌─────────────────────────────────┐                               │
│  │    Score Confidence             │                               │
│  └─────────────────────────────────┘                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│         LLM Connector (app/connectors/llm_connector.py)              │
│                                                                      │
│  Kimi K2 Thinking via Moonshot AI                                   │
│  • Field extraction with reasoning                                  │
│  • 200-300 sequential tool calls                                    │
│  • Transparent thinking process                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   Structured Output (JSON)                           │
│                                                                      │
│  • extracted_fields: {...}                                          │
│  • reasoning_log: [...]                                             │
│  • confidence_scores: {...}                                         │
│  • processing_time_ms: 1234                                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### FastAPI Application (`app/main.py`)
- HTTP server and request handling
- CORS middleware
- API documentation (Swagger/ReDoc)
- Route orchestration

### Routes (`app/routes.py`)
- Endpoint definitions
- Request/response validation
- Error handling
- Background task management

### OCR Connector (`app/connectors/ocr_connector.py`)
- Interface to DeepSeek-OCR via HuggingFace
- Image-to-text conversion
- Timeout and error handling
- Batch processing capability

### LLM Connector (`app/connectors/llm_connector.py`)
- Interface to Kimi K2 via Moonshot AI
- Field extraction prompts
- Chat completion interface
- Response parsing (TODO: structured)

### Extraction Agent (`app/agents/extraction_agent.py`)
- LangGraph state machine (TODO)
- Multi-step extraction workflow
- Reasoning trace capture
- Confidence scoring

### File Handler (`app/utils/file_handler.py`)
- File upload management
- PDF to image conversion
- Image validation
- Base64 encoding
- Cleanup operations

### TOON Converter (`app/utils/toon_converter.py`)
- OCR output formatting
- Token optimization (TODO)
- Structured data conversion

### Configuration (`app/config.py`)
- Environment variable management
- Settings validation
- Default configurations

### Models (`app/models/schemas.py`)
- Request/response schemas
- Data validation
- Type hints

## Data Flow Example

### Processing a CMS-1500 Form

1. **Client Request**
   ```bash
   POST /api/v1/process/upload
   Content-Type: multipart/form-data
   file: cms1500_filled.pdf
   ```

2. **File Handler**
   - Saves upload to `data/uploads/`
   - Converts PDF → PNG (page 1)
   - Validates image format
   - Encodes to base64

3. **OCR Connector**
   ```python
   image_url = "data:image/png;base64,iVBORw0KG..."
   ocr_text = await ocr_connector.extract_text(image_url)
   ```
   Returns raw OCR text preserving layout

4. **TOON Converter** (Future)
   ```python
   toon_text = toon_converter.convert_to_toon(ocr_text)
   ```
   Reduces token count for LLM

5. **Extraction Agent** (Future)
   - Validates form is CMS-1500
   - Identifies present fields
   - Extracts values field-by-field
   - Cross-validates related fields
   - Scores confidence per field

6. **LLM Connector**
   ```python
   result = await llm_connector.extract_fields(toon_text, "CMS-1500")
   ```
   Returns structured fields with reasoning

7. **Response**
   ```json
   {
     "form_type": "CMS-1500",
     "ocr_text": "...",
     "extracted_fields": {
       "patient_name": "John Doe",
       "dob": "1980-05-15",
       ...
     },
     "reasoning_log": [...],
     "confidence_scores": {...},
     "total_processing_time_ms": 3421
   }
   ```

## External Dependencies

### APIs
- **HuggingFace Inference**: DeepSeek-OCR model hosting
  - Endpoint: `https://router.huggingface.co/v1`
  - Auth: Bearer token (HF_TOKEN)

- **Moonshot AI**: Kimi K2 model API
  - Endpoint: `https://api.moonshot.cn/v1`
  - Auth: API key (MOONSHOT_API_KEY)
  - OpenAI-compatible interface

### Libraries
- **FastAPI**: Web framework
- **OpenAI SDK**: API client for both OCR and LLM
- **LangGraph**: Agent orchestration (planned)
- **python-toon**: Data format conversion (planned)
- **pdf2image**: PDF processing
- **Pillow**: Image handling

## Deployment

### Docker Container
```
┌────────────────────────────────────┐
│  Docker Container                   │
│  ┌──────────────────────────────┐  │
│  │  Python 3.12.9               │  │
│  │  + FastAPI App               │  │
│  │  + Dependencies              │  │
│  │  + poppler-utils             │  │
│  └──────────────────────────────┘  │
│                                     │
│  Volumes:                           │
│  • ./data → /app/data               │
│  • ./logs → /app/logs               │
│  • ./app → /app/app (dev)           │
│                                     │
│  Port: 8000                         │
└────────────────────────────────────┘
```

### Docker Compose
- Single service architecture
- Environment variable injection
- Volume mounts for persistence
- Network isolation
- Automatic restart

## Security Considerations

### Current Implementation
- API keys in environment variables
- CORS enabled for all origins (development)
- No authentication on endpoints
- File uploads cleaned automatically

### Production Recommendations
- Restrict CORS origins
- Add API key authentication
- Implement rate limiting
- Add request size limits
- Sanitize file uploads
- Use HTTPS/TLS
- Implement audit logging
- Secure API key storage (secrets manager)

## Performance Characteristics

### OCR Processing
- Single image: ~5-15 seconds
- Depends on: image size, network latency, API queue
- Timeout: 300 seconds (configurable)

### LLM Extraction
- Field extraction: ~3-10 seconds
- Depends on: text length, field complexity, model load
- Timeout: default (configurable)

### File Operations
- PDF conversion: ~1-2 seconds per page
- Image validation: <1 second
- Base64 encoding: <1 second

### Bottlenecks
- External API calls (network I/O)
- PDF processing for multi-page documents
- Sequential batch processing

### Future Optimizations
- Parallel batch processing
- Response caching
- Image preprocessing/optimization
- Streaming responses for long operations

## Error Handling

### Levels
1. **Input Validation**: Pydantic models
2. **Business Logic**: Try/catch in connectors
3. **HTTP Errors**: FastAPI HTTPException
4. **Background Tasks**: Logged, don't block response

### Error Responses
```json
{
  "detail": "OCR processing failed: timeout"
}
```

HTTP status codes:
- 200: Success
- 400: Bad request (invalid input)
- 500: Server error (API failure, processing error)
