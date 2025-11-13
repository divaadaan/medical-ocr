"""Script to process a sample CMS-1500 form end-to-end."""
import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.connectors.ocr_connector import OCRConnector
from app.connectors.llm_connector import LLMConnector


async def process_form(image_url: str):
    """
    Process a CMS-1500 form through the full pipeline.

    Args:
        image_url: URL or path to the form image
    """
    print("=" * 70)
    print("Medical Form Processing Pipeline")
    print("=" * 70)
    print(f"\nInput: {image_url}\n")

    # Step 1: OCR
    print("Step 1: OCR Text Extraction")
    print("-" * 70)
    ocr = OCRConnector()
    try:
        ocr_text = await ocr.extract_text(image_url)
        print(f"✅ Extracted {len(ocr_text)} characters")
        print("\nFirst 300 characters of OCR output:")
        print(ocr_text[:300])
        print("...\n")
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return

    # Step 2: Field Extraction
    print("\nStep 2: Field Extraction with Kimi K2")
    print("-" * 70)
    llm = LLMConnector()
    try:
        result = await llm.extract_fields(ocr_text, "CMS-1500")
        print("✅ Extraction complete")

        print("\nRaw LLM Response:")
        print(result.get("raw_response", "No response")[:500])
        print("...\n")

        # TODO: When agent is implemented, this will show structured fields
        print("\n⚠️  Note: Structured field extraction not yet implemented")
        print("    Next steps:")
        print("    - Implement LangGraph agent in app/agents/extraction_agent.py")
        print("    - Add CMS-1500 specific field parsing")
        print("    - Integrate confidence scoring")

    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return

    print("\n" + "=" * 70)
    print("Pipeline complete!")
    print("=" * 70)


async def main():
    """Run the sample processing."""
    # Use one of the downloaded sample forms
    samples = {
        "1": "Texas AG Sample",
        "2": "Arkansas DHS Sample",
        "3": "CMS PQRS Sample",
        "4": "Montana Medicaid Sample",
    }

    print("\nAvailable sample forms:")
    for key, name in samples.items():
        print(f"  {key}. {name}")

    choice = input("\nSelect a form (1-4) or enter a URL: ").strip()

    if choice in samples:
        sample_files = {
            "1": "data/samples/sample_texas.pdf",
            "2": "data/samples/sample_arkansas.pdf",
            "3": "data/samples/sample_cms_pqrs.pdf",
            "4": "data/samples/sample_montana.pdf",
        }
        # For local files, would need to convert to base64 or use file upload
        # For now, use the original URLs
        urls = {
            "1": "https://www.texasattorneygeneral.gov/sites/default/files/files/divisions/crime-victims/CMS%201500%20Sample.pdf",
            "2": "https://humanservices.arkansas.gov/wp-content/uploads/SampleCMS-1500.pdf",
            "3": "https://www.cms.gov/Medicare/Quality-Initiatives-Patient-Assessment-Instruments/PQRS/Downloads/2013_PQRS_sampleCMS1500claim_12-19-2012.pdf",
            "4": "https://medicaidprovider.mt.gov/docs/forms/cms1500sample0212bwinstructions.pdf",
        }
        image_url = urls[choice]
    else:
        image_url = choice

    await process_form(image_url)


if __name__ == "__main__":
    asyncio.run(main())
