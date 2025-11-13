"""File handling utilities for medical forms."""
import os
import base64
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from PIL import Image
from pdf2image import convert_from_path
from app.config import settings


class FileHandler:
    """Handle file uploads and conversions."""

    def __init__(self, upload_dir: str = "data/uploads"):
        """Initialize file handler with upload directory."""
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> Path:
        """
        Save uploaded file to disk.

        Args:
            file: Uploaded file from FastAPI

        Returns:
            Path to saved file

        Raises:
            ValueError: If file extension is not allowed
        """
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.allowed_extensions:
            raise ValueError(f"File type .{file_ext} not allowed")

        file_path = self.upload_dir / file.filename
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        return file_path

    def pdf_to_images(self, pdf_path: Path) -> list[Path]:
        """
        Convert PDF to images.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of paths to converted images

        Note:
            Requires poppler installed for pdf2image
            TODO: Add error handling for missing poppler
        """
        images = convert_from_path(pdf_path)
        image_paths = []

        for i, image in enumerate(images):
            image_path = pdf_path.parent / f"{pdf_path.stem}_page_{i+1}.png"
            image.save(image_path, "PNG")
            image_paths.append(image_path)

        return image_paths

    def image_to_base64(self, image_path: Path) -> str:
        """
        Convert image to base64 string for API transmission.

        Args:
            image_path: Path to image file

        Returns:
            Base64 encoded image string with data URI prefix
        """
        with open(image_path, "rb") as f:
            image_data = f.read()

        base64_data = base64.b64encode(image_data).decode("utf-8")

        # Determine MIME type
        ext = image_path.suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
        }
        mime_type = mime_types.get(ext, "image/png")

        return f"data:{mime_type};base64,{base64_data}"

    def validate_image(self, image_path: Path) -> bool:
        """
        Validate that file is a valid image.

        Args:
            image_path: Path to image file

        Returns:
            True if valid image, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def cleanup_file(self, file_path: Path) -> None:
        """
        Delete file from disk.

        Args:
            file_path: Path to file to delete
        """
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            # Log error but don't raise to avoid breaking cleanup chains
            print(f"Error deleting file {file_path}: {e}")
