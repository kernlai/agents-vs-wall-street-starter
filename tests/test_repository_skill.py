from __future__ import annotations

import unittest
from pathlib import Path


class RepositorySkillTests(unittest.TestCase):
    def test_research_skill_has_valid_minimal_structure_and_no_placeholders(self) -> None:
        root = Path(".agents/skills/researching-company-signals")
        content = (root / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: researching-company-signals\n"))
        self.assertIn("description:", content.split("---", 2)[1])
        self.assertNotIn("TODO", content)
        self.assertTrue((root / "agents/openai.yaml").is_file())
        self.assertTrue((root / "references/schemas.md").is_file())


if __name__ == "__main__":
    unittest.main()
