"""Pydantic models for API requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class OCRRequest(BaseModel):
    """Request model for OCR processing."""

    image_url: Optional[str] = Field(None, description="URL to the image to process")
    use_toon: bool = Field(True, description="Convert OCR output to TOON format")


class OCRResponse(BaseModel):
    """Response model for OCR processing."""

    text: str = Field(..., description="Extracted text from the image")
    format: str = Field("text", description="Output format (text or toon)")
    processing_time_ms: float = Field(..., description="OCR processing time in milliseconds")


class ExtractionRequest(BaseModel):
    """Request model for field extraction."""

    ocr_text: str = Field(..., description="OCR text to extract fields from")
    form_type: str = Field("CMS-1500", description="Type of medical form")


class ExtractionResponse(BaseModel):
    """Response model for field extraction."""

    fields: Dict[str, Any] = Field(..., description="Extracted structured fields")
    reasoning_log: List[Dict[str, str]] = Field(
        default_factory=list, description="Agent reasoning steps"
    )
    confidence_scores: Dict[str, float] = Field(
        default_factory=dict, description="Confidence score per field"
    )
    processing_time_ms: float = Field(..., description="Extraction processing time in milliseconds")


class ProcessFormRequest(BaseModel):
    """Request model for end-to-end form processing."""

    image_url: Optional[str] = Field(None, description="URL to the form image")
    form_type: str = Field("CMS-1500", description="Type of medical form")


class ProcessFormResponse(BaseModel):
    """Response model for end-to-end form processing."""

    form_type: str
    ocr_text: str
    extracted_fields: Dict[str, Any]
    reasoning_log: List[Dict[str, str]]
    confidence_scores: Dict[str, float]
    total_processing_time_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
