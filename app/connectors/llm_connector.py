"""LLM connector for Kimi K2 via Moonshot AI API."""
from typing import Optional, List, Dict, Any
from openai import OpenAI
from app.config import settings


class LLMConnector:
    """Connector for Kimi K2 via Moonshot AI OpenAI-compatible API."""

    def __init__(self):
        """Initialize the LLM connector with Moonshot AI configuration."""
        self.client = OpenAI(
            base_url=settings.moonshot_api_base,
            api_key=settings.moonshot_api_key,
        )
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens

    async def extract_fields(
        self,
        ocr_text: str,
        form_type: str = "CMS-1500",
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract structured fields from OCR text using Kimi K2.

        Args:
            ocr_text: Text extracted from the medical form
            form_type: Type of medical form (e.g., CMS-1500)
            system_prompt: Optional custom system prompt

        Returns:
            Dictionary containing extracted fields and metadata

        Note:
            TODO: Integrate with LangGraph agent for multi-step extraction
            TODO: Add field-specific validation and error handling
            TODO: Implement confidence scoring per field
        """
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt(form_type)

        user_prompt = self._build_extraction_prompt(ocr_text, form_type)

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            response_text = completion.choices[0].message.content

            # TODO: Parse response into structured format
            # TODO: Extract reasoning steps from Kimi K2 thinking output
            # TODO: Calculate confidence scores

            return {
                "raw_response": response_text,
                "fields": {},  # Placeholder for parsed fields
                "reasoning": [],  # Placeholder for reasoning steps
                "confidence_scores": {}  # Placeholder for confidence
            }

        except Exception as e:
            raise Exception(f"Field extraction failed: {str(e)}")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generic chat completion with Kimi K2.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Optional override for temperature
            max_tokens: Optional override for max tokens

        Returns:
            Generated response text
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )

            return completion.choices[0].message.content

        except Exception as e:
            raise Exception(f"Chat completion failed: {str(e)}")

    def _get_default_system_prompt(self, form_type: str) -> str:
        """Generate default system prompt for form extraction."""
        return f"""You are an expert medical document information extraction assistant.
Your task is to extract structured information from {form_type} forms.

Guidelines:
- Extract all fields accurately from the provided text
- Preserve exact values as they appear in the form
- Use null/empty for missing fields
- For ambiguous data, provide your best interpretation with a confidence note
- Return structured JSON format with clear field names

Think step-by-step about each field extraction."""

    def _build_extraction_prompt(self, ocr_text: str, form_type: str) -> str:
        """Build the user prompt for field extraction."""
        # TODO: Customize prompt based on form_type
        # TODO: Add examples of expected output format
        # TODO: Include TOON format handling if applicable

        return f"""Extract all fields from this {form_type} form:

{ocr_text}

Return the extracted data as a structured JSON object with the following information:
- Patient demographics (name, DOB, gender, address)
- Insurance information (policy numbers, group numbers)
- Diagnosis codes (ICD-10)
- Procedure codes (HCPCS)
- Provider information (NPI, taxonomy, address)
- Service dates and charges
- Authorization numbers

For each field, provide the extracted value. If a field is not present or unclear, use null."""
