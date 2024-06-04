from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .model import find_similar_problems, get_problem_vector
from .scraping import extract_problem_name


class UrlRequest(BaseModel):
    url: str


app = FastAPI()

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


@app.post("/recommend")
async def recommend(request: UrlRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="No URL provided")

    try:
        problem_name = extract_problem_name(request.url)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error extracting problem name: {e}")

    try:
        similar_problems = find_similar_problems(problem_name)
        vectors = [get_problem_vector(problem['problem_name'])
                   for problem in similar_problems]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error finding similar problems: {e}")

    return {"recommendations": similar_problems, "vectors": vectors}

# Entry point for Vercel
app = app
