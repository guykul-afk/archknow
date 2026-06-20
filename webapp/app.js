document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const btnAnalyze = document.getElementById('btn-analyze');
    const blueprintViewer = document.getElementById('blueprint-viewer');
    const checklistContainer = document.getElementById('checklist-container');
    const aiInsightsContainer = document.getElementById('ai-insights-container');
    
    const projectNavigator = document.getElementById('project-navigator');
    const floorSelect = document.getElementById('floor-select');
    const aptSelect = document.getElementById('apt-select');
    
    let projectData = null;

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
        uploadZone.style.borderColor = 'var(--success)';
        uploadZone.style.background = 'rgba(0, 210, 106, 0.05)';
        uploadZone.querySelector('p').innerText = 'קובץ נטען בהצלחה: sample_project.dxf';
        btnAnalyze.style.display = 'block';
    });

    // API Call to our Python Engine
    btnAnalyze.addEventListener('click', () => {
        btnAnalyze.innerText = 'מנתח פרויקט (מחפש קומות ודירות)...';
        btnAnalyze.disabled = true;

        fetch('/api/analyze')
            .then(res => res.json())
            .then(data => {
                projectData = data;
                uploadZone.style.display = 'none';
                projectNavigator.classList.remove('hidden');
                blueprintViewer.classList.remove('hidden');
                
                populateFloors();
            })
            .catch(err => {
                console.error(err);
                btnAnalyze.innerText = 'שגיאה בשרת';
            });
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
        const apt = projectData.floors[floorIdx].apartments[aptIdx];
        
        if (apt) {
            renderChecklist(apt.validation_results || []);
            renderAIInsights(apt.qualitative_insights || []);
            renderBlueprint(apt.rooms || []);
        }
    }

    function renderBlueprint(rooms) {
        blueprintViewer.innerHTML = '<svg class="connection-lines"></svg>';
        let top = 10;
        let left = 10;
        rooms.forEach((r, idx) => {
            const div = document.createElement('div');
            div.className = 'node';
            div.style.top = top + '%';
            div.style.left = left + '%';
            div.innerText = r.name;
            blueprintViewer.appendChild(div);
            left += 30;
            if (left > 70) {
                left = 10;
                top += 30;
            }
        });
    }

    function renderChecklist(results) {
        checklistContainer.innerHTML = ''; 

        if (results.length === 0) {
            checklistContainer.innerHTML = '<div class="placeholder-state">אין תוצאות לאפיון זה</div>';
            return;
        }

        results.forEach(item => {
            const isPass = item.status === 'PASS';
            const iconClass = isPass ? 'status-pass' : 'status-fail';
            const tagClass = isPass ? 'tag-pass' : 'tag-fail';
            const icon = isPass ? '✓' : '✗';
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
