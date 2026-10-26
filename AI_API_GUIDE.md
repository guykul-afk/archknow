# 🤖 ArchiCheck (ArchKnow) — AI Integration & REST API Guide

מדריך מקיף לחיבור מערכות בינה מלאכותית חיצוניות (OpenAI ChatGPT, Custom GPTs, Claude Projects, LangChain, CrewAI, AutoGen, סוכנים אוטונומיים וסקריפטים) למערכת **ArchiCheck** לצורך ניתוח, תחקור והשוואת תוצאות בדיקה אדריכליות ותקנים סטטוטוריים.

---

## 🌟 מה ה-API מספק למערכות AI?

1. **תאימות מיידית ל-OpenAI Custom GPTs**: קובץ תקני `openapi.json` להגדרה בלחיצת כפתור אחת (Actions).
2. **סכמת כלי AI מוכנה מראש (`/api/v1/ai/tools`)**: הגדרות Function Calling מובנות ל-OpenAI ול-Anthropic Claude.
3. **סיכום מנהלים חסכוני בטוקנים (`/api/v1/projects/{id}/summary`)**: מחזיר טקסט Markdown מובנה ומסודר (ציון, כשלים סטטוטוריים FAIL, התראות איכות WARN והמלצות) לצריכה ישירה בתוך ה-Prompt ללא חריגה ממכסת הטוקנים.
4. **אורז הקשר חכם (`/api/v1/ai/context`)**: מנגנון RAG ממוקד שמקבל שאילתה ומחזיר רק את הממצאים והתקנים הרלוונטיים מוכנים להזרקה לפרומפט.
5. **מאגר של 400+ תקנים וחוקי תכנון (OKF)**: תקנות התכנון והבנייה בישראל, ת"י 1918 נגישות, תקני שטח בינלאומיים (UK NDSS, ADG, WBS), ארגונומיה (NKBA) ומדדי Space Syntax.
6. **מנוע אימות בזמן אמת (`/api/v1/analyze/plan`)**: אפשרות לשלוח נתוני דירה ב-JSON ולקבל פענוח איכות מיידי.
7. **ממשק Swagger UI אינטראקטיבי**: זמין בכתובת `/api/docs`.

---

## 🚀 כתובות קצה מרכזיות (Base URL: `http://localhost:5000/api/v1`)

| מתודה | Endpoint | תיאור |
|---|---|---|
| `GET` | `/health` | בדיקת תקינות המערכת, גרסה וכמות חוקים טעונים |
| `GET` | `/projects` | קטלוג 5 פרויקטי הדגל (`pines48`, `kkl10`, `hafetz44`, `yatkovski7`, `kitroni37`) |
| `GET` | `/projects/{id}` | פרופיל פרויקט, קומות, תוכניות (Sheets), מקטעים וציונים |
| `GET` | `/projects/{id}/summary` | **סיכום AI תמציתי ומובנה (Markdown + JSON)** |
| `GET` | `/projects/{id}/analysis` | שליפת ליקויים עם סינון לפי `status` (`FAIL`, `WARN`, `PASS`), `room`, `rule_id`, `q` |
| `GET` | `/projects/{id}/spatial-metrics` | מטריקות גיאומטריות, שטחים, חדרים וחיבוריות מרחבית |
| `GET` | `/compare` | השוואה רוחבית של פרויקטים (ציונים, אחוזי הצלחה, חריגות) |
| `POST` | `/ai/context` | חילוץ והזרקת קונטקסט לפי שאילתה טבעית עבור LLM |
| `GET` | `/rules` | חיפוש במאגר 400+ חוקי OKF ואדריכלות |
| `GET` | `/rules/{rule_id}` | פרטי תקן או חוק ספציפי (למשל `B1.13`) |
| `POST` | `/analyze/plan` | הרצת בדיקה חיה מול מנוע האימות על דירה חדשה ב-JSON |
| `GET` | `/ai/tools` | הגדרות Function Calling מוכנות ל-OpenAI ול-Claude |
| `GET` | `/openapi.json` | מפרט OpenAPI 3.1.0 מלא עבור Custom GPT Actions |
| `GET` | `/docs` (או `/api/docs`) | ממשק Swagger UI חי להתנסות בדפדפן |

---

## 🛠️ מדריך חיבור לפי פלטפורמה

### 1. חיבור ל-ChatGPT Custom GPT (OpenAI Actions)

כדי לתת ל-Custom GPT גישה ישירה לנתוני המערכת:

1. היכנס לעריכת ה-GPT שלך ב-OpenAI (`Explore GPTs` -> `Create / Edit GPT`).
2. תחת לשונית **Configure**, לחץ על **Create new action**.
3. לחץ על **Import from URL** והזן:
   ```text
   http://YOUR-HOST:5000/api/v1/openapi.json
   ```
   *(או העתק את תוכן ה-JSON מ-`/api/v1/openapi.json` והדבק בתיבת ה-Schema).*
