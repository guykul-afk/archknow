# ArchiCheck (ArchKnow)

An end-to-end automated platform to analyze residential architectural plans against professional design guidelines.

## Features

- **Rule Parsing (OKF):** Parses structural codes, room requirements, and guidelines from professional textbooks into structured OKF (Open Knowledge Format) markdown files.
- **CAD Extraction (DXF):** Extracts room polygons, labels, and generates a spatial topology network from DXF files.
- **Validation Engine:**
  - **Quantitative Checks:** Validates dimensions, areas, and custom rule limits.
  - **Qualitative Analysis:** Uses an LLM to assess space adjacencies, functional layout, accessibility, and general livability based on topology and visual text rules.
- **Interactive UI:** A modern glassmorphism web dashboard to upload DXF plans, select rule sets, view a breakdown of violations, and get detailed AI feedback.

## Project Structure

- `okf_rules/` - Curated design rules structured in OKF.
- `cad_parser.py` - DXF parsing logic (via `ezdxf`).
- `validation_engine.py` - Local rule validation.
- `qualitative_analyzer.py` - AI qualitative validation.
- `server.py` - Flask web server.
- `webapp/` - Dashboard Frontend (HTML/CSS/JS).
- `generate_mock_dxf.py` - Generates a mock apartment DXF for testing.

## Getting Started

1. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r webapp/requirements.txt  # (or install flask, ezdxf, PyMuPDF, pyyaml, openai/google-genai depending on implementation)
   ```
2. Start the web application:
   ```bash
   python server.py
   ```
3. Open `http://localhost:5000` in your browser.


## Knowledge Base & Engine v2

### New knowledge files (`okf_rules/`)
| Rule ID | File | Content |
| :--- | :--- | :--- |
| `WBS_NDSS_ADG` | `wbs_ndss_adg_housing_benchmarks.md` | UK NDSS space standard, London Plan D6, NSW ADG, Swiss WBS (structure) |
| `NKBA_KB` | `nkba_kitchen_bath_planning_guidelines.md` | NKBA kitchen & bath ergonomics (work triangle, aisles, landing areas, fixture clearances) |
| `APL_HOUSING` | `alexander_pattern_language_housing.md` | 29 dwelling-scale patterns from *A Pattern Language* |
| `SPACE_SYNTAX_SAGA` | `space_syntax_saga_metrics.md` | Space Syntax depth/integration, corridor ratio, rectangularity, SAGA proxies |
| `IS1918_ACCESS` | `israel_accessibility_is1918_housing.md` | Accessibility framework; reference values **pending verification** against IS 1918 |
| `SOURCES_REGISTRY` | `sources_registry_architectural_quality.md` | Every recommended source and its integration status |

Numeric thresholds live in each file's YAML frontmatter; `validation_engine.py` reads them via `get_rule_param()`
(mirrored in `ADVANCED_FALLBACKS`). Editing a value in the knowledge file changes the engine's behaviour.

### Result statuses
- `FAIL` — Israeli statutory requirement not met (unchanged legacy checks).
- `WARN` — below an international benchmark / best practice, or required data is missing. Advanced checks never emit `FAIL`.
- `PASS` — requirement met (also used for informational metrics such as integration ranking).

### Optional apartment fields used by v2 checks
Each check runs only when its data exists:
`topology` (+ `EXT` edge or `entrance_room_id`), `orientations`, `storage.built_in_sqm` / `storage.volume_m3`,
`rooms[].polygon`, `rooms[].window_area_sqm`, `rooms[].depth_m`, `rooms[].kitchen_layout`, `rooms[].fixtures`,
balcony rooms with `depth_m` / `threshold_cm`, `accessible_unit`, `net_area_sqm`, `bedrooms`, `bedspaces`.
See `pines48_apt_c_sample.json` for a complete example.

### Commands
```bash
python validation_engine.py pines48_apt_c_sample.json        # full report (apartment or project file)
python qualitative_analyzer.py pines48_apt_c_sample.json out.txt [--apartment N]
python test_advanced_checks.py                               # test suite
```
After changing the engine or rules, copy `validation_engine.py` and `okf_rules/` into `functions/` before deploying.
