from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .model import find_similar_problems, get_problem_vector
from .scraping import extract_problem_name
import logging


class UrlRequest(BaseModel):
    url: str


app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)


@app.post("/recommend")
async def recommend(request: UrlRequest):
    logging.info("Received request: %s", request.json())

    if not request.url:
        raise HTTPException(status_code=400, detail="No URL provided")

    try:
        problem_name = extract_problem_name(request.url)
        logging.info("Extracted problem name: %s", problem_name)
    except Exception as e:
        logging.error("Error extracting problem name: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Error extracting problem name: {e}")

    try:
        similar_problems = find_similar_problems(problem_name)
        vectors = [get_problem_vector(problem['problem_name'])
                   for problem in similar_problems]
        logging.info("Found similar problems: %s", similar_problems)
    except Exception as e:
        logging.error("Error finding similar problems: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Error finding similar problems: {e}")

    return {"recommendations": similar_problems, "vectors": vectors}
