import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

SOURCE_DIR = Path(__file__).resolve().parents[1]
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from build_manager import BuildManager


class BuildManagerModeTests(unittest.TestCase):
    def test_detached_head_builds_the_checked_out_commit(self):
        manager = object.__new__(BuildManager)
        manager.worktrees_dir = Path.cwd() / "worktrees"
        version = object.__new__(type("Version", (), {}))
        version.branch = "configured-branch"
        version.name = "configured-version"

        completed = type("Completed", (), {"stdout": "HEAD\n"})()
        with patch("build_manager.subprocess.run", return_value=completed) as run:
            self.assertEqual(manager.create_worktree(version), Path.cwd())

        run.assert_called_once_with(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )

    def test_both_modes_use_the_shared_build_pipeline(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            manager = object.__new__(BuildManager)
            manager.docs_source = source
            for mode, navigation in (("recursive_tree", "directory_tree"), ("project_catalog", "categories")):
                config = {"generation": {"discovery": {"mode": mode}, "navigation": {"mode": navigation}}}
                (source / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
                version = object()
                with self.subTest(mode=mode), patch.object(manager, "_build_html_and_pdf", return_value=True) as build:
                    self.assertTrue(manager.build_docs_in_worktree(Path.cwd(), version))
                    build.assert_called_once_with(source, version, config)


if __name__ == "__main__":
    unittest.main()
