# -*- coding: utf-8 -*-
"""
Verification suite for ArchiCheck AI REST API (v1).
"""
import json
import unittest
from server import app


class TestArchiCheckApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_01_health(self):
        res = self.client.get('/api/v1/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'healthy')
        self.assertGreater(data.get('loaded_projects_count', 0), 0)
        self.assertGreater(data.get('loaded_okf_rules_count', 0), 0)
        print("[OK] Health Check Passed:", data.get('service'))

    def test_02_projects_list(self):
        res = self.client.get('/api/v1/projects')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(data.get('total'), 5)
        p_ids = [p['id'] for p in data.get('projects', [])]
        self.assertIn('pines48', p_ids)
        self.assertIn('kkl10', p_ids)
        print("[OK] Projects List Passed. Found projects:", p_ids)

    def test_03_project_details(self):
        res = self.client.get('/api/v1/projects/pines48')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        project = data.get('project', {})
        self.assertEqual(project.get('project_id'), 'pines48')
        self.assertGreater(project.get('sheets_count'), 0)
        print("[OK] Project Details Passed:", project.get('project_id'))

    def test_04_project_analysis_filtering(self):
        # All notes
        res_all = self.client.get('/api/v1/projects/pines48/analysis')
        self.assertEqual(res_all.status_code, 200)
        data_all = res_all.get_json()
        total = data_all.get('total_matched')
        self.assertGreater(total, 0)

        # Filter by WARN,PASS
        res_filter = self.client.get('/api/v1/projects/pines48/analysis?status=WARN')
        self.assertEqual(res_filter.status_code, 200)
        data_filter = res_filter.get_json()
        for note in data_filter.get('notes', []):
            self.assertEqual(note.get('status'), 'WARN')

        # Filter by room
        res_room = self.client.get('/api/v1/projects/pines48/analysis?room=%D7%A1%D7%9C%D7%95%D7%9F')
        self.assertEqual(res_room.status_code, 200)
        print(f"[OK] Analysis Filtering Passed. Total: {total}, WARNs: {data_filter.get('total_matched')}")

    def test_05_ai_summary(self):
        res = self.client.get('/api/v1/projects/kkl10/summary')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('markdown_prompt_context', data)
        self.assertIn('token_estimate', data)
        self.assertIn('structured', data)
        print(f"[OK] AI Executive Summary Passed. Approx tokens: {data.get('token_estimate')}")

    def test_06_spatial_metrics(self):
        res = self.client.get('/api/v1/projects/pines48/spatial-metrics')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        metrics = data.get('spatial_metrics', {})
        self.assertEqual(metrics.get('project_id'), 'pines48')
        print("[OK] Spatial Metrics Passed. Sheets:", len(metrics.get('sheets', [])))

    def test_07_compare_projects(self):
        res = self.client.get('/api/v1/compare?projects=pines48,kkl10,kitroni37')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(data.get('total_compared'), 3)
        print("[OK] Compare Projects Passed. Compared 3 projects successfully.")

    def test_08_ai_context_packing(self):
        payload = {
            "query": "safe room dimensions driveway issues",
            "project_id": "kkl10",
            "max_items": 4
        }
        res = self.client.post('/api/v1/ai/context', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('prompt_context', data)
        self.assertGreater(data.get('matched_count', 0), 0)
        print("[OK] AI Context Packing Passed. Matched findings:", data.get('matched_count'))

    def test_09_rules_discovery(self):
        res = self.client.get('/api/v1/rules?limit=10')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(data.get('total_rules', 0), 300)
        self.assertGreater(len(data.get('available_categories', [])), 0)

        # Test specific rule
        res_single = self.client.get('/api/v1/rules/B1.13')
        self.assertEqual(res_single.status_code, 200)
        self.assertEqual(res_single.get_json().get('rule', {}).get('rule_id'), 'B1.13')
        print(f"[OK] Rules Discovery Passed. Loaded {data.get('total_rules')} rules.")

    def test_10_live_plan_validation(self):
        sample_apartment = {
            "apartment_id": "test_apt_01",
            "bedrooms": 3,
            "bedspaces": 5,
            "net_area_sqm": 85.0,
            "global_parameters": {
                "ceiling_height_m": 2.65
            },
            "rooms": [
                {
                    "room_name": "living_room",
                    "room_type": "living",
                    "area_sqm": 24.5,
                    "depth_m": 5.2,
                    "window_area_sqm": 3.8
                },
                {
                    "room_name": "safe_room",
                    "room_type": "safe_room",
                    "area_sqm": 9.2,
                    "depth_m": 2.75,
                    "window_area_sqm": 1.05
                }
            ]
        }
        res = self.client.post('/api/v1/analyze/plan', json=sample_apartment)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(data.get('total_checks', 0), 0)
        print(f"[OK] Live Validation Engine Passed. Ran {data.get('total_checks')} checks.")

    def test_11_ai_tools_spec(self):
        res = self.client.get('/api/v1/ai/tools')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('openai_tools', data)
        self.assertIn('anthropic_tools', data)
        self.assertGreater(len(data.get('openai_tools')), 0)
        print("[OK] AI Tools Specification Passed. Tools count:", len(data.get('openai_tools')))

    def test_12_openapi_spec(self):
        res = self.client.get('/api/v1/openapi.json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get('openapi'), '3.1.0')
        self.assertIn('/projects', data.get('paths', {}))
        self.assertIn('/ai/context', data.get('paths', {}))
        print("[OK] OpenAPI 3.1.0 Specification Validated.")

    def test_13_docs_ui(self):
        res = self.client.get('/api/v1/docs')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SwaggerUIBundle', res.data)
        print("[OK] Interactive Swagger UI Docs Page Loaded.")


if __name__ == '__main__':
    unittest.main()
