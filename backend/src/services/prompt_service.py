from typing import List, Dict, Any


class PromptService:
    @staticmethod
    def construct_rag_prompt(question: str, context: List[str], mode: str = "full-book") -> str:
        """
        Construct a RAG prompt based on the question, context, and mode
        """
        context_str = "\n".join(context)

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

        return prompt

    @staticmethod
    def construct_fallback_prompt(question: str) -> str:
        """
        Construct a fallback prompt when no relevant context is found
        """
        return f"""
        The question is: {question}

        I cannot answer this question based on the provided book content.
        The information needed to answer this question is not available in the provided context.
        """