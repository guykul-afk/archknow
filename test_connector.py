# -*- coding: utf-8 -*-
"""
Tests for archknow_client.py SDK against live local test server.
"""
import threading
import time
import unittest
from server import app
from archknow_client import ArchKnowClient
from werkzeug.serving import make_server


class TestServerThread(threading.Thread):
    def __init__(self, app, port=5055):
        super().__init__()
        self.server = make_server('127.0.0.1', port, app)
        self.port = port
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


class TestArchKnowClientSDK(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_thread = TestServerThread(app, port=5055)
        cls.server_thread.start()
        time.sleep(0.5)
        cls.client = ArchKnowClient(base_url="http://127.0.0.1:5055/api/v1")

    @classmethod
    def tearDownClass(cls):
        cls.server_thread.shutdown()

    def test_01_health(self):
        data = self.client.health()
        self.assertEqual(data.get("status"), "healthy")
        self.assertGreater(data.get("loaded_projects_count"), 0)
        print("[OK] Client.health() passed")

    def test_02_projects(self):
        projects = self.client.list_projects()
        self.assertEqual(len(projects), 5)
        p = self.client.get_project("pines48")
        self.assertEqual(p.get("project_id"), "pines48")
        print("[OK] Client.list_projects() and get_project() passed")

    def test_03_summary(self):
        summary = self.client.get_project_summary("kkl10")
        self.assertIn("markdown_prompt_context", summary)
        md = self.client.get_prompt_markdown("kkl10")
        self.assertTrue(len(md) > 100)
        print("[OK] Client.get_project_summary() passed")

    def test_04_analysis_and_shorthands(self):
        analysis = self.client.get_analysis("pines48", status="WARN")
        self.assertGreater(analysis.get("total_matched"), 0)
        warnings = self.client.get_warnings("pines48")
        self.assertEqual(len(warnings), analysis.get("total_matched"))
        violations = self.client.get_violations("kkl10")
        self.assertIsInstance(violations, list)
        print("[OK] Client.get_analysis(), get_warnings(), get_violations() passed")

    def test_05_spatial(self):
        sp = self.client.get_spatial_metrics("hafetz44")
        self.assertEqual(sp.get("project_id"), "hafetz44")
        print("[OK] Client.get_spatial_metrics() passed")

    def test_06_compare(self):
        comp = self.client.compare_projects(["pines48", "kkl10"])
        self.assertEqual(len(comp), 2)
        print("[OK] Client.compare_projects() passed")

    def test_07_ai_context(self):
        ctx = self.client.get_ai_context("רוחב ממד", project_id="kkl10")
        self.assertIn("prompt_context", ctx)
        self.assertGreater(ctx.get("matched_count"), 0)
        print("[OK] Client.get_ai_context() passed")

    def test_08_rules(self):
        rules = self.client.list_rules(limit=5)
        self.assertGreater(rules.get("total_rules"), 300)
        rule = self.client.get_rule("B1.13")
        self.assertEqual(rule.get("rule_id"), "B1.13")
        cats = self.client.get_rule_categories()
        self.assertGreater(len(cats), 0)
        print("[OK] Client.list_rules(), get_rule(), get_rule_categories() passed")

    def test_09_validate(self):
        res = self.client.validate_apartment_file("pines48_apt_c_sample.json")
        self.assertEqual(res.get("status"), "success")
        self.assertGreater(res.get("total_checks"), 0)
        print("[OK] Client.validate_apartment_file() passed")

    def test_10_tools_and_dispatcher(self):
        oai_tools = self.client.get_openai_tools()
        self.assertGreater(len(oai_tools), 0)
        claude_tools = self.client.get_anthropic_tools()
        self.assertEqual(len(oai_tools), len(claude_tools))

        # Test tool dispatcher execution
        disp_res = self.client.execute_tool_call(
            "get_project_ai_summary",
            {"project_id": "pines48"}
        )
        self.assertEqual(disp_res.get("project_id"), "pines48")
        print("[OK] Client.get_openai_tools() and execute_tool_call() passed")

    def test_11_openapi(self):
        spec = self.client.get_openapi_spec()
        self.assertEqual(spec.get("openapi"), "3.1.0")
        print("[OK] Client.get_openapi_spec() passed")

    def test_12_download_client_file(self):
        import urllib.request
        # Test download from /api/v1/client.py
        with urllib.request.urlopen("http://127.0.0.1:5055/api/v1/client.py") as resp:
            self.assertEqual(resp.status, 200)
            content = resp.read().decode('utf-8')
            self.assertIn("class ArchKnowClient", content)

        # Test download from root /archknow_client.py
        with urllib.request.urlopen("http://127.0.0.1:5055/archknow_client.py") as resp2:
            self.assertEqual(resp2.status, 200)
            content2 = resp2.read().decode('utf-8')
            self.assertIn("class ArchKnowClient", content2)

        print("[OK] External Client download URLs verified!")
        print("[OK] Client.get_openapi_spec() passed")


if __name__ == "__main__":
    unittest.main()
