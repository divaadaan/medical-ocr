# Medical Document Information Extraction POC

Agentic information extraction pipeline for medical forms using DeepSeek-OCR and Kimi K2 Thinking model.

## Overview

This application processes medical forms (PDF/PNG) and extracts structured information using:
- **OCR**: DeepSeek-OCR via HuggingFace Inference API
- **LLM**: Kimi K2 Thinking via Moonshot AI API
- **Agent Framework**: LangGraph (planned)
- **Data Format**: TOON for efficient token usage
- **API**: FastAPI with Docker deployment

## Project Structure

```
medical-ocr/
├── app/
│   ├── agents/           # LangGraph-based extraction agents (TODO)
│   ├── connectors/       # External service connectors
│   │   ├── ocr_connector.py      # DeepSeek-OCR integration
│   │   └── llm_connector.py      # Kimi K2 integration
│   ├── models/           # Pydantic schemas
│   ├── utils/            # Helper utilities
│   │   ├── file_handler.py       # File upload/conversion
│   │   └── toon_converter.py     # TOON format conversion
│   ├── config.py         # Application configuration
│   ├── routes.py         # API endpoints
│   └── main.py           # FastAPI application
├── data/
│   ├── forms/            # CMS-1500 blank forms
│   └── samples/          # Sample filled forms
├── tests/                # Test suite (TODO)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Setup

### Prerequisites

- Docker and Docker Compose
- HuggingFace API token (for DeepSeek-OCR)
- Moonshot AI API key (for Kimi K2)

### Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
HF_TOKEN=your_huggingface_token_here
MOONSHOT_API_KEY=your_moonshot_api_key_here
```

### Running with Docker

Build and run the application:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Running Locally (Development)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m app.main
```

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### OCR Text Extraction
```
POST /api/v1/ocr/extract
{
  "image_url": "https://example.com/form.png",
  "use_toon": true
}
```

### Field Extraction
```
POST /api/v1/extract/fields
{
  "ocr_text": "extracted text...",
  "form_type": "CMS-1500"
}
```

### Process Form (Upload)
```
POST /api/v1/process/upload
Form Data:
  - file: medical_form.pdf
  - form_type: CMS-1500
```

### Process Form (URL)
```
POST /api/v1/process/url
{
  "image_url": "https://example.com/form.png",
  "form_type": "CMS-1500"
}
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## CMS-1500 Form Dataset

The repository includes sample CMS-1500 forms in `data/samples/`:
- `cms1500_blank.pdf` - Blank form template
- `sample_texas.pdf` - Filled sample from Texas AG
- `sample_arkansas.pdf` - Filled sample from Arkansas DHS
- `sample_cms_pqrs.pdf` - PQRS example from CMS
- `sample_montana.pdf` - Montana Medicaid sample

## Development Status

### Completed
- ✅ FastAPI application structure
- ✅ DeepSeek-OCR connector via HuggingFace
- ✅ Kimi K2 LLM connector via Moonshot AI
- ✅ Docker containerization
- ✅ File upload and processing
- ✅ Basic API endpoints
- ✅ Sample CMS-1500 forms downloaded

### TODO
- ⏳ LangGraph agent implementation for multi-step extraction
- ⏳ TOON format integration for OCR output
- ⏳ Field-specific extraction prompts for CMS-1500
- ⏳ Confidence scoring per field
- ⏳ Reasoning log capture and storage
- ⏳ Multi-page PDF processing
- ⏳ Evaluation pipeline with metrics
- ⏳ Streamlit dashboard for visualization
- ⏳ Ground truth annotation system
- ⏳ Test suite with pytest
- ⏳ Production-ready error handling

## Technologies

- **FastAPI**: Modern Python web framework
- **DeepSeek-OCR**: Advanced OCR model for text extraction
- **Kimi K2 Thinking**: LLM with reasoning capabilities
- **LangGraph**: Agent orchestration framework (planned)
- **TOON**: Efficient data format for LLM input (planned)
- **Docker**: Containerization and deployment
- **Pydantic**: Data validation and settings

## License

See COPYRIGHT file for usage restrictions.

## Next Steps

1. Implement LangGraph agent workflow in `app/agents/extraction_agent.py`
2. Add CMS-1500 specific field extraction logic
3. Integrate TOON format conversion for OCR outputs
4. Build evaluation pipeline and Streamlit dashboard
5. Create test suite with sample forms
