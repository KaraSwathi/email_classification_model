from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
from utils import mask_pii
import traceback
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel  

app = FastAPI(title="Email Classifier API",
    description="Classifies emails and removes sensitive information.",
    version="1.0",
    docs_url="/docs",   #  Explicitly enable /docs
    redoc_url="/redoc", # Ensure /redoc is also available
              
)
class EntityDetails(BaseModel):
    position: list[int]
    classification: str
    entity: str

class EmailRequest(BaseModel):
    input_email_body: str

class EmailResponse(BaseModel):
    input_email_body: str
    list_of_masked_entities: list[EntityDetails]
    masked_email: str
    category_of_the_email: str


@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/classify")
def classify_email(email_request: EmailRequest):
    return {"message": "API route is working"}

# Debugging: Print all available routes
import inspect
print([route.path for route in app.router.routes])


# Load trained models
try:
    vectorizer = load("vectorizer.joblib")
    model = load("nb_email_classifier.joblib")
except Exception as e:
    print(f"Error loading models: {traceback.format_exc()}")

class EmailRequest(BaseModel):
    input_email_body: str

@app.post("/classify", response_model=EmailResponse)
def classify_email(email_request: EmailRequest):
    text = email_request.input_email_body.strip()
    return {"message": "API route is working!"}


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
    masked_entities = [
                {"position": [18, 26], "classification": "full_name", "entity": "John Doe"},
        {"position": [45, 67], "classification": "email", "entity": "johndoe@example.com"}
    ]

    masked_email = email_request.input_email_body.replace("John Doe", "[full_name]").replace("johndoe@example.com", "[email]")

    # Ensure proper JSON serialization
    response_data = {
        "input_email_body": email_request.input_email_body,
        "list_of_masked_entities": masked_entities,
        "masked_email": masked_text,
        "category_of_the_email": category
    }
    print(f"DEBUG - Returning JSON Response: {response_data}")  # Debugging step
    return JSONResponse(content=response_data)  # Ensure JSON format
