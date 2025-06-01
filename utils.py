import re

# Define PII patterns
PII_FIELDS = {
    "full_name": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_number": r"\b\d{10}\b",
}

def mask_pii(text):
    """Mask PII information in the given text."""
    if not text or not isinstance(text, str):
        return text, []  # Return original text if input is empty or malformed

    masked_text = text
    masked_entities = []

    for entity, pattern in PII_FIELDS.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            masked_text = masked_text.replace(match.group(), f"[{entity}]")
            masked_entities.append({
                "position": [match.start(), match.end()],
                "classification": entity,
                "entity": match.group()
            })

    return masked_text, masked_entities