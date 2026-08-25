import os
import re
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


load_dotenv()


def _get_client():
    """
    Helper method to expose credentials and endpoint.
    Used to prevent credentials from being used unless method called
    """
    endpoint = os.environ["AZURE_OCR_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_OCR_KEY"]

    return DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )


def extract_text(image_file) -> str:
    """
    takes an image file and extract the text from it
    Image file should contain  list of ingredients
    """
    client = _get_client()
    image_bytes = image_file.read()

    request = AnalyzeDocumentRequest(
        bytes_source=image_bytes
    )


    poller = client.begin_analyze_document(
        "prebuilt-read",
        request,
    )

    result = poller.result()

    lines = []

    for page in result.pages:
        for line in page.lines:
            lines.append(fix_mixed_fraction(line.content))

    return "\n".join(lines)


def fix_mixed_fraction(line):
    """
    transforms a fraction into a mixed fraction
    21/2 becomes 2 1/2
    """
    pattern = r"^(\s*[•·\-]?\s*)(\d+)(\d)/(\d)(?=\s)"

    match = re.match(pattern, line)

    if not match:
        return line

    prefix = match.group(1)
    whole = match.group(2)
    numerator = int(match.group(3))
    denominator = int(match.group(4))

    if numerator >= denominator:
        return line

    fixed = f"{prefix}{whole} {numerator}/{denominator}"

    return fixed + line[match.end():]