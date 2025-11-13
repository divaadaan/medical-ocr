"""OCR connector for DeepSeek-OCR via HuggingFace Inference API."""
import os
from typing import Optional
from openai import OpenAI
from app.config import settings


class OCRConnector:
    """Connector for DeepSeek-OCR via HuggingFace router."""

    def __init__(self):
        """Initialize the OCR connector with HuggingFace configuration."""
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=settings.hf_token,
        )
        self.model = settings.ocr_model
        self.timeout = settings.ocr_timeout

    async def extract_text(
        self,
        image_url: str,
        prompt: Optional[str] = None
    ) -> str:
        """
        Extract text from an image using DeepSeek-OCR.

        Args:
            image_url: URL or local path to the image
            prompt: Optional custom prompt for OCR extraction

        Returns:
            Extracted text from the image

        Raises:
            Exception: If OCR processing fails
        """
        if prompt is None:
            prompt = "Extract all text from this medical form. Preserve the structure and layout."

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url
                                }
                            }
                        ]
                    }
                ],
                timeout=self.timeout,
            )

            return completion.choices[0].message.content

        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")

    async def extract_text_batch(
        self,
        image_urls: list[str],
        prompt: Optional[str] = None
    ) -> list[str]:
        """
        Extract text from multiple images.

        Args:
            image_urls: List of image URLs or local paths
            prompt: Optional custom prompt for OCR extraction

        Returns:
            List of extracted texts

        Note:
            Currently processes images sequentially.
            TODO: Implement parallel processing with rate limiting
        """
        results = []
        for image_url in image_urls:
            text = await self.extract_text(image_url, prompt)
            results.append(text)
        return results
