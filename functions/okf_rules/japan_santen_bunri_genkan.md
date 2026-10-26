---
category: International Ergonomics & Typology
subcategory: Japanese Contemporary Housing — San-ten Bunri & Genkan
description_summary: Japanese architectural ergonomics — San-ten Bunri (3-point separation of toilet cubicle, washstand/laundry dressing room, and wet bath/shower for simultaneous family use) and Genkan entry dirt-lock threshold.
indicator: San-ten Bunri 3-Point Wet Separation & Genkan Entry Threshold
rule_id: JPN_SB_1
type: architectural_rule
check_type: wet_room_separation
target_room: bathroom
engine_usage: validation_engine.run_advanced_checks
japan_genkan_min_depth_m: 1.05
japan_genkan_shoe_cabinet_depth_m: 0.38
japan_santen_toilet_min_width_m: 0.80
japan_santen_toilet_min_length_m: 1.30
japan_santen_washstand_min_width_m: 0.90
---
# JPN_SB_1: ארגונומיה יפנית — *San-ten Bunri* (הפרדה משולשת של החלל הרטוב) ו-*Genkan*

## מקור תכנוני
- Japanese Architectural Standard Specification (JASS) & תכנון דירות מגורים עכשווי ביפן.

## עקרונות ומדדים לניתוח תכנוני
1. ***San-ten Bunri* (三点分離 — הפרדת 3 נקודות רטובות)**:
   - בדירות משפחתיות (או דירות עם חדר רחצה יחיד), שילוב האסלה, הכיור והמקלחת בחדר אחד גורם ל"נעילת" השירותים והכיור בזמן שאחד מבני הבית מתקלח, ולחשיפת אזור ההתארגנות לאדים ורטיבות.
   - **הפרדה ל-3 תאים עצמאיים**:
     1. **תא אסלה נפרד (WC)**: רוחב $\ge \mathbf{0.80\text{ m}}$ $\times$ אורך $\ge \mathbf{1.30\text{ m}}$ עם כיור נטילת ידיים.
     2. **מבואת כיור, התלבשות וכביסה יבשה (*Senmenjo*)**: רוחב $\ge \mathbf{0.90\text{ m}}$.
     3. **חדר רחצה רטוב (*Ofuro* — מקלחת ואמבטיה)**: $\ge \mathbf{1.20 \times 1.60\text{ m}}$ סגור בדלת אטומה לאדים.
2. ***Genkan* (玄関 — מבואת כניסה וארון נעליים)**:
   - עומק מבואת כניסה פנוי $\ge \mathbf{1.05\text{–}1.20\text{ m}}$ מדלת הכניסה, בשילוב נישה לארון נעליים/מעילים בעומק $\mathbf{35\text{–}40\text{ cm}}$.
