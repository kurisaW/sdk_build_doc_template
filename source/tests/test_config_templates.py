import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SOURCE_DIR = Path(__file__).resolve().parents[1]
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from pdf_generator_enhanced_v2 import DocumentScanner
from utils.document_catalog import DocumentCatalog
from utils.file_processor import FileProcessor
from utils.html_builder import build_html_site
from utils.index_generator import IndexGenerator


class ConfigTemplateTests(unittest.TestCase):
    def test_root_order_uses_navigation_and_natural_order(self):
        generator = object.__new__(IndexGenerator)
        generator.generation_config = {
            "navigation": {"order": ["second", "first"]},
        }
        directories = [Path("first"), Path("second"), Path("extra10"), Path("extra2")]
        self.assertEqual(
            generator._ordered_root_directories(directories),
            [Path("second"), Path("first"), Path("extra2"), Path("extra10")],
        )
        generator.generation_config["navigation"] = {}
        self.assertEqual(generator._ordered_root_directories(directories), [Path("extra2"), Path("extra10"), Path("first"), Path("second")])

    def test_removed_generation_fields_fail_with_migration_message(self):
        with tempfile.TemporaryDirectory() as temporary:
            for generation in ({"mode": "project_catalog"}, {"output_structure": []}):
                with self.subTest(generation=generation), self.assertRaisesRegex(ValueError, "Removed generation fields"):
                    DocumentCatalog.build(Path(temporary), {}, generation)

    def test_templates_support_round_trip_mode_switch_and_real_html(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            projects = root / "projects"
            source = root / "source"
            source.mkdir()
            shutil.copy2(SOURCE_DIR / "conf.py", source / "conf.py")
            for directory in ("utils", "_static", "_templates"):
                shutil.copytree(SOURCE_DIR / directory, source / directory)
            names = ["Board_template", "Board_basic_demo", "Board_dual_core/core0", "Board_dual_core/core1"]
            for relative in ["."] + names + ["Board_basic_demo/vendor"]:
                directory = projects / relative
                directory.mkdir(parents=True, exist_ok=True)
                for filename in ("README.md", "README_zh.md"):
                    (directory / filename).write_text(
                        f'# {relative}\n\n<iframe src="./demo.html"></iframe>\n\n[Animation](./demo.html)\n',
                        encoding="utf-8",
                    )
                for filename in ("demo.html", "demo.css", "demo.js"):
                    (directory / filename).write_text("test asset", encoding="utf-8")
            sentinel = source / "user-owned.txt"
            sentinel.write_text("keep", encoding="utf-8")
            for mode in ("recursive_tree", "project_catalog", "recursive_tree"):
                with self.subTest(mode=mode):
                    config = yaml.safe_load((SOURCE_DIR / "config_templates" / f"{mode}.yaml").read_text(encoding="utf-8"))
                    config["repository"]["projects_dir"] = "../projects"
                    generation = config["generation"]
                    if mode == "recursive_tree":
                        order = ["Board_dual_core", "Board_basic_demo", "Board_template"]
                        config["categories"] = {name: {"name": name} for name in order}
                        generation["navigation"]["order"] = order
                        generation["navigation"]["directory_order"] = {"Board_dual_core": ["core1", "core0"]}
                    (source / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")
                    catalog = DocumentCatalog.build(projects, config["categories"], generation)
                    processor = FileProcessor(str(projects), str(source), generation, catalog=catalog)
                    processor.cleanup_dest_dir()
                    processor.sync_document_tree()
                    IndexGenerator(str(source), processor).generate_all_indexes(config["categories"], {}, config["project"])
                    processor.finalize_manifest()
                    self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
                    self.assertEqual((source / "Board_basic_demo/vendor/README.md").exists(), mode == "recursive_tree")
                    self.assertEqual((source / "_navigation/basic_zh.rst").exists(), mode == "project_catalog")
                    for filename in ("demo.html", "demo.css", "demo.js"):
                        self.assertTrue((source / "Board_basic_demo" / filename).is_file())
                    scanner = DocumentScanner(source / "_build/html", projects, source / "config.yaml")
                    for language in ("zh", "en"):
                        documents = scanner.scan_documents(language)
                        if mode == "project_catalog":
                            self.assertEqual(list(documents), ["start", "basic", "multicore"])
                            self.assertEqual(len(documents["basic"]), 1)
                        else:
                            self.assertEqual(list(documents), order)
                            self.assertEqual([doc["file"].parent.name for doc in documents["Board_dual_core"]], ["core1", "core0"])
                    output = root / "html"
                    build_html_site(source, output, config, ("zh", "en"), "zh")
                    for filename in ("README_zh.html", "README.html"):
                        page = (output / "Board_basic_demo" / filename).read_text(encoding="utf-8")
                        self.assertIn('src="./demo.html"', page)
                        self.assertIn('target="_blank"', page)
                        self.assertIn("image_viewer.js", page)
                    self.assertTrue((output / "Board_basic_demo/demo.html").is_file())


if __name__ == "__main__":
    unittest.main()
