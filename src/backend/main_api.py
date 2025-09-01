# main_api.py

import os
import json
import uvicorn
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import your RAG toolkit components
from spanda_rag_toolkit import (
    Spanda_DecomposeQuestion,
    Spanda_QuestionFilter,
    Spanda_Decompose_Reranker,
    Spanda_Chunk_Summarizer,
    Spanda_Final_Query
)
from chunk_extractor import ChunkExtraction 
from math_checker import check_math_expression

# --- Existing Setup (from your file) ---
# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path=dotenv_path, override=True)

# Get environment variables
model = os.getenv("model")
base_url = os.getenv("base_url")
cross_encoder_model = os.getenv("cross_encoder_model")

# --- FastAPI Application Setup ---

# Create a FastAPI app instance
app = FastAPI(
    title="Spanda RAG API",
    description="An API for processing questions with a RAG pipeline - GitOps Demo.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"], # all
    allow_headers = ["*"]
)

# Define a Pydantic model for the request body.
# This ensures that any incoming request has a "question" field which is a string.
class QuestionRequest(BaseModel):
    question: str

# --- Helper Function (from your file) ---
def clean_json_response(response):
    """Clean malformed JSON responses from LLM."""
    if isinstance(response, (list, dict)):
        return response
    if isinstance(response, str):
        try:
            cleaned = response.strip()
            if '[' in cleaned:
                start = cleaned.find('[')
                end = cleaned.rfind(']') + 1
                cleaned = cleaned[start:end]
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("Warning: Could not parse JSON, using raw response")
            return response
    return response

# --- Core RAG Logic Function ---
def run_rag_pipeline(user_question: str):
    """
    Executes the full RAG pipeline for a given user question.
    """
    try:
        print(f"Processing question: '{user_question}'")
        print("============")
        
        try:
            math_checker_instance = check_math_expression(model, base_url)
            response = math_checker_instance.math_function(user_question)
            is_math = response.strip().upper()

        except Exception as e:
            print(f"Math Checker Error: {e}")
            return {"error": f"Math Checker Error: {e}"}
        

        if is_math == "TRUE":
            print("Detected a mathematical/theoretical question.")
            print("Solving question...")
            summarized_chunks_replacemet = [
                {
                    "question": user_question,
                    "search_results": ["No external context needed for this mathematical/theoretical question."]
                }
            ]

            try:
                print("Creating final LLM caller...")
                llm_caller = Spanda_Final_Query(model=model, base_url=base_url)
                print("Calling caller_function...")
                final_answer = llm_caller.caller_function(user_question,summarized_chunks_replacemet)
                print("Final answer generated successfully")
            except Exception as e:
                print(f"Error in final LLM call: {e}")
                return {"error": f"Error in final LLM call: {e}"}
            return {
                "filtered_questions": [],
                "summarized_chunks": "",
                "answer": final_answer
            }
        
        else:

            print("Detected a theoretical question.")
            # Step 1: Decompose Question
            print("Step 1: Decomposing question...")
            decomposer = Spanda_DecomposeQuestion(model=model, base_url=base_url)
            sub_questions = decomposer.decompose_function(user_question)

            # Step 2: Filter Sub-questions
            print("Step 2: Filtering sub-questions...")
            question_filter = Spanda_QuestionFilter(model=model, base_url=base_url)
            raw_filtered_questions = question_filter.filter_subquestions_function(user_question, sub_questions)
            filtered_questions = clean_json_response(raw_filtered_questions)
            print(f"Filtered sub-questions: {filtered_questions}")

            # Step 3: Extract Chunks
            print("Step 3: Extracting chunks...")
            chunk_extractor = ChunkExtraction()
            filtered_questions_chunks = chunk_extractor.chunker_function(filtered_questions)

            # Step 4: Re-rank
            print("Step 4: Re-ranking chunks...")
            reranker = Spanda_Decompose_Reranker(cross_encoder_model)
            final_ranked_list = reranker.reranker_function(filtered_questions_chunks)

            # Step 5: Summarize Chunks
            print("Step 5: Summarizing chunks...")
            summarizer = Spanda_Chunk_Summarizer(base_url=base_url, model=model)
            summarized_chunks = summarizer.summarize_chunks(final_ranked_list)

            # Step 6: Generate Final Answer
            print("Step 6: Generating final answer...")
            llm_caller = Spanda_Final_Query(model=model, base_url=base_url)
            final_answer = llm_caller.caller_function(user_question,summarized_chunks)

            print("Pipeline completed successfully.")
            return {
                "filtered_questions": filtered_questions,
                "summarized_chunks": summarized_chunks,
                "answer": final_answer
            }

    except json.JSONDecodeError as e:
        error_message = f"JSON parsing error: {e}"
        print(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred in the pipeline: {e}"
        print(error_message)
        return {"error": error_message}

# --- API Endpoint Definition ---
@app.get("/")
async def root():
    """
    Root endpoint that returns API information and version.
    """
    return {
        "message": "Spanda RAG API - GitOps Demo",
        "version": "1.1.0",
        "status": "running",
        "demo": "CI/CD Pipeline Integration"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy", "version": "1.1.0"}

@app.post("/ask/")
async def ask_question(request: QuestionRequest):
    """
    This endpoint receives a question, processes it through the RAG pipeline,
    and returns the final answer.
    """
    print(f"Received request with question: {request.question}")
    response_data = run_rag_pipeline(request.question)
    return response_data

# --- Server Execution ---
# This block allows you to run the server directly from the command line
if __name__ == "__main__":
    # Use uvicorn to run the app. It will be available at http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
