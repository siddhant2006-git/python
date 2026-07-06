import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from repository import repository


class BranchWorkflowTests(unittest.TestCase):
    def test_checkout_new_branch_and_merge(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = repository(temp_dir)
            repo.init()

            Path(temp_dir, "file.txt").write_text("hello", encoding="utf-8")
            repo.add_path("file.txt")
            repo.commit("first commit")

            repo.branch("feature")
            Path(temp_dir, "file.txt").write_text("hello world", encoding="utf-8")
            repo.add_path("file.txt")
            repo.commit("feature commit")

            repo.checkout("main")
            Path(temp_dir, "file.txt").write_text("hello main", encoding="utf-8")
            repo.add_path("file.txt")
            repo.commit("main commit")

            result = repo.merge("feature")

            self.assertEqual(result, "feature")
            self.assertEqual(repo.get_current_branch(), "main")

    def test_rebase_feature_branch_onto_main(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = repository(temp_dir)
            repo.init()

            Path(temp_dir, "file.txt").write_text("hello", encoding="utf-8")
            repo.add_path("file.txt")
            repo.commit("first commit")

            repo.branch("feature")
            Path(temp_dir, "file.txt").write_text("hello feature", encoding="utf-8")
            repo.add_path("file.txt")
            repo.commit("feature commit")

            repo.checkout("main")
            Path(temp_dir, "file.txt").write_text("hello main", encoding="utf-8")
            repo.add_path("file.txt")
            repo.commit("main commit")

            repo.checkout("feature")
            result = repo.rebase("main")

            self.assertEqual(result, "feature")
            self.assertEqual(repo.get_current_branch(), "feature")
            self.assertNotEqual(repo.get_head_commit_hash(), repo._read_ref("main"))


if __name__ == "__main__":
    unittest.main()
