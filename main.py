from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
import uvicorn
from utils import mask_pii
import traceback
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# Load trained models
try:
    vectorizer = load("vectorizer.joblib")
    model = load("nb_email_classifier.joblib")
except Exception as e:
    print(f"Error loading models: {traceback.format_exc()}")

class EmailRequest(BaseModel):
    input_email_body: str

@app.post("/classify")
def classify_email(email_request: EmailRequest):
    text = email_request.input_email_body.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Email body cannot be empty.")

    try:
        masked_text, masked_entities = mask_pii(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PII Masking Error: {str(e)}")

    try:
        X_test = vectorizer.transform([masked_text])
        category = model.predict(X_test)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")

    # Ensure proper JSON serialization
    response_data = {
        "input_email_body": text,
        "list_of_masked_entities": masked_entities,
        "masked_email": masked_text,
        "category_of_the_email": category
    }
    print(f"DEBUG - Returning JSON Response: {response_data}")  # Debugging step
    return JSONResponse(content=response_data)  # Ensure JSON format

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
