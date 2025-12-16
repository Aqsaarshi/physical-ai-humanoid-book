import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import google.generativeai as genai
from typing import List, Dict, Any
from ..config import settings


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using the Gemini model
        """
        import logging
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API error in generate_response: {str(e)}")
            raise Exception(f"Error generating response from Gemini: {str(e)}")

    def generate_response_with_context(self, question: str, context: List[str], mode: str = "full-book") -> str:
        """
        Generate a response using the Gemini model with provided context
        """
        import logging
        context_str = "\n".join(context) if context else ""

        if mode == "selected-text":
            prompt = f"""
            Answer the question based ONLY on the provided selected text.
            Do not use any external knowledge or information outside of the provided text.
            If the answer is not in the provided text, clearly state that the answer cannot be found in the provided text.

            Selected Text: {context_str}

            Question: {question}

            Answer (with specific reference to the provided text):
            """
        else:  # full-book mode
            prompt = f"""
            Answer the question based ONLY on the provided book content.
            Do not use any external knowledge or information outside of the provided content.
            If the answer is not in the provided content, clearly state that the answer cannot be found in the book.

            Book Content: {context_str}

            Question: {question}

            Answer (with citations to relevant chapters/sections):
            """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            raise Exception(f"Error generating response from Gemini: {str(e)}")

    def validate_response_against_context(self, response: str, context: List[str]) -> bool:
        """
        Validate that the response is grounded in the provided context
        """
        # Basic validation - check if response has content
        if not response or len(response.strip()) == 0:
            return False

        # In a more sophisticated implementation, we could check for semantic similarity
        # between the response and the context
        return True  # Placeholder implementation

    def generate_response_with_latency_safeguards(self, prompt: str, max_tokens: int = 1000,
                                                  safety_settings: Dict = None) -> str:
        """
        Generate a response with latency and token safeguards
        """
        if safety_settings is None:
            safety_settings = {
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            }

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                ),
                safety_settings=safety_settings
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error generating response from Gemini with safeguards: {str(e)}")