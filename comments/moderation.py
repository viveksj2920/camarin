from google.cloud import language_v1

def moderate_text(content: str) -> tuple[bool, str]:
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(request={'document': document})
    score = response.document_sentiment.score

    # Flag strongly negative sentiment
    if score < -0.5:
        return True, f"Negative sentiment detected (score={score:.2f})"
    return False, ""
