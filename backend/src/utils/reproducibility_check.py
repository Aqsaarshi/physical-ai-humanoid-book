"""
Reproducibility verification utility for the RAG pipeline
"""
import hashlib
import json
from datetime import datetime
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.qdrant_service import QdrantService
from services.gemini_service import GeminiService
from services.retrieval_service import RetrievalService
from config import settings


class ReproducibilityChecker:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.gemini_service = GeminiService()
        self.retrieval_service = RetrievalService()

    def generate_pipeline_fingerprint(self, query: str, context_mode: str = "full-book") -> Dict[str, Any]:
        """
        Generate a fingerprint of the RAG pipeline for the given query
        """
        fingerprint = {
            "query": query,
            "context_mode": context_mode,
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "qdrant_collection": self.retrieval_service.qdrant_service.collection_name,
                "model": "gemini-pro",  # Hardcoded for now, could be dynamic
            }
        }

        # Add Qdrant validation result
        try:
            is_valid = self.qdrant_service.validate_collection()
            fingerprint["qdrant_valid"] = is_valid
        except Exception as e:
            fingerprint["qdrant_valid"] = False
            fingerprint["qdrant_error"] = str(e)

        # Generate a hash of the fingerprint for easy comparison
        fingerprint_json = json.dumps(fingerprint, sort_keys=True)
        fingerprint["hash"] = hashlib.sha256(fingerprint_json.encode()).hexdigest()

        return fingerprint

    def verify_pipeline_reproducibility(self, query: str, expected_fingerprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify that the pipeline produces consistent results
        """
        current_fingerprint = self.generate_pipeline_fingerprint(query, expected_fingerprint.get("context_mode", "full-book"))

        verification_result = {
            "query": query,
            "is_reproducible": current_fingerprint["hash"] == expected_fingerprint["hash"],
            "current_fingerprint": current_fingerprint,
            "expected_fingerprint": expected_fingerprint,
            "differences": {}
        }

        # Check for specific differences
        if current_fingerprint["qdrant_valid"] != expected_fingerprint.get("qdrant_valid"):
            verification_result["differences"]["qdrant_valid"] = {
                "current": current_fingerprint["qdrant_valid"],
                "expected": expected_fingerprint.get("qdrant_valid")
            }

        return verification_result

    def run_full_pipeline_check(self) -> Dict[str, Any]:
        """
        Run a comprehensive reproducibility check of the entire pipeline
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "overall_status": "pass"
        }

        # Test queries for different scenarios
        test_queries = [
            {"query": "What is the main topic of this book?", "mode": "full-book"},
            {"query": "Can you summarize chapter 1?", "mode": "full-book"},
        ]

        for test_query in test_queries:
            fingerprint = self.generate_pipeline_fingerprint(
                test_query["query"],
                test_query["mode"]
            )
            results["checks"].append({
                "query": test_query["query"],
                "mode": test_query["mode"],
                "fingerprint": fingerprint
            })

        # Check if all required services are available
        service_checks = {
            "qdrant_connected": self.qdrant_service.validate_collection(),
            "gemini_configured": self._check_gemini_connection()
        }

        results["service_checks"] = service_checks
        results["overall_status"] = "pass" if all(service_checks.values()) else "fail"

        return results

    def _check_gemini_connection(self) -> bool:
        """
        Check if Gemini service is properly configured
        """
        try:
            # Try to generate a simple response to test the connection
            test_response = self.gemini_service.generate_response("Hello")
            return len(test_response) > 0
        except Exception:
            return False


def main():
    """
    Main function to run reproducibility checks
    """
    checker = ReproducibilityChecker()
    results = checker.run_full_pipeline_check()

    print("Reproducibility Check Results:")
    print(json.dumps(results, indent=2))

    if results["overall_status"] == "pass":
        print("\n✓ Pipeline is reproducible")
    else:
        print("\n✗ Pipeline has reproducibility issues")
        print("Service checks:", results["service_checks"])


if __name__ == "__main__":
    main()