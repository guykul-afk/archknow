# Architectural & BIM Dimensional Extraction Report (Verified QA Revision)
**Project:** Keren Kayemet LeYisrael (KKL) 10, Petah Tikva (`קק"ל 10, פתח תקווה`)  
**Architect:** Eyal Sendrowitz Architects Ltd. (`אייל סנדרוביץ אדריכלים`)  
**Lot Details:** Gush 6386, Helka 198, Lot Area: $862.00\text{ m}^2$  
**Coordinate Origin $(0,0,0)$:** South-West exterior corner of the main above-ground building structural footprint at $\pm 0.00 = +59.53\text{ m}$ (Absolute Elevation).  
- **$+X$ Axis:** West $\rightarrow$ East (Main Building Width $= 12.73\text{ m}$; Basement Width $= 19.55\text{ m}$ from $X = -3.41\text{ m}$ to $+16.14\text{ m}$)
- **$+Y$ Axis:** Vertical Elevation in meters relative to $\pm 0.00$ ($-9.07\text{ m}$ Foundation to $+31.40\text{ m}$ Upper Parapet)
- **$+Z$ Axis:** South $\rightarrow$ North (`רחוב קרן קיימת לישראל` Street Frontage at North; Main Building Length $= 33.09\text{ m}$; Basement Length $= 39.71\text{ m}$ from $Z = -3.60\text{ m}$ to $+36.11\text{ m}$)

---

## 1. Zero-Trust Architectural & Section QA Audit (בדיקת התאמה אדריכלית מלאה וחתכים)

Following a full cross-check of the Garmoshka **East Elevation (`חזית מזרחית`)**, **West/North/South Elevations**, **Sections 1-1 & 2-2 (`חתך 1-1, 2-2`)**, and **Sales Plans (Sheets 2–22)**, the following critical volumetric, section, and facade discrepancies were identified and resolved in the 3D BIM model:

| # | Architectural Zone | Discrepancy in v1 Model | Exact Garmoshka / Section Reality (Fixed in v2) |
| :- | :--- | :--- | :--- |
| **1** | **Floors 1–2 vs. Floor 3 (North Facade & Section)** | In v1, the North-West wall was pushed back by $1.72\text{ m}$ (`zNorthWest = 31.37m`) starting at Floor 3, creating a false step in the main building wall. | **Main exterior North wall (`Z = 33.09m`) is continuous from Ground (L0) through Floor 7!** What changes between Floors 1–2 (`Apt C`) and Floors 3–7 (`Apt D, G, H`) is **only the cantilevered balcony**:<br>• **Floors 1–2 (`Apt C`):** Full-width cantilevered balcony ($11.50\text{ m}$ inner / $11.93\text{ m}$ outer, $X \in [0.40, 12.33]$, $Z \in [33.09, 34.81]$, $22.80\text{ m}^2$).<br>• **Floor 3 (`Apt D`):** Enclosed apartment still reaches $Z = 33.09\text{ m}$. Cantilevered balcony shifts to the **East half only** ($5.56\text{ m} \times 1.73\text{ m}$, $X \in [6.37, 12.33]$, $Z \in [33.09, 34.82]$). The exposed **West half** of Floor 2's balcony slab below ($X \in [0.40, 6.37]$, $Z \in [33.09, 34.81]$) has a perimeter parapet/railing at $+10.50\text{ m}$. |
| **2** | **Floor 1 vs. Ground Floor (North Lobby & Transformer Room)** | Ground floor (`L0`) was modeled flush with $Z = 33.09\text{ m}$ all across. | On Ground Floor (`L0`), the **North-East corner** features a glazed **Lobby & Transformer Room (`חדר טרפו / לובי כניסה`)** with a $50\text{ cm}$ thick transformation ceiling slab (`תקרת טרנספורמציה H=50`) and recessed entrance colonnade under Floor 1 (`Z = 28.50m to 33.09m`). Floor 1 cantilevers over the North-West pedestrian entrance area. |
| **3** | **Floors 3–4 vs. Floor 5 vs. Floors 6–7 (South-East Facade Step)** | South-East wall was modeled at $Z = 0.00\text{ m}$ uniformly on all floors L1–L7. | Looking at the **East Elevation (Left side = South)** and Plans L3-4 (`Apt E`), L5 (`Apt F`), and L6-7 (`Apt A`):<br>• **Floors 1–2 (`Apt A`, $116\text{ m}^2$):** South-East bedroom wall is at $Z = 0.00\text{ m}$ (with $1.80\text{ m}$ balcony to $Z = -1.80\text{ m}$).<br>• **Floors 3–4 (`Apt E`, $131\text{ m}^2$, 5-room):** An extra South-East bedroom (`ח. שינה 1`, $2.84 \times 3.60\text{ m}$) projects southward on the East side!<br>• **Floor 5 (`Apt F`, $124.2\text{ m}^2$):** Slightly shorter SE room ($3.19\text{ m}$ vs $3.60\text{ m}$), creating a terrace step at $+19.95\text{ m}$.<br>• **Floors 6–7 (`Apt A`, $116\text{ m}^2$):** Reverts to the 4-room layout; the exposed roof of Floor 5's SE room forms a **side terrace with railing & pergola beam on Floor 6** (`מרפסת קומה 5/6`). |
| **4** | **Floor 8 (Penthouse) & Technical Roof (`קומת גג +29.90 / +31.40`)** | Roof was modeled with a protruding beige box (`31.40m`) and sloped blue solar triangles sitting on top of the parapet. | Per **East Elevation & Sections 1-1 / 2-2**:<br>• **Floor 8 (`+26.50m` to `+29.90m`):** Set back on the **South** by $2.86\text{ m}$ ($Z = 2.86\text{ m}$) and on the **North** by $2.86\text{ m}$ ($Z = 30.23\text{ m}$), leaving an enclosed length of $28.48\text{ m}$ (`2848` in Garmoshka).<br>• **South & North Penthouse Terraces (`+26.50m`):** Topped by **Aluminum Pergolas (`פרגולת אלומיניום H=350`)** reaching $+30.00\text{ m}$, framed by the perimeter decorative beams.<br>• **Technical Roof (`+29.90m` to `+31.40m`):** The **entire 28.48 m building mass** continues up to a clean, flat horizontal white parapet wall at **$+31.40\text{ m}$** ($H = 1.50\text{ m}$ above the $+29.90\text{ m}$ roof slab). The stairwell/elevator core (`+31.30\text{ m}`) and low-profile solar collectors (`קולטי שמש`) sit **inside** the $1.50\text{ m}$ parapet walls so they do not protrude above $+31.40\text{ m}$ on the East/West elevations! |
| **5** | **East & West Facade Fenestration & 2-Story Dark Window Channels (`C`)** | v1 had only 3 generic window columns and 2 wide louver bays. | Per the **East Elevation (`חזית מזרחית קנ"מ 1:100`)**, the facade is rigorously organized into **9 distinct vertical bays** from South (Left) to North (Right) with **2-story grouped dark anthracite frames (`C`)** spanning Floors 1–2, 3–4, 5–6, and 7–8:<br>1. **South Balconies** ($1.80\text{ m}$ projection)<br>2. **Bay 1 (South Pier):** Single vertical window strip in white wall (`E`)<br>3. **Bay 2 (South-Mid):** 2-story dark frame (`C`) with paired windows (`A`)<br>4. **Bay 3 (Mamad Tower):** Continuous dark vertical recessed slot (`C`) with $1.00 \times 1.00\text{ m}$ Mamad blast windows<br>5. **Bay 4 (Central Service Shaft):** Continuous full-height **Aluminum Louver Screen (`D` - מסתור כביסה)** from Ground (`L0`) to Floor 8<br>6. **Bay 5 (Center-North):** 2-story dark frame (`C`) with twin bedroom windows<br>7. **Bay 6 (North-Mid):** 2-story dark frame (`C`) with paired windows (`A`)<br>8. **Bay 7 (North Pier):** Single vertical window column (Floors 1–7, stepped at Floor 8)<br>9. **North Balconies** (Full width L1–L2, East-half L3–L7, Pergola Terrace L8) |
| **6** | **Subterranean Section (`מרתף 1- / 2-`)** | Simplified flat slabs without the stepped ground garden slab or water tank pit walls. | Per **East Elevation & Section 1-1**:<br>• **Ground Courtyard Step:** South side slab is dropped to $-0.80\text{ m}$ (`ע.ש מרתפים 0.80 מ'`) with a $50\text{ cm}$ drop beam (`H=50`), stepping up to $\pm 0.00$ at the central entrance.<br>• **East Vehicle Ramp:** Descends from North-East street entry ($\pm 0.00$) southward along the East wall ($7.5\% \rightarrow 15\% \rightarrow 7.5\%$) down to Basement -1 ($-4.35\text{ m}$).<br>• **West Internal Ramp:** Descends from Basement -1 ($-4.38\text{ m}$) to Basement -2 ($-7.65\text{ m}$).<br>• **Deep Water Tank & Pump Pit (`חדר מאגר מים 15 קוב + חדר משאבות`):** Dropped pit in the center-north of Basement -2 down to $-8.62\text{ m}$ / $-9.07\text{ m}$ foundation bottom. |

---

## 2. Complete Vertical Datum & Floor-to-Floor Schedule (חתכים 1-1, 2-2)

| Level Name | Hebrew Label | Structural Slab (`פ.ב`) [m] | Finished Floor (`פ.ר`) [m] | Absolute Elev. [m] | Floor-to-Floor Height [m] | Clear Ceiling Height [m] | Architectural Envelope Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Foundation Bottom** | תחתית רפסודה | $-9.07$ | — | $+50.46$ | — | — | Under Water Tank & Pump Room (`50 ס"מ` mat) |
| **Water Tank Pit** | מאגר מים / משאבות | $-8.62\text{ / }-8.75$ | $-8.57$ | $+50.91$ | $1.10$ | $2.50$ | $15\text{ m}^3$ tank ($6.15 \times 3.05\text{ m}$) + $15\text{ m}^2$ pump room |
| **Basement -2** | קומת מרתף 2- | $-7.65$ | $-7.50$ | $+51.88$ | $3.30$ | $2.40 - 2.78$ | $18$ parking spaces + $6$ storage units ($793\text{ m}^2$) |
| **Basement -1** | קומת מרתף 1- | $-4.35$ | $-4.55$ | $+55.18$ | $4.35$ | $2.40 - 3.66$ | $16$ parking spaces + $8$ storage units ($793\text{ m}^2$) |
| **Ground Floor (L0)** | קומת קרקע (0) | $\pm 0.00$ | $-0.03\text{ / }-0.20$ | $+59.53$ | $4.20$ | $3.83$ | Lobby, Transformer room (`תקרת טרפו`), Garden Apts `G-1`, `G-2` |
| **Floor 1** | קומה 1 | $+4.20$ | $+4.05$ | $+63.73$ | $3.15$ | $2.78$ | Apts `A`, `B`, `C` (Full-width North balcony $22.8\text{ m}^2$) |
| **Floor 2** | קומה 2 | $+7.35$ | $+7.20$ | $+66.88$ | $3.15$ | $2.78$ | Apts `A`, `B`, `C` (Full-width North balcony $22.8\text{ m}^2$) |
| **Floor 3** | קומה 3 | $+10.50$ | $+10.35$ | $+70.03$ | $3.15$ | $2.78$ | Apts `E` (5-rm SE ext.), `B`, `D` (East-half North balcony $12\text{ m}^2$) |
| **Floor 4** | קומה 4 | $+13.65$ | $+13.50$ | $+73.18$ | $3.15$ | $2.78$ | Apts `E` (5-rm SE ext.), `B`, `D` (East-half North balcony $12\text{ m}^2$) |
| **Floor 5** | קומה 5 | $+16.80$ | $+16.65$ | $+76.33$ | $3.15$ | $2.78$ | Apts `F`, `B`, `G` (SE bedroom step at top of L5) |
| **Floor 6** | קומה 6 | $+19.95$ | $+19.80$ | $+79.48$ | $3.15$ | $2.78$ | Apts `A` (4-rm SE setback), `B`, `H` |
| **Floor 7** | קומה 7 | $+23.10$ | $+22.95$ | $+82.63$ | $3.40$ | $3.03$ | Apts `A`, `B`, `H` (High ceiling $3.40\text{ m}$ floor-to-floor) |
| **Floor 8 (Penthouse)**| קומה 8 (פנטהאוז) | $+26.50$ | $+26.35$ | $+86.03$ | $3.40$ | $2.95$ | `PH-1` (North) & `PH-2` (South), $28.48\text{ m}$ enclosed length + $H=3.50\text{ m}$ Pergolas |
| **Technical Roof (L9)**| קומת גג (9) | $+29.90$ | $+29.67$ | $+89.43$ | $1.50$ | — | Flat roof slab at $+29.90\text{ m}$; Stair/Elevator core to $+31.30\text{ m}$ |
| **Upper Roof Parapet**| מעקה גג עליון | $+31.40$ | — | $+90.93$ | — | — | Continuous perimeter parapet wall ($H = 1.50\text{ m}$) concealing roof equipment |

---

## 3. Floor-by-Floor Envelope & Balcony Geometry (1:1 Metric Coordinates)

### 3.1 Main Building Structural Footprint ($X \in [0.00\text{ m}, 12.73\text{ m}]$, $Z \in [0.00\text{ m}, 33.09\text{ m}]$)
- **Ground Floor (`L0`, $0.00\text{ m} \rightarrow +4.20\text{ m}$):**
  - South Garden Apartments (`G-1` West, `G-2` East): $Z = 0.00\text{ m}$ to $Z = 18.20\text{ m}$. Overhung on the South by a decorative perimeter concrete frame beam (`קורה דקורטיבית`) at $+3.83\text{ m} \rightarrow +4.20\text{ m}$ ($Z \in [-1.80, 0.00]$).
  - Central Core & Service Rooms (`חדר אשפה, חדר גז, חדר אופניים ועגלות`): $Z = 18.20\text{ m}$ to $Z = 27.50\text{ m}$.
  - North-East Double-Height Glazed Lobby & Transformer Zone (`לובי כניסה + חדר טרפו`): $X \in [6.00, 12.73]$, $Z \in [25.50, 32.20]$, featuring the large 4-bay curtain wall (`A`) visible on the right side of the East Elevation, plus a structural corner column at $Z = 33.09\text{ m}$ supporting Floor 1 above.
