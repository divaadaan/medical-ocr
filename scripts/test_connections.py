"""Test script to verify OCR and LLM API connections."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.connectors.ocr_connector import OCRConnector
from app.connectors.llm_connector import LLMConnector


async def test_ocr():
    """Test DeepSeek-OCR connection."""
    print("Testing DeepSeek-OCR connection...")
    try:
        connector = OCRConnector()
        # Use a sample CMS-1500 form
        sample_url = "https://www.texasattorneygeneral.gov/sites/default/files/files/divisions/crime-victims/CMS%201500%20Sample.pdf"

        print(f"Extracting text from: {sample_url}")
        text = await connector.extract_text(sample_url)

        print("✅ OCR connection successful!")
        print(f"Extracted text length: {len(text)} characters")
        print("\nFirst 500 characters:")
        print(text[:500])
        return True
    except Exception as e:
        print(f"❌ OCR connection failed: {e}")
        return False


async def test_llm():
    """Test Kimi K2 connection."""
    print("\nTesting Kimi K2 connection...")
    try:
        connector = LLMConnector()

        messages = [
            {"role": "user", "content": "Hello! Can you confirm you're working? Just say 'Yes, I'm working.'"}
        ]

        response = await connector.chat(messages)

        print("✅ LLM connection successful!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"❌ LLM connection failed: {e}")
        return False


async def main():
    """Run all connection tests."""
    print("=" * 60)
    print("Medical OCR API - Connection Test")
    print("=" * 60)

    ocr_ok = await test_ocr()
    llm_ok = await test_llm()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  OCR: {'✅ Working' if ocr_ok else '❌ Failed'}")
    print(f"  LLM: {'✅ Working' if llm_ok else '❌ Failed'}")
    print("=" * 60)

    if ocr_ok and llm_ok:
        print("\n🎉 All connections working! Ready to process forms.")
        return 0
    else:
        print("\n⚠️  Some connections failed. Check your API keys in .env")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
