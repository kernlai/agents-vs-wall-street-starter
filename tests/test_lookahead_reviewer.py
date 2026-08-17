from __future__ import annotations

import json
import unittest

from signal_agent.lookahead import OpenAIReviewProvider, incomplete_review


class RecordingTransport:
    def __init__(self) -> None:
        self.request = None

    def post(self, url, payload, headers, timeout):
        self.request = (url, payload, headers, timeout)
        output = {
            "status": "passed",
            "issues": [],
            "reasoningSummary": "Every claim is reconstructable from supplied excerpts.",
        }
        return {
            "id": "resp-review-1",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps(output)}]}],
        }


class LookaheadReviewerTests(unittest.TestCase):
    def test_openai_review_is_structured_and_has_no_web_or_other_tools(self) -> None:
        transport = RecordingTransport()
        provider = OpenAIReviewProvider(api_key="secret", model="gpt-5.6-terra", transport=transport)
        result = provider.review(
            {
                "sourceManifest": [{"id": "src-1", "publishedAt": "2026-05-20"}],
                "sourceExcerpts": [{"sourceId": "src-1", "text": "Guidance was $100m."}],
                "informationCutoff": "2026-08-16T17:15:00+01:00",
                "promptSha256": "a" * 64,
                "researchAudit": {"schemaVersion": "research_audit.v1"},
                "proposals": [{"claimId": "claim-1", "summary": "Guidance was $100m."}],
            }
        )

        self.assertEqual(result["schemaVersion"], "lookahead_review.v1")
        self.assertEqual(result["status"], "passed")
        request = transport.request[1]
        self.assertNotIn("tools", request)
        self.assertFalse(request["store"])
        self.assertEqual(request["text"]["format"]["type"], "json_schema")
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertNotIn("secret", json.dumps(request))

    def test_missing_reviewer_is_explicitly_incomplete(self) -> None:
        review = incomplete_review("OPENAI_API_KEY is not set")
        self.assertEqual(review["status"], "incomplete")
        self.assertIn("OPENAI_API_KEY", review["reason"])


if __name__ == "__main__":
    unittest.main()
