document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    const btnAnalyze = document.getElementById('btn-analyze');
    const blueprintViewer = document.getElementById('blueprint-viewer');
    const checklistContainer = document.getElementById('checklist-container');
    const aiInsightsContainer = document.getElementById('ai-insights-container');
    
    const projectNavigator = document.getElementById('project-navigator');
    const floorSelect = document.getElementById('floor-select');
    const aptSelect = document.getElementById('apt-select');
    
    let selectedFile = null;
    let projectData = null;
    
    // Initialize Firebase (Production / Cloud Mode)
    let firestoreDb = null;
    let firebaseStorage = null;

    fetch('/__/firebase/init.json')
    .then(async response => {
        const config = await response.json();
        firebase.initializeApp(config);
        firestoreDb = firebase.firestore();
        firebaseStorage = firebase.storage();
        console.log("Firebase initialized successfully in Cloud Mode.");
    })
    .catch((err) => {
        console.warn("Could not load Firebase init config. Running in Local Mode (server.py required).");
    });

    // Click to select file
    uploadZone.addEventListener('click', (e) => {
        if (e.target !== btnAnalyze) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (fileInput.files.length > 0) {
            handleFileSelection(fileInput.files[0]);
        }
    });

    // Handle Drag & Drop visually
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.style.borderColor = 'var(--accent-blue)';
        uploadZone.style.background = 'rgba(0, 225, 255, 0.05)';
    });

    uploadZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadZone.style.borderColor = 'var(--panel-border)';
        uploadZone.style.background = 'transparent';
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    function handleFileSelection(file) {
        selectedFile = file;
        uploadZone.style.borderColor = 'var(--success)';
        uploadZone.style.background = 'rgba(0, 210, 106, 0.05)';
        uploadZone.querySelector('p').innerText = `קובץ נבחר: ${file.name}`;
        btnAnalyze.style.display = 'block';
    }

    // API Call (Firebase Cloud Mode or Local Mode fallback)
    btnAnalyze.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent triggering fileInput click
        
        if (!selectedFile) return;

        const isPdf = selectedFile.name.toLowerCase().endsWith('.pdf');
        btnAnalyze.innerText = isPdf
            ? 'מנתח את קובץ ה-PDF: קריאת גיליון, קירות, פתחים וחללים (עשוי להימשך כמה דקות בפעם הראשונה)...'
            : 'מפענח ומנתח שרטוט (זה עשוי לקחת מספר שניות)...';
        btnAnalyze.disabled = true;

        if (firestoreDb && firebaseStorage) {
            // Cloud Mode: Upload to Firebase Storage and listen to Firestore
            const fileId = Date.now() + "_" + Math.random().toString(36).substr(2, 9);
            const storageRef = firebaseStorage.ref(`uploads/${fileId}.pdf`);
            
            console.log(`Cloud Mode: Uploading PDF to storage with ID: ${fileId}...`);
            storageRef.put(selectedFile)
            .then(() => {
                console.log("PDF uploaded to Firebase Storage successfully. Waiting for Cloud Function analysis...");
                
                // Set up a listener on Firestore for the analysis results
                const unsubscribe = firestoreDb.collection("projects").doc(fileId)
                .onSnapshot((doc) => {
                    if (doc.exists) {
                        const data = doc.data();
                        console.log("Firestore update received:", data);
                        
                        if (data.status === 'success') {
                            unsubscribe();
                            // New pipeline stores the full project as JSON; older docs are flat
                            projectData = data.project_json ? JSON.parse(data.project_json) : data.project ? data.project : {
                                project_name: data.project_name,
                                bg_image_url: data.bg_image_url,
                                floors: [{
                                    floor_name: "קומה מתוך PDF",
                                    apartments: [{
                                        apartment_id: "דירת PDF מנותחת",
                                        rooms: data.rooms,
                                        topology: data.topology,
                                        accessibility: data.accessibility,
                                        validation_results: data.validation_results
                                    }]
                                }]
                            };
                            
                            uploadZone.style.display = 'none';
                            projectNavigator.classList.remove('hidden');
                            blueprintViewer.classList.remove('hidden');
                            populateFloors();
                        } else if (data.status === 'error') {
                            unsubscribe();
                            alert(`שגיאה בניתוח הקובץ:\n${data.error}`);
                            btnAnalyze.innerText = 'הרץ מנוע אנליזה';
                            btnAnalyze.disabled = false;
                        }
                    }
                });
            })
            .catch(err => {
                console.error("Storage upload failed:", err);
                alert(`שגיאה בהעלאת הקובץ לענן:\n${err.message}`);
                btnAnalyze.innerText = 'הרץ מנוע אנליזה';
                btnAnalyze.disabled = false;
            });
        } else {
            // Local Mode Fallback
            console.log("Local Mode: Falling back to local backend server.py...");
            const formData = new FormData();
            formData.append('file', selectedFile);

            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(async (res) => {
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.error || 'שגיאה בעיבוד הקובץ');
                }
                return data;
            })
            .then(data => {
                projectData = data;
                uploadZone.style.display = 'none';
                projectNavigator.classList.remove('hidden');
                blueprintViewer.classList.remove('hidden');
                
                populateFloors();
            })
            .catch(err => {
                console.error(err);
                alert(`שגיאה:\n${err.message}`);
                btnAnalyze.innerText = 'הרץ מנוע אנליזה';
                btnAnalyze.disabled = false;
            });
        }
    });

    function populateFloors() {
        floorSelect.innerHTML = '';
        if (projectData && projectData.floors) {
            projectData.floors.forEach((floor, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.text = floor.floor_name;
                floorSelect.appendChild(opt);
            });
            populateApartments();
        }
    }

    floorSelect.addEventListener('change', populateApartments);

    function populateApartments() {
        aptSelect.innerHTML = '';
        const floorIdx = floorSelect.value;
        const floor = projectData.floors[floorIdx];
        
        if (floor && floor.apartments) {
            floor.apartments.forEach((apt, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.text = apt.apartment_id;
                aptSelect.appendChild(opt);
            });
            renderApartment();
        }
    }
    
    aptSelect.addEventListener('change', renderApartment);

    function renderApartment() {
        const floorIdx = floorSelect.value;
        const aptIdx = aptSelect.value;
        const floor = projectData.floors[floorIdx];
        const apt = floor.apartments[aptIdx];
        
        if (apt) {
            const img = document.getElementById('blueprint-img');
            const bg = floor.bg_image_url || projectData.bg_image_url;
            if (bg) {
                img.src = bg;
            } else {
                img.src = '';
            }
            renderChecklist(apt.validation_results || []);
            renderAIInsights(apt.qualitative_insights || []);
            renderBlueprint(apt.rooms || [], apt.validation_results || []);
            renderPolygons(apt.rooms || []);
            renderDimensionsTable(apt.rooms || []);
            renderExtraction(apt, projectData);
        }
    }

    // ---------- Smart PDF extraction (plan_analyzer) ----------
    const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));

    function renderPolygons(rooms) {
        const svg = document.getElementById('blueprint-polygons');
        if (!svg) return;
        svg.innerHTML = '';
        rooms.forEach((r, idx) => {
            if (!r.polygon_pct || r.polygon_pct.length < 3) return;
            const p = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
            p.setAttribute('points', r.polygon_pct.map(([x, y]) => `${x},${y}`).join(' '));
            p.setAttribute('class', `type-${r.type || 'room'}`);
            p.id = `room-poly-${idx}`;
            const t = document.createElementNS('http://www.w3.org/2000/svg', 'title');
            t.textContent = `${r.name} — ${r.area_sqm} מ"ר`;
            p.appendChild(t);
            svg.appendChild(p);
        });
    }

    const toggle = document.getElementById('toggle-polygons');
    if (toggle) {
        toggle.addEventListener('change', () => {
            document.getElementById('blueprint-polygons').classList.toggle('hidden', !toggle.checked);
        });
    }

    function metaItem(label, value, src) {
        if (value === undefined || value === null || value === '' || (Array.isArray(value) && !value.length)) return '';
        return `<div class="meta-item"><div class="meta-label">${esc(label)}</div>
                <div class="meta-value">${esc(Array.isArray(value) ? value.join(', ') : value)}</div>
                ${src ? `<div class="meta-src">${esc(src)}</div>` : ''}</div>`;
    }

    function renderExtraction(apt, project) {
        const panel = document.getElementById('extraction-panel');
        const ex = apt.plan_extraction;
        if (!panel) return;
        if (!ex) { panel.classList.add('hidden'); return; }
        panel.classList.remove('hidden');
        const sh = ex.sheet || {}, cal = ex.calibration || {}, a = ex.apartment || {};
        const calTxt = cal.median_error_pct != null
            ? `אומת מול ${cal.matched_dimensions}/${cal.total_dimensions} מידות (סטייה ${cal.median_error_pct}%)`
            : (cal.scale_source || '');
        const srcLabel = {vision: 'קריאת Vision', text_layer: 'שכבת טקסט', 'text_layer+vision': 'טקסט + Vision'}[ex.reading_source] || ex.reading_source;
        document.getElementById('extraction-meta').innerHTML = [
            metaItem('פרויקט', [sh.project_name, sh.city].filter(Boolean).join(', '), srcLabel),
            metaItem('קומות', sh.floors_text || (sh.floors || []).join(', ')),
            metaItem('דירות', sh.apartment_numbers),
            metaItem('קנה מידה', cal.scale, calTxt),
            metaItem('שטח מוצהר', a.declared_area_sqm ? `${a.declared_area_sqm} מ"ר` : null, 'טבלת שרטוט'),
            metaItem('שטח פנים נטו', a.net_interior_area_sqm ? `${a.net_interior_area_sqm} מ"ר` : null, 'נמדד מגאומטריה'),
            metaItem('שטח מרפסות', a.outdoor_area_sqm ? `${a.outdoor_area_sqm} מ"ר` : null),
            metaItem('חדרים (מוצהר / זוהה)', `${a.declared_rooms ?? '—'} / ${a.rooms_count_measured ?? '—'}`),
            metaItem('חדרי שינה (כולל ממ"ד)', a.bedrooms),
            metaItem('דלת כניסה', a.main_entrance_width_cm ? `${a.main_entrance_width_cm} ס"מ` : 'לא זוהתה'),
            metaItem('כיווני אוויר', a.orientations && a.orientations.length ? a.orientations : 'ללא חץ צפון'),
            metaItem('פתחים', Object.entries(ex.openings_summary || {}).map(([k, v]) => `${k}: ${v}`)),
        ].join('');
        const qa = ex.qa || [];
        document.getElementById('extraction-qa').innerHTML = qa.map(item => {
            const cls = item.status === 'PASS' ? 'pass' : (item.status === 'WARN' ? 'warn' : 'fail');
            const icon = item.status === 'PASS' ? '✓' : (item.status === 'WARN' ? '!' : '✗');
            return `<div class="checklist-item"><div class="status-icon status-${cls}">${icon}</div>
                    <div class="rule-info"><div class="rule-name">${esc(item.check)} <span class="tag tag-${cls}">${item.status}</span></div>
                    <div class="rule-desc">${esc(item.message)}</div></div></div>`;
        }).join('') || '<div class="placeholder-state">אין בדיקות</div>';
        const warns = (ex.warnings || []).concat(project.warnings || []);
        document.getElementById('extraction-warnings').innerHTML = warns.map(w => `<div>⚠️ ${esc(w)}</div>`).join('');
    }

    function renderBlueprint(rooms, validationResults) {
        const overlay = document.getElementById('blueprint-overlay');
        overlay.innerHTML = ''; // Clear previous elements
        
        rooms.forEach((r, idx) => {
            if (r.x_pct !== undefined && r.y_pct !== undefined) {
                // Highlight glow element (back layer)
                const highlightGlow = document.createElement('div');
                highlightGlow.className = 'room-highlight-glow';
                highlightGlow.id = `room-highlight-${idx}`;
                highlightGlow.style.left = r.x_pct + '%';
                highlightGlow.style.top = r.y_pct + '%';
                
                // Info icon container
                const iconDiv = document.createElement('div');
                iconDiv.className = 'info-icon-node';
                iconDiv.id = `room-icon-${idx}`;
                iconDiv.style.left = r.x_pct + '%';
                iconDiv.style.top = r.y_pct + '%';
                iconDiv.style.pointerEvents = 'auto'; // enable mouse interaction
                iconDiv.innerHTML = 'ℹ️';

                // Check for failures
                const roomFailures = (validationResults || []).filter(f => f.status === 'FAIL' && f.element.includes(r.name));
                if (roomFailures.length > 0) {
                    iconDiv.classList.add('has-error');
                }

                // Smart Card
                const card = document.createElement('div');
                card.className = 'smart-card';
                card.id = `room-card-${idx}`;
                card.style.pointerEvents = 'auto'; // enable mouse interaction
                // Position card slightly offset from the icon
                card.style.left = `calc(${r.x_pct}% + 15px)`;
                card.style.top = `calc(${r.y_pct}% + 15px)`;
                
                let cardHtml = `
                    <div class="smart-card-header">
                        <strong>${r.name}</strong>
                        <button class="close-card-btn" onclick="this.parentElement.parentElement.classList.remove('active')">×</button>
                    </div>
                    <div class="smart-card-body">
                        <div><strong>שטח:</strong> ${r.area_sqm} מ"ר</div>
                        <div><strong>רוחב:</strong> ${r.width_cm ? r.width_cm + ' ס"מ' : 'לא ידוע'}</div>
                        <div><strong>אורך:</strong> ${r.length_cm ? r.length_cm + ' ס"מ' : 'לא ידוע'}</div>
                    </div>
                `;
                
                if (roomFailures.length > 0) {
                    const failMsgs = roomFailures.map(f => `<div class="card-error">⚠️ ${f.message}</div>`).join('');
                    cardHtml += `<div class="smart-card-errors">${failMsgs}</div>`;
                }
                
                card.innerHTML = cardHtml;
                
                // Event listener to open card
                iconDiv.addEventListener('click', (e) => {
                    e.stopPropagation();
                    // Close all other cards
                    document.querySelectorAll('.smart-card.active').forEach(c => c.classList.remove('active'));
                    card.classList.add('active');
                });
                
                overlay.appendChild(highlightGlow);
                overlay.appendChild(iconDiv);
                overlay.appendChild(card);
            }
        });
        
        // Close cards when clicking outside
        blueprintViewer.addEventListener('click', () => {
            document.querySelectorAll('.smart-card.active').forEach(c => c.classList.remove('active'));
        });
    }

    function renderDimensionsTable(rooms) {
        const tableContainer = document.getElementById('vector-dimensions-container');
        
        const roomsBody = document.getElementById('rooms-table-body');
        const kitchenBody = document.getElementById('kitchen-table-body');
        const corridorsBody = document.getElementById('corridors-table-body');
        const balconiesBody = document.getElementById('balconies-table-body');
        const bathroomsBody = document.getElementById('bathrooms-table-body');
        
        const roomsContainer = document.getElementById('group-rooms-container');
        const kitchenContainer = document.getElementById('group-kitchen-container');
        const corridorsContainer = document.getElementById('group-corridors-container');
        const balconiesContainer = document.getElementById('group-balconies-container');
        const bathroomsContainer = document.getElementById('group-bathrooms-container');

        if (!rooms || rooms.length === 0) {
            tableContainer.classList.add('hidden');
            return;
        }
        
        tableContainer.classList.remove('hidden');
        
        // Clear all
        roomsBody.innerHTML = '';
        kitchenBody.innerHTML = '';
        corridorsBody.innerHTML = '';
        balconiesBody.innerHTML = '';
        bathroomsBody.innerHTML = '';
        
        let roomsCount = 0;
        let kitchenCount = 0;
        let corridorsCount = 0;
        let balconiesCount = 0;
        let bathroomsCount = 0;
        
        rooms.forEach((r, idx) => {
            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            tr.innerHTML = `
                <td style="padding: 6px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-weight: 600;">${r.name}</td>
                <td style="padding: 6px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">${r.area_sqm}</td>
                <td style="padding: 6px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">${r.width_cm || 'לא ידוע'}</td>
                <td style="padding: 6px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">${r.length_cm || 'לא ידוע'}</td>
            `;
            
            // Add hover events for highlight
            tr.addEventListener('mouseenter', () => {
                const glow = document.getElementById(`room-highlight-${idx}`);
                const icon = document.getElementById(`room-icon-${idx}`);
                tr.style.backgroundColor = 'rgba(0, 225, 255, 0.1)';
                if(glow) glow.classList.add('active');
                if(icon) icon.classList.add('hover-focus');
            });
            tr.addEventListener('mouseleave', () => {
                const glow = document.getElementById(`room-highlight-${idx}`);
                const icon = document.getElementById(`room-icon-${idx}`);
                tr.style.backgroundColor = '';
                if(glow) glow.classList.remove('active');
                if(icon) icon.classList.remove('hover-focus');
            });
            
            // Click to open card
            tr.addEventListener('click', () => {
                const icon = document.getElementById(`room-icon-${idx}`);
                if (icon) icon.click();
            });
            
            const rType = r.type || '';
            const rName = r.name || '';
            
            if (rType === 'kitchen' || rName.includes('מטבח')) {
                kitchenBody.appendChild(tr);
                kitchenCount++;
            }
            else if (rType === 'corridor' || rName.includes('מסדרון') || rName.includes('מעבר') || rName.includes('פרוזדור')) {
                corridorsBody.appendChild(tr);
                corridorsCount++;
            }
            else if (rType === 'balcony' || rName.includes('מרפסת')) {
                balconiesBody.appendChild(tr);
                balconiesCount++;
            }
            else if (rType === 'bathroom' || rName.includes('רחצה') || rName.includes('שירותים') || rName.includes('אמבטיה') || rName.includes('מקלחת') || rName.includes('ח.רחצה')) {
                bathroomsBody.appendChild(tr);
                bathroomsCount++;
            }
            else {
                roomsBody.appendChild(tr);
                roomsCount++;
            }
        });
        
        // Show/hide containers
        roomsContainer.style.display = roomsCount > 0 ? 'block' : 'none';
        kitchenContainer.style.display = kitchenCount > 0 ? 'block' : 'none';
        corridorsContainer.style.display = corridorsCount > 0 ? 'block' : 'none';
        balconiesContainer.style.display = balconiesCount > 0 ? 'block' : 'none';
        bathroomsContainer.style.display = bathroomsCount > 0 ? 'block' : 'none';
    }

    function renderChecklist(results) {
        checklistContainer.innerHTML = ''; 

        if (results.length === 0) {
            checklistContainer.innerHTML = '<div class="placeholder-state">אין תוצאות לאפיון זה</div>';
            return;
        }

        results.forEach(item => {
            const isPass = item.status === 'PASS';
            const isWarn = item.status === 'WARN';
            const iconClass = isPass ? 'status-pass' : (isWarn ? 'status-warn' : 'status-fail');
            const tagClass = isPass ? 'tag-pass' : (isWarn ? 'tag-warn' : 'tag-fail');
            const icon = isPass ? '✓' : (isWarn ? '!' : '✗');
            const msg = item.message ? item.message : 'תקין';

            const div = document.createElement('div');
            div.className = 'checklist-item';
            div.innerHTML = `
                <div class="status-icon ${iconClass}">${icon}</div>
                <div class="rule-info">
                    <div class="rule-name">${item.element} <span class="tag ${tagClass}">${item.status}</span></div>
                    <div class="rule-desc">Rule ${item.rule_id}: ${msg}</div>
                </div>
            `;
            checklistContainer.appendChild(div);
        });
    }

    function renderAIInsights(insights) {
        aiInsightsContainer.innerHTML = '';
        
        if (insights.length === 0) {
            aiInsightsContainer.innerHTML = '<div class="placeholder-state">אין תובנות לדירה זו</div>';
            return;
        }

        const div = document.createElement('div');
        div.className = 'ai-report';
        let html = '';
        insights.forEach(ins => {
            html += `<h3>${ins.title}</h3><p>${ins.description}</p>`;
        });
        div.innerHTML = html;
        aiInsightsContainer.appendChild(div);
    }
});
