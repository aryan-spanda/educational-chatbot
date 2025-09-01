import os
import json
from dotenv import load_dotenv, find_dotenv

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path=dotenv_path, override=True)


# Get environment variables
model = os.getenv("model")
base_url = os.getenv("base_url")
cross_encoder_model = os.getenv("cross_encoder_model")

def clean_json_response(response):
    """Clean malformed JSON responses from LLM."""
    if isinstance(response, (list, dict)):
        return response
    
    if isinstance(response, str):
        try:
            # Find JSON boundaries
            cleaned = response.strip()
            if '[' in cleaned:
                start = cleaned.find('[')
                end = cleaned.rfind(']') + 1
                cleaned = cleaned[start:end]
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the original response
            print(f" Warning: Could not parse JSON, using raw response")
            return response
    
    return response

def main():
    # Import components
    from spanda_rag_toolkit import (
        Spanda_DecomposeQuestion,
        Spanda_QuestionFilter,
        Spanda_Decompose_Reranker,
        Spanda_Chunk_Summarizer, 
        Spanda_Final_Query
    )
    
    from chunk_extractor import ChunkExtraction  # Local file import
    # Removed: from chunk_summarizer import chunk_summarizer
    
    print(" Starting Spanda RAG Toolkit Pipeline")
    print("============")

    
    user_question = "Explain Planck's Quantum Hypothesis."
    print(f" Processing question: '{user_question}'")
    print("============")
    
    try:
        # Step 1: Decompose Question
        print(" Step 1: Decomposing question into sub-questions...")
        decomposer = Spanda_DecomposeQuestion(model=model, base_url=base_url)
        sub_questions = decomposer.decompose_function(user_question)
        
        # Step 2: Filter Sub-questions
        print(" Step 2: Filtering relevant sub-questions...")
        question_filter = Spanda_QuestionFilter(model=model, base_url=base_url)
        raw_filtered_questions = question_filter.filter_subquestions_function(user_question, sub_questions)
        
        # Clean the JSON response to handle malformed output
        filtered_questions = clean_json_response(raw_filtered_questions)
        print("Filtered sub-questions:")
        print(filtered_questions)
        
        # Step 3: Extract Chunks
        print(" Step 3: Extracting 5 chunks per sub-question...")
        chunk_extractor = ChunkExtraction()
        filtered_questions_chunks = chunk_extractor.chunker_function(filtered_questions)
        
        # Step 4: Re-rank
        print(" Step 4: Re-ranking chunks...")
        reranker = Spanda_Decompose_Reranker(cross_encoder_model)
        final_ranked_list = reranker.reranker_function(filtered_questions_chunks)
        
        # Step 5: Summarize Chunks 
        print(" Step 5: Summarizing chunks...")
        summarizer = Spanda_Chunk_Summarizer(base_url=base_url, model=model)  
        summarized_chunks = summarizer.summarize_chunks(final_ranked_list)
        
        # Step 6: Generate Final Answer 
        print(" Step 6: Generating final answer...")
        llm_caller = Spanda_Final_Query(model=model, base_url=base_url)
        final_answers = llm_caller.caller_function(summarized_chunks)
        
        print("\n" + "="*50)
        print("FINAL ANSWER:")
        print("="*50)
        print(final_answers)
        
    except json.JSONDecodeError as e:
        print(f" JSON parsing error: {e}")
        print("The LLM response contains malformed JSON. Check your filter_subquestions_function output.")
    except Exception as e:
        print(f" Pipeline failed: {e}")

if __name__ == "__main__":
    main()