4. בהגדרות ה-Authentication: בחר `None` (או `API Key` אם הגדרת משתנה סביבה `ARCHKNOW_API_KEY`).
5. בהוראות ה-GPT (Instructions), הוסף:
   > "You are an expert Architectural Quality Auditor. Use your connected ArchiCheck Actions to query projects, inspect statutory violations (FAIL), check design warnings (WARN), and fetch project summaries to answer user questions about architectural plans."

---

### 2. שימוש ב-Python עם OpenAI Function Calling

```python
import json
import requests
from openai import OpenAI

client = OpenAI()
BASE_URL = "http://localhost:5000/api/v1"

# 1. משוך את כלי ה-AI המוכנים מהמערכת
tools_resp = requests.get(f"{BASE_URL}/ai/tools").json()
openai_tools = tools_resp["openai_tools"]

# 2. שאלת משתמש
user_prompt = "מהן הבעיות המרכזיות ברוחב הממ״דים והמיסעה בפרויקט קק״ל 10?"

# 3. קריאה ל-OpenAI עם הכלים
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "אתה יועץ איכות תכנון ובנייה בישראל."},
        {"role": "user", "content": user_prompt}
    ],
    tools=openai_tools,
    tool_choice="auto"
)

# 4. ביצוע קריאת הכלי שהמודל בחר
tool_call = response.choices[0].message.tool_calls[0]
fn_name = tool_call.function.name
fn_args = json.loads(tool_call.function.arguments)

print(f"המודל החליט לקרוא לפונקציה: {fn_name} עם פרמטרים: {fn_args}")

if fn_name == "get_project_ai_summary":
    tool_res = requests.get(f"{BASE_URL}/projects/{fn_args['project_id']}/summary").json()
elif fn_name == "get_project_audit_notes":
    tool_res = requests.get(f"{BASE_URL}/projects/{fn_args['project_id']}/analysis", params=fn_args).json()
elif fn_name == "get_ai_architectural_context":
    tool_res = requests.post(f"{BASE_URL}/ai/context", json=fn_args).json()

print("תשובת הכלי התקבלה בהצלחה!")
```

---

### 3. חילוץ Prompt Context מהיר (RAG) לכל LLM (Claude, Llama, Gemini)

אם יש לך סוכן שרוצה לקבל קונטקסט ממוקד מבלי לנהל קריאות כלים מורכבות:

```python
import requests

# שולחים את השאלה ישירות לנקודת ה-Context
res = requests.post("http://localhost:5000/api/v1/ai/context", json={
    "query": "האם יש כשלים סטטוטוריים בפינס 48 או בעיות נגישות?",
    "project_id": "pines48",
    "max_items": 5
}).json()

prompt_context = res["prompt_context"]
print(prompt_context)
```
**תוצאה:** מחרוזת קומפקטית עם הממצאים, הערכים שנמדדו מול התקן וההמלצות, מוכנה להזרקה כ-System Context!

---

### 4. דוגמאות cURL

#### א. שליפת סיכום מנהלים לפרויקט
```bash
curl -X GET "http://localhost:5000/api/v1/projects/hafetz44/summary"
```

#### ב. סינון רק כשלים והתראות בחדר מסוים
```bash
curl -X GET "http://localhost:5000/api/v1/projects/kkl10/analysis?status=WARN,FAIL&room=ממ%22ד"
```

#### ג. השוואת 3 פרויקטים
```bash
curl -X GET "http://localhost:5000/api/v1/compare?projects=pines48,kkl10,kitroni37"
```

#### ד. בדיקה חיה של דירה חדשה ב-JSON
```bash
curl -X POST "http://localhost:5000/api/v1/analyze/plan" \
     -H "Content-Type: application/json" \
     -d '{
       "apartment_id": "apt_101",
       "bedrooms": 3,
       "net_area_sqm": 88.0,
       "global_parameters": {"ceiling_height_m": 2.50},
       "rooms": [
         {"room_name": "סלון", "area_sqm": 26.0, "depth_m": 5.4},
         {"room_name": "ממ\"ד", "area_sqm": 9.1, "depth_m": 2.60}
       ]
     }'
```

---

## 🔒 אבטחה ואימות (Authentication)

כברירת מחדל במצב פיתוח, ה-API פתוח לבקשות (`X-Auth-Mode: open`).  
להפעלת אבטחה בייצור:
1. הגדר משתנה סביבה במערכת:
   ```bash
   set ARCHKNOW_API_KEY=your_secret_api_key_here
   ```
2. שלח את המפתח בכל בקשה באחת משתי דרכים:
   - Header: `X-API-Key: your_secret_api_key_here`
   - Header: `Authorization: Bearer your_secret_api_key_here`
