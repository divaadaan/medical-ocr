"""FastAPI route definitions."""
import time
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.models import (
    OCRRequest,
    OCRResponse,
    ExtractionRequest,
    ExtractionResponse,
    ProcessFormRequest,
    ProcessFormResponse,
    HealthResponse,
)
from app.connectors.ocr_connector import OCRConnector
from app.connectors.llm_connector import LLMConnector
from app.utils.file_handler import FileHandler
from app.utils.toon_converter import TOONConverter


router = APIRouter()
file_handler = FileHandler()
ocr_connector = OCRConnector()
llm_connector = LLMConnector()
toon_converter = TOONConverter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.1.0")


@router.post("/ocr/extract", response_model=OCRResponse)
async def extract_text(request: OCRRequest):
    """
    Extract text from an image using DeepSeek-OCR.

    Args:
        request: OCR request with image URL

    Returns:
        Extracted text and metadata
    """
    if not request.image_url:
        raise HTTPException(status_code=400, detail="image_url is required")

    start_time = time.time()

    try:
        text = await ocr_connector.extract_text(request.image_url)

        if request.use_toon:
            # Convert extracted text to TOON format for efficient downstream processing
            # TODO: Implement structured parsing of OCR output before TOON conversion
            formatted_text = text  # Placeholder
            output_format = "toon"
        else:
            formatted_text = text
            output_format = "text"

        processing_time = (time.time() - start_time) * 1000

        return OCRResponse(
            text=formatted_text,
            format=output_format,
            processing_time_ms=processing_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/fields", response_model=ExtractionResponse)
async def extract_fields(request: ExtractionRequest):
    """
    Extract structured fields from OCR text using Kimi K2.

    Args:
        request: Extraction request with OCR text

    Returns:
        Extracted fields with reasoning logs

    Note:
        TODO: Integrate LangGraph agent for multi-step extraction workflow
        TODO: Add checkpointing and error recovery
        TODO: Implement confidence scoring per field
    """
    start_time = time.time()

    try:
        # Placeholder for LangGraph agent integration
        # The agent will orchestrate:
        # 1. Field identification
        # 2. Value extraction with validation
        # 3. Cross-field consistency checks
        # 4. Confidence scoring
        # All with full reasoning trace capture

        result = await llm_connector.extract_fields(
            request.ocr_text,
            request.form_type
        )

        processing_time = (time.time() - start_time) * 1000

        return ExtractionResponse(
            fields=result.get("fields", {}),
            reasoning_log=result.get("reasoning", []),
            confidence_scores=result.get("confidence_scores", {}),
            processing_time_ms=processing_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process/upload")
async def process_uploaded_form(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    form_type: str = "CMS-1500"
):
    """
    Process an uploaded medical form (end-to-end).

    Handles PDF or image upload, performs OCR, and extracts fields.

    Args:
        file: Uploaded file (PDF or image)
        form_type: Type of medical form

    Returns:
        Complete processing results
    """
    start_time = time.time()

    try:
        # Save uploaded file
        file_path = await file_handler.save_upload(file)

        # Convert PDF to images if needed
        if file_path.suffix.lower() == ".pdf":
            image_paths = file_handler.pdf_to_images(file_path)
            image_path = image_paths[0]  # Process first page for now
            # TODO: Handle multi-page PDFs
        else:
            image_path = file_path

        # Validate image
        if not file_handler.validate_image(image_path):
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Convert to base64 for OCR API
        image_data = file_handler.image_to_base64(image_path)

        # Extract text via OCR
        ocr_text = await ocr_connector.extract_text(image_data)

        # Extract fields via LLM
        # TODO: Replace with LangGraph agent workflow
        extraction_result = await llm_connector.extract_fields(ocr_text, form_type)

        total_time = (time.time() - start_time) * 1000

        # Schedule cleanup
        background_tasks.add_task(file_handler.cleanup_file, file_path)
        if image_path != file_path:
            background_tasks.add_task(file_handler.cleanup_file, image_path)

        return ProcessFormResponse(
            form_type=form_type,
            ocr_text=ocr_text,
            extracted_fields=extraction_result.get("fields", {}),
            reasoning_log=extraction_result.get("reasoning", []),
            confidence_scores=extraction_result.get("confidence_scores", {}),
            total_processing_time_ms=total_time
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process/url", response_model=ProcessFormResponse)
async def process_form_url(request: ProcessFormRequest):
    """
    Process a medical form from a URL (end-to-end).

    Args:
        request: Processing request with image URL

    Returns:
        Complete processing results
    """
    if not request.image_url:
        raise HTTPException(status_code=400, detail="image_url is required")

    start_time = time.time()

    try:
        # Extract text via OCR
        ocr_text = await ocr_connector.extract_text(request.image_url)

        # Extract fields via LLM
        # TODO: Replace with LangGraph agent workflow
        extraction_result = await llm_connector.extract_fields(
            ocr_text,
            request.form_type
        )

        total_time = (time.time() - start_time) * 1000

        return ProcessFormResponse(
            form_type=request.form_type,
            ocr_text=ocr_text,
            extracted_fields=extraction_result.get("fields", {}),
            reasoning_log=extraction_result.get("reasoning", []),
            confidence_scores=extraction_result.get("confidence_scores", {}),
            total_processing_time_ms=total_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
