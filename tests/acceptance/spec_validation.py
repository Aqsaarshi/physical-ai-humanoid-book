"""
Final validation against spec acceptance criteria
"""
from src.services.rag_service import RAGService
from src.services.retrieval_service import RetrievalService
from src.services.gemini_service import GeminiService
from src.services.citation_service import CitationService
import time
from typing import Dict, Any


class SpecValidator:
    def __init__(self):
        self.rag_service = RAGService()
        self.retrieval_service = RetrievalService()
        self.gemini_service = GeminiService()
        self.citation_service = CitationService()

    def validate_answers_from_book_content_only(self) -> Dict[str, Any]:
        """
        Validate that answers are strictly grounded in book content (SC-001)
        """
        test_query = "What is the main concept discussed in the book?"

        # Generate response using RAG
        result = self.rag_service.generate_answer_with_context(test_query)

        validation = {
            "requirement": "Answers are strictly grounded in book content",
            "query": test_query,
            "response": result["content"][:100] + "...",  # Truncate for display
            "citations_present": len(result["citations"]) > 0,
            "confidence": result["confidence"],
            "passed": result["confidence"] == "high" and len(result["citations"]) > 0
        }

        return validation

    def validate_selected_text_mode(self) -> Dict[str, Any]:
        """
        Validate selected-text mode ignores non-selected content (SC-002)
        """
        selected_text = "Artificial intelligence is a branch of computer science."
        test_query = "What is artificial intelligence?"

        # Use selected text mode
        result = self.rag_service.generate_answer_with_context(
            test_query,
            mode="selected-text",
            selected_text=selected_text
        )

        validation = {
            "requirement": "Selected-text mode ignores non-selected content",
            "selected_text": selected_text,
            "query": test_query,
            "response": result["content"][:100] + "...",
            "citations_present": len(result["citations"]) > 0,
            "passed": selected_text.lower() in result["content"].lower()
        }

        return validation

    def validate_response_time(self) -> Dict[str, Any]:
        """
        Validate response time requirement (SC-004)
        """
        test_query = "What is the summary of the book?"

        start_time = time.time()
        result = self.rag_service.generate_answer_with_context(test_query)
        end_time = time.time()

        response_time = end_time - start_time

        validation = {
            "requirement": "Response time under 10 seconds",
            "query": test_query,
            "response_time_seconds": round(response_time, 2),
            "passed": response_time < 10.0  # Less than 10 seconds
        }

        return validation

    def run_all_validations(self) -> Dict[str, Any]:
        """
        Run all spec validations and return results
        """
        results = {
            "timestamp": time.time(),
            "validations": [],
            "overall_passed": True
        }

        # Run each validation
        validations = [
            self.validate_answers_from_book_content_only(),
            self.validate_selected_text_mode(),
            self.validate_response_time()
        ]

        results["validations"] = validations
        results["overall_passed"] = all(v["passed"] for v in validations)

        return results


def main():
    validator = SpecValidator()
    results = validator.run_all_validations()

    print("Specification Validation Results:")
    print("=" * 50)

    for i, validation in enumerate(results["validations"], 1):
        status = "✓ PASS" if validation["passed"] else "✗ FAIL"
        print(f"{i}. {status} - {validation['requirement']}")
        print(f"   Query: {validation.get('query', 'N/A')}")
        print(f"   Result: {validation.get('response', validation.get('response_time_seconds', 'N/A'))}")
        print()

    overall_status = "✓ ALL TESTS PASSED" if results["overall_passed"] else "✗ SOME TESTS FAILED"
    print(f"Overall Status: {overall_status}")

    return results["overall_passed"]


if __name__ == "__main__":
    main()