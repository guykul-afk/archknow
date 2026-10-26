# -*- coding: utf-8 -*-
"""
ArchiCheck (ArchKnow) - Unified AI Connector & SDK Client
קובץ קישור כולל (All-In-One Connector) לכל שירותי ה-API של מערכת ArchiCheck.

קובץ זה מספק ממשק שלם (SDK / Client) ב-Python, עצמאי לחלוטין וללא תלויות חובה
(עובד עם ספריית הסטנדרט של Python או עם requests), ומאפשר לכל מערכת AI, סוכן אוטומטי,
או סקריפט להתחבר ולבצע את כל הפעולות מול כל שירותי המערכת.

שירותים נתמכים:
1. Health & System - בדיקת סטטוס מערכת
2. Projects - קטלוג ופרטי פרויקטים
3. AI Summary - סיכומי מנהלים חסכוניים בטוקנים
4. Analysis & Filtering - תחקור ממצאים (כשלים סטטוטוריים, התראות איכות, סינון לפי חדרים)
5. Spatial Metrics - מטריקות גיאומטריות וטופולוגיה
6. Compare - השוואה רוחבית של פרויקטים
7. AI Context - אורז קונטקסט לשאלות טבעיות (RAG)
8. OKF Rules - מאגר 400+ חוקי תכנון ובנייה
9. Live Plan Validation - אימות דירות בזמן אמת
10. AI Tooling Dispatcher - הרצת Tool Calling אוטומטית עבור OpenAI ו-Claude
11. OpenAPI Spec - ייצוא מפרט OpenAPI

שימוש כספרייה:
    from archknow_client import ArchKnowClient
    client = ArchKnowClient(base_url="http://localhost:5000/api/v1")
    projects = client.list_projects()
    summary = client.get_project_summary("pines48")
    context = client.get_ai_context("מה הליקויים בקק״ל 10?")

שימוש משורת הפקודה (CLI):
    python archknow_client.py health
    python archknow_client.py projects
    python archknow_client.py summary pines48
    python archknow_client.py analysis kkl10 --status FAIL,WARN
    python archknow_client.py compare
    python archknow_client.py context "מה הבעיות במיסעה?"
    python archknow_client.py rules --query ממד
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, List, Any, Optional, Union

# Try importing requests for enhanced performance, fallback to urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class ArchKnowAPIError(Exception):
    """Exception raised when an API call returns an error status."""
    def __init__(self, status_code: int, error_code: str, message: str, payload: Optional[dict] = None):
        super().__init__(f"[{status_code} - {error_code}] {message}")
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.payload = payload or {}


class ArchKnowClient:
    """
    Unified client for all ArchiCheck API services.
    """

    def __init__(self, base_url: str = "http://localhost:5000/api/v1", api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize the ArchiCheck API client.

        :param base_url: The root URL of the API (default: http://localhost:5000/api/v1)
        :param api_key: Optional API Key for authentication (if required by server)
        :param timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.environ.get("ARCHKNOW_API_KEY", "").strip() or None
        self.timeout = timeout

    # -------------------------------------------------------------------------
    # Internal Request Handler
    # -------------------------------------------------------------------------

    def _request(self, method: str, path: str, params: Optional[dict] = None, json_body: Optional[dict] = None) -> Any:
        """Internal unified HTTP request handler supporting requests and urllib."""
        clean_path = path if path.startswith('/') else f"/{path}"
        url = f"{self.base_url}{clean_path}"

        headers = {
            "Accept": "application/json",
            "User-Agent": "ArchKnow-AI-Connector/1.0"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["X-API-Key"] = self.api_key

        if HAS_REQUESTS:
            try:
                resp = requests.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    json=json_body,
                    headers=headers,
                    timeout=self.timeout
                )
                try:
                    data = resp.json()
                except Exception:
                    data = {"raw_text": resp.text}

                if not resp.ok:
                    err_code = data.get("error_code", "HTTP_ERROR")
                    msg = data.get("message", resp.text)
                    raise ArchKnowAPIError(resp.status_code, err_code, msg, data)
                return data
            except requests.RequestException as e:
                if isinstance(e, requests.HTTPError) and e.response is not None:
                    raise
                raise ConnectionError(f"Failed to connect to ArchiCheck API at {url}: {str(e)}")
        else:
            # Fallback to urllib.request
            if params:
                query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
                url = f"{url}?{query_string}"

            body_data = None
            if json_body is not None:
                body_data = json.dumps(json_body, ensure_ascii=False).encode('utf-8')
                headers["Content-Type"] = "application/json; charset=utf-8"

            req = urllib.request.Request(url, data=body_data, headers=headers, method=method.upper())
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    raw_bytes = response.read()
                    charset = response.headers.get_content_charset() or 'utf-8'
                    text = raw_bytes.decode(charset)
                    return json.loads(text)
            except urllib.error.HTTPError as e:
                raw_bytes = e.read()
                try:
                    text = raw_bytes.decode('utf-8')
                    err_data = json.loads(text)
                except Exception:
                    err_data = {"raw_text": str(raw_bytes)}
                err_code = err_data.get("error_code", f"HTTP_{e.code}")
                msg = err_data.get("message", str(e))
                raise ArchKnowAPIError(e.code, err_code, msg, err_data)
            except urllib.error.URLError as e:
                raise ConnectionError(f"Failed to connect to ArchiCheck API at {url}: {e.reason}")

    # =========================================================================
    # Service 1: Health & System Information
    # =========================================================================

    def health(self) -> Dict[str, Any]:
        """
        Check API health, engine status, and loaded architectural standards.
        Returns system status, active version, total rules loaded, and projects count.
        """
        return self._request("GET", "/health")

    # =========================================================================
    # Service 2: Projects Management & Catalog
    # =========================================================================

    def list_projects(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all architectural projects in the catalog with compliance scores.

        :param query: Optional search filter by name, city, or keyword.
        :return: List of project summary objects.
        """
        params = {"q": query} if query else None
        res = self._request("GET", "/projects", params=params)
        return res.get("projects", [])

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        Get full project metadata, sheets (plans), sections, and high-level KPIs.

        :param project_id: Project identifier ('pines48', 'kkl10', 'hafetz44', 'yatkovski7', 'kitroni37')
        """
        res = self._request("GET", f"/projects/{project_id}")
        return res.get("project", {})

    # =========================================================================
    # Service 3: AI-Optimized Executive Summaries (Token-Budgeted)
    # =========================================================================

    def get_project_summary(self, project_id: str) -> Dict[str, Any]:
        """
        Fetch a compact, prompt-ready architectural executive summary.
        Includes estimated token count, formatted Markdown summary, and structured metrics.

        :param project_id: Project identifier
        """
        return self._request("GET", f"/projects/{project_id}/summary")

    def get_prompt_markdown(self, project_id: str) -> str:
        """
        Helper method returning only the Markdown text block ready to inject into an LLM prompt.

        :param project_id: Project identifier
        :return: Pre-formatted Markdown summary string
        """
        summary = self.get_project_summary(project_id)
        return summary.get("markdown_prompt_context", "")

    # =========================================================================
    # Service 4: Deep Audit Analysis & Findings Filtering
    # =========================================================================

    def get_analysis(
        self,
        project_id: str,
        status: Optional[str] = None,
        room: Optional[str] = None,
        rule_id: Optional[str] = None,
        query: Optional[str] = None,
        sheet_id: Optional[str] = None,
        section_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Query architectural audit findings with fine-grained filters.

        :param project_id: Project identifier
        :param status: Filter by status ('FAIL', 'WARN', 'PASS', or comma-separated 'FAIL,WARN')
        :param room: Filter by room name or typology keyword (e.g. 'ממ"ד', 'מטבח', 'סלון')
        :param rule_id: Filter by rule ID (e.g. 'B1.13', 'IS1918', 'NKBA')
        :param query: Free-text search in title, summary, and recommendation
        :param sheet_id: Filter by sheet/floor ID
        :param section_id: Filter by section ID
        :param limit: Maximum findings to return (default: 50, max: 200)
        :param offset: Pagination offset
        """
        params = {
            "status": status,
            "room": room,
            "rule_id": rule_id,
            "q": query,
            "sheet_id": sheet_id,
            "section_id": section_id,
            "limit": limit,
            "offset": offset
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", f"/projects/{project_id}/analysis", params=clean_params)

    def get_violations(self, project_id: str) -> List[Dict[str, Any]]:
        """Shorthand to retrieve only statutory failures (status='FAIL')."""
        res = self.get_analysis(project_id, status="FAIL", limit=100)
        return res.get("notes", [])

    def get_warnings(self, project_id: str) -> List[Dict[str, Any]]:
        """Shorthand to retrieve design & ergonomic warnings (status='WARN')."""
        res = self.get_analysis(project_id, status="WARN", limit=100)
        return res.get("notes", [])

    # =========================================================================
    # Service 5: Spatial Metrics & CAD Topology
    # =========================================================================

    def get_spatial_metrics(self, project_id: str) -> Dict[str, Any]:
        """
        Get dimensional, room breakdown, and spatial topology metrics.

        :param project_id: Project identifier
        """
        res = self._request("GET", f"/projects/{project_id}/spatial-metrics")
        return res.get("spatial_metrics", {})

    # =========================================================================
    # Service 6: Comparative Benchmarking
    # =========================================================================

    def compare_projects(self, projects: Optional[Union[List[str], str]] = None) -> List[Dict[str, Any]]:
        """
        Side-by-side benchmarking of architectural projects.

        :param projects: Optional list or comma-separated string of project IDs.
                         Defaults to comparing all catalog projects.
        :return: List of comparative project objects sorted by score descending.
        """
        params = None
        if projects:
            if isinstance(projects, list):
                params = {"projects": ",".join(projects)}
            else:
                params = {"projects": projects}
        res = self._request("GET", "/compare", params=params)
        return res.get("comparison", [])

    # =========================================================================
    # Service 7: AI RAG & Context Packing (for LLMs)
    # =========================================================================

    def get_ai_context(self, query: str, project_id: Optional[str] = None, max_items: int = 6) -> Dict[str, Any]:
        """
        Extract relevant architectural findings and guidelines for an external LLM.
        Returns a prompt-ready context block for RAG prompt construction.

        :param query: User question or topic (e.g. 'מה הליקויים במיסעה ובממדים?')
        :param project_id: Target project ID (or None for auto-detection)
        :param max_items: Maximum relevant findings to retrieve
        """
        payload = {
            "query": query,
            "project_id": project_id,
            "max_items": max_items
        }
        clean_payload = {k: v for k, v in payload.items() if v is not None}
        return self._request("POST", "/ai/context", json_body=clean_payload)

    # =========================================================================
    # Service 8: OKF Architectural Rules Knowledge Base
    # =========================================================================

    def list_rules(self, category: Optional[str] = None, query: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Search and explore the 400+ OKF architectural rules and standards.

        :param category: Category filter (e.g. 'Planning Standards', 'Accessibility', 'Kitchen & Bathroom Ergonomics')
        :param query: Keyword search in rule definitions
        :param limit: Max items to return
        :param offset: Pagination offset
        """
        params = {
            "category": category,
            "q": query,
            "limit": limit,
            "offset": offset
        }
        clean_params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "/rules", params=clean_params)

    def get_rule(self, rule_id: str) -> Dict[str, Any]:
        """
        Get the full specification and thresholds for a specific rule ID.

        :param rule_id: Rule identifier (e.g. 'B1.13', 'NDSS_1B2P', 'IS1918_DOOR')
        """
        res = self._request("GET", f"/rules/{rule_id}")
        return res.get("rule", {})

    def get_rule_categories(self) -> List[str]:
        """Get a list of all distinct rule categories available in the knowledge base."""
        res = self.list_rules(limit=1)
        return res.get("available_categories", [])

    # =========================================================================
    # Service 9: Live Plan Validation Engine
    # =========================================================================

    def validate_plan(self, apartment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit apartment plan JSON to the live validation engine and get immediate results.

        :param apartment_data: Apartment schema dictionary (net_area_sqm, bedrooms, ceiling_height, rooms, etc.)
        """
        return self._request("POST", "/analyze/plan", json_body=apartment_data)

    def validate_apartment_file(self, json_file_path: str) -> Dict[str, Any]:
        """
        Load an apartment or project JSON file from disk and validate it.

        :param json_file_path: Path to the local JSON file
        """
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle project file with floors/apartments
        if "floors" in data and data["floors"]:
            first_apt = data["floors"][0]["apartments"][0]
            return self.validate_plan(first_apt)
        return self.validate_plan(data)

    # =========================================================================
    # Service 10: Tooling Specifications & Tool Dispatcher for AI Agents
    # =========================================================================

    def get_tools_spec(self) -> Dict[str, Any]:
        """
        Get tool specifications formatted for OpenAI and Anthropic Claude.
        """
        return self._request("GET", "/ai/tools")

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Get pre-baked OpenAI Tools array ready for openai.chat.completions.create(tools=...)."""
        spec = self.get_tools_spec()
        return spec.get("openai_tools", [])

    def get_anthropic_tools(self) -> List[Dict[str, Any]]:
        """Get pre-baked Anthropic Claude tools array ready for anthropic.messages.create(tools=...)."""
        spec = self.get_tools_spec()
        return spec.get("anthropic_tools", [])

    def execute_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Universal tool execution router for AI Agents.
        Executes a function call requested by an LLM and returns the structured output.

        :param tool_name: The name of the function invoked by the LLM
        :param arguments: Dictionary of arguments provided by the LLM
        """
        if tool_name == "list_architectural_projects":
            return self.list_projects(query=arguments.get("q"))
        elif tool_name == "get_project_ai_summary":
            return self.get_project_summary(arguments["project_id"])
        elif tool_name == "get_project_audit_notes":
            return self.get_analysis(
                project_id=arguments["project_id"],
                status=arguments.get("status"),
                room=arguments.get("room"),
                query=arguments.get("q")
            )
        elif tool_name == "get_ai_architectural_context":
            return self.get_ai_context(
                query=arguments["query"],
                project_id=arguments.get("project_id")
            )
        elif tool_name == "compare_architectural_projects":
            return self.compare_projects(projects=arguments.get("projects"))
        elif tool_name == "search_architectural_rules":
            return self.list_rules(
                category=arguments.get("category"),
                query=arguments.get("q")
            )
        else:
            raise ValueError(f"Unknown tool name: {tool_name}")

    # =========================================================================
    # Service 11: OpenAPI Specification
    # =========================================================================

    def get_openapi_spec(self) -> Dict[str, Any]:
        """Fetch the full OpenAPI 3.1.0 specification dictionary."""
        return self._request("GET", "/openapi.json")


# =============================================================================
# Command-Line Interface (CLI)
# =============================================================================

def main():
    """CLI Entry Point for testing and operating the API client directly."""
    import argparse

    parser = argparse.ArgumentParser(
        description="ArchiCheck AI API - Unified CLI Connector & Tester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
דוגמאות שימוש:
  python archknow_client.py health
  python archknow_client.py projects
  python archknow_client.py summary pines48
  python archknow_client.py analysis kkl10 --status FAIL,WARN
  python archknow_client.py compare --projects pines48,kkl10,kitroni37
  python archknow_client.py context "מה הליקויים במיסעה?"
  python archknow_client.py rules --query ממד
  python archknow_client.py validate pines48_apt_c_sample.json
        """
    )
    parser.add_argument("--url", default="http://localhost:5000/api/v1", help="API Base URL (default: http://localhost:5000/api/v1)")
    parser.add_argument("--key", default=None, help="Optional API Key")

    subparsers = parser.add_subparsers(dest="command", help="API Services")

    # health
    subparsers.add_parser("health", help="Check API health and status")

    # projects
    proj_parser = subparsers.add_parser("projects", help="List all architectural projects")
    proj_parser.add_argument("-q", "--query", help="Filter by name or keyword")

    # project
    p_detail_parser = subparsers.add_parser("project", help="Get project details & sheets")
    p_detail_parser.add_argument("project_id", help="Project ID (e.g. pines48, kkl10)")

    # summary
    sum_parser = subparsers.add_parser("summary", help="Get AI-optimized executive summary")
    sum_parser.add_argument("project_id", help="Project ID")
    sum_parser.add_argument("--raw", action="store_true", help="Print raw JSON instead of markdown")

    # analysis
    an_parser = subparsers.add_parser("analysis", help="Query architectural audit notes")
    an_parser.add_argument("project_id", help="Project ID")
    an_parser.add_argument("--status", help="Filter by status (FAIL, WARN, PASS)")
    an_parser.add_argument("--room", help="Filter by room keyword (e.g. ממ\"ד, סלון)")
    an_parser.add_argument("-q", "--query", help="Text search in findings")
    an_parser.add_argument("--limit", type=int, default=20, help="Max findings to show")

    # spatial
    sp_parser = subparsers.add_parser("spatial", help="Get spatial metrics & room dimensions")
    sp_parser.add_argument("project_id", help="Project ID")

    # compare
    cmp_parser = subparsers.add_parser("compare", help="Compare projects side-by-side")
    cmp_parser.add_argument("--projects", help="Comma-separated project IDs")

    # context
    ctx_parser = subparsers.add_parser("context", help="Extract AI prompt context for a question (RAG)")
    ctx_parser.add_argument("query", help="Question or topic")
    ctx_parser.add_argument("--project_id", help="Target project ID")

    # rules
    rule_parser = subparsers.add_parser("rules", help="Search OKF architectural rules")
    rule_parser.add_argument("-q", "--query", help="Keyword search in rules")
    rule_parser.add_argument("--category", help="Category filter")

    # validate
    val_parser = subparsers.add_parser("validate", help="Validate an apartment JSON file against OKF rules")
    val_parser.add_argument("file", help="Path to apartment JSON file")

    # tools
    subparsers.add_parser("tools", help="Print OpenAI & Anthropic tool calling specifications")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    client = ArchKnowClient(base_url=args.url, api_key=args.key)

    try:
        if args.command == "health":
            res = client.health()
            print(json.dumps(res, indent=2, ensure_ascii=False))

        elif args.command == "projects":
            projects = client.list_projects(query=args.query)
            print(f"Found {len(projects)} projects:\n" + "=" * 50)
            for p in projects:
                print(f"[{p['id']}] {p['short_name']} - Score: {p['score']}")
                print(f"  {p['subtitle']}")
                print(f"  Status: {p['status_summary']}\n")

        elif args.command == "project":
            proj = client.get_project(args.project_id)
            print(json.dumps(proj, indent=2, ensure_ascii=False))

        elif args.command == "summary":
            sum_data = client.get_project_summary(args.project_id)
            if args.raw:
                print(json.dumps(sum_data, indent=2, ensure_ascii=False))
            else:
                print(sum_data.get("markdown_prompt_context", ""))

        elif args.command == "analysis":
            res = client.get_analysis(
                project_id=args.project_id,
                status=args.status,
                room=args.room,
                query=args.query,
                limit=args.limit
            )
            notes = res.get("notes", [])
            print(f"Project: {res.get('project_name')} (Score: {res.get('overall_score')})")
            print(f"Matched findings: {res.get('total_matched')} (Showing {len(notes)}):\n" + "=" * 60)
            for n in notes:
                print(f"[{n.get('status')}] {n.get('title')} ({n.get('room_name', 'General')})")
                print(f"  Measured: {n.get('measured')} | Standard: {n.get('benchmark')}")
                if n.get('recommendation'):
                    print(f"  Fix: {n.get('recommendation')}")
                print("-" * 50)

        elif args.command == "spatial":
            metrics = client.get_spatial_metrics(args.project_id)
            print(json.dumps(metrics, indent=2, ensure_ascii=False))

        elif args.command == "compare":
            cmp_list = client.compare_projects(projects=args.projects)
            print("Project Comparison Table:\n" + "=" * 65)
            print(f"{'ID':<12} {'Score':<10} {'Pass Rate':<12} {'Checks':<8} {'Fails':<6} {'Warns':<6}")
            print("-" * 65)
            for row in cmp_list:
                print(f"{row['project_id']:<12} {str(row['score']):<10} {str(row['pass_rate_pct']) + '%':<12} {row['total_checks']:<8} {row['fail_count']:<6} {row['warn_count']:<6}")

        elif args.command == "context":
            ctx = client.get_ai_context(query=args.query, project_id=args.project_id)
            print(ctx.get("prompt_context", ""))

        elif args.command == "rules":
            res = client.list_rules(category=args.category, query=args.query, limit=15)
            print(f"Matched rules: {res.get('matched')} (out of {res.get('total_rules')} total):\n" + "=" * 60)
            for r in res.get("rules", []):
                print(f"[{r.get('rule_id')}] ({r.get('category')})")
                print(f"  {r.get('description_summary', '')}\n")

        elif args.command == "validate":
            res = client.validate_apartment_file(args.file)
            print(json.dumps(res, indent=2, ensure_ascii=False))

        elif args.command == "tools":
            spec = client.get_tools_spec()
            print(json.dumps(spec, indent=2, ensure_ascii=False))

    except ArchKnowAPIError as e:
        print(f"Error ({e.status_code}): {e.message}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"Connection Failed: {str(e)}", file=sys.stderr)
        print("Make sure the ArchiCheck server is running (`python server.py`).", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
