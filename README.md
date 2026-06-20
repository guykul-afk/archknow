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
