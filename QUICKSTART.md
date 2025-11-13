# Quick Start Guide

## 1. Setup Environment

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- `HF_TOKEN`: Your HuggingFace API token (get from https://huggingface.co/settings/tokens)
- `MOONSHOT_API_KEY`: Your Moonshot AI API key (get from https://platform.moonshot.ai/)

## 2. Run with Docker (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The API will be available at http://localhost:8000

## 3. Test the API

Open your browser and go to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

## 4. Process a Sample Form

### Option A: Using the API

```bash
# OCR text extraction
curl -X POST "http://localhost:8000/api/v1/ocr/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://www.texasattorneygeneral.gov/sites/default/files/files/divisions/crime-victims/CMS%201500%20Sample.pdf"
  }'

# End-to-end processing
curl -X POST "http://localhost:8000/api/v1/process/url" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://www.texasattorneygeneral.gov/sites/default/files/files/divisions/crime-victims/CMS%201500%20Sample.pdf",
    "form_type": "CMS-1500"
  }'
```

### Option B: Using the Test Script

```bash
# Test API connections
python scripts/test_connections.py

# Process a sample form
python scripts/process_sample_form.py
```

## 5. Upload Your Own Form

Use the upload endpoint to process your own CMS-1500 forms:

```bash
curl -X POST "http://localhost:8000/api/v1/process/upload" \
  -F "file=@/path/to/your/form.pdf" \
  -F "form_type=CMS-1500"
```

## Development Mode

To run without Docker (for development):

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python -m app.main
```

## Next Steps

1. **Implement LangGraph Agent**: The extraction logic in `app/agents/extraction_agent.py` needs to be completed to enable multi-step field extraction with reasoning traces.

2. **Customize Field Extraction**: Add CMS-1500 specific field definitions and validation rules in `app/connectors/llm_connector.py`.

3. **Add TOON Format**: Integrate the python-toon library in `app/utils/toon_converter.py` for efficient OCR output formatting.

4. **Build Evaluation Pipeline**: Create ground truth annotations and implement metrics calculation.

5. **Create Streamlit Dashboard**: Build visualization dashboard for evaluation results and reasoning logs.

## Troubleshooting

**Q: Connection refused or timeout errors?**
- Verify your API keys are correct in `.env`
- Check you have internet connectivity
- Ensure HuggingFace and Moonshot AI services are accessible

**Q: PDF processing fails?**
- Make sure poppler-utils is installed (included in Docker image)
- For local development on Windows, install poppler separately

**Q: Import errors?**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check you're in the correct directory and virtual environment

## Support

For issues and questions, refer to:
- README.md for detailed documentation
- API docs at http://localhost:8000/docs
- Specifications in the project root
