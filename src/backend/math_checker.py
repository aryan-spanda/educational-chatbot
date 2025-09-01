from openai import OpenAI
from google.genai import errors

class check_math_expression():

    def __init__(self, model,base_url):
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(base_url=self.base_url)

    def math_function(self,user_question):
        
        prompt = """
You are a question classifier. Your task is to determine if a user's question is mathematical or theory-based.

A question should be classified as mathematical/theory-based (TRUE) if it involves:
- Mathematical calculations, equations, or formulas
- Mathematical concepts (algebra, calculus, geometry, statistics, etc.)
- Theoretical physics, chemistry, or other sciences
- Abstract theoretical concepts or frameworks
- Logical reasoning or proofs
- Scientific theories or principles

A question should be classified as non-mathematical/theory-based (FALSE) if it involves:
- Practical how-to instructions
- Personal advice or opinions
- Current events or news
- Creative writing or storytelling
- General knowledge facts (unless mathematical/theoretical)
- Product recommendations
- Entertainment or casual conversation

Instructions:
1. Analyze the user's question carefully
2. Determine if it falls into the mathematical/theory-based category
3. Respond with only "TRUE" or "FALSE" (nothing else)


Response:

"""
        try:
            response = self.client.chat.completions.create(
                model= self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_question}
                ]
        )
        except Exception as e:
            print(f"API Error Details: {str(e)}")
            return f"Error generating response: {e}"
        return response.choices[0].message.content