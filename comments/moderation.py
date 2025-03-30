from google.cloud import language_v1
from google.oauth2 import service_account
import os

def moderate_text(content: str) -> tuple[bool, str]:
    credentials = service_account.Credentials.from_service_account_file(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)
    client = language_v1.LanguageServiceClient(credentials=credentials)

    document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(request={'document': document})
    score = response.document_sentiment.score

    # Flag strongly negative sentiment
    if score < -0.5:
        return True, f"Negative sentiment detected (score={score:.2f})"
    return False, ""