- **Floors 1 & 2 (`L1–L2`, $+4.20\text{ m} \rightarrow +10.50\text{ m}$):**
  - **Main Enclosed Envelope:** Full $12.73\text{ m} \times 33.09\text{ m}$, except on the South-East (`Apt A` bedroom wing, $X \in [6.84, 12.73]$) where the North-South length is $3.60\text{ m}$ shorter at the rear notch, and **Full-Width North Balcony (`Apt C`)** spanning $X \in [0.40, 12.33]$, $Z \in [33.09, 34.81]$ ($11.50\text{ m} \times 1.72\text{ m}$ clear, $22.80\text{ m}^2$).
  - **South Twin Balconies (`Apt B` & `Apt A`):** Two $5.70\text{ m} \times 1.80\text{ m}$ balconies ($Z \in [-1.80, 0.00]$) separated by a $190.2\text{ cm}$ frosted glass privacy divider at $X = 6.36\text{ m}$.
- **Floors 3 & 4 (`L3–L4`, $+10.50\text{ m} \rightarrow +16.80\text{ m}$):**
  - **North Balcony Shift (`Apt D`):** Main North wall remains at $Z = 33.09\text{ m}$. The cantilevered balcony is now on the **East half only** ($X \in [6.37, 12.33]$, $Z \in [33.09, 34.82]$, $5.56\text{ m} \times 1.73\text{ m} = 12.00\text{ m}^2$). On Floor 3 (`+10.50m`), the exposed West half of Floor 2's balcony below ($X \in [0.40, 6.37]$, $Z \in [33.09, 34.81]$) forms a roof terrace / ledge with glass parapet and aluminum pergola beam (`פרגולת אלומיניום`).
  - **South-East 5-Room Extension (`Apt E`):** Full $33.09\text{ m}$ length on both East and West sides.
- **Floor 5 (`L5`, $+16.80\text{ m} \rightarrow +19.95\text{ m}$):**
  - **North (`Apt G`):** Same East-half cantilevered balcony ($X \in [6.37, 12.33]$, $Z \in [33.09, 34.82]$).
  - **South (`Apt B` & `Apt F`):** Twin South balconies ($Z \in [-1.80, 0.00]$).
- **Floors 6 & 7 (`L6–L7`, $+19.95\text{ m} \rightarrow +26.50\text{ m}$):**
  - **North (`Apt H`):** Same East-half cantilevered balcony ($X \in [6.37, 12.33]$, $Z \in [33.09, 34.82]$).
  - **South (`Apt B` & `Apt A`):** Twin South balconies; Floor 7 has an increased floor-to-floor height of **$3.40\text{ m}$** ($+23.10\text{ m}$ to $+26.50\text{ m}$).
- **Floor 8 — Penthouse Level (`L8`, $+26.50\text{ m} \rightarrow +29.90\text{ m}$):**
  - **Setback Enclosed Footprint:** Length $= 28.48\text{ m}$ (`2848` in Garmoshka), spanning from **$Z = 1.75\text{ m}$ (South setback)** to **$Z = 30.23\text{ m}$ (North setback)**.
  - **South Penthouse Terrace (`PH-2`, $29.80\text{ m}^2$):** Spans from $Z = -1.80\text{ m}$ (cantilever) to $Z = +1.75\text{ m}$ (setback wall), covered by an **Aluminum Pergola (`H = 3.50m`, top at `+30.00m`)**.
  - **North Penthouse Terrace (`PH-1`, $44.00\text{ m}^2$):** Spans full building width from $Z = 30.23\text{ m}$ to $Z = 33.09\text{ m}$ (plus the East cantilevered balcony zone to $Z = 34.82\text{ m}$), covered by an **Aluminum Pergola (`H = 3.50m`, top at `+30.00m`)**.
- **Technical Roof (`L9`, $+29.90\text{ m} \rightarrow +31.40\text{ m}$):**
  - Enclosed by a continuous $1.50\text{ m}$ high perimeter parapet wall from $Z = 1.75\text{ m}$ to $Z = 30.23\text{ m}$ (top at **$+31.40\text{ m}$**).
  - Central Stair & Elevator Overrun (`פיר מעליות וחדר מדרגות`) reaches $+31.30\text{ m}$ (flush with/below the $+31.40\text{ m}$ parapet line on the East & West elevations).
  - Low-profile solar collector banks (`קולטי שמש`) and emergency generator (`גנרטור`) are mounted on the $+29.90\text{ m}$ roof deck **below** the $+31.40\text{ m}$ parapet line.
