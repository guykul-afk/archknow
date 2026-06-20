document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const btnAnalyze = document.getElementById('btn-analyze');
    const blueprintViewer = document.getElementById('blueprint-viewer');
    const checklistContainer = document.getElementById('checklist-container');
    const aiInsightsContainer = document.getElementById('ai-insights-container');

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
        uploadZone.querySelector('p').innerText = 'קובץ נטען בהצלחה: sample_apartment.dxf';
        btnAnalyze.style.display = 'block';
    });

    // Mock API Call to our Python Engine
    btnAnalyze.addEventListener('click', () => {
        btnAnalyze.innerText = 'מנתח שרטוט...';
        btnAnalyze.disabled = true;

        // Simulate network request
        setTimeout(() => {
            uploadZone.style.display = 'none';
            blueprintViewer.classList.remove('hidden');
            renderChecklist();
            renderAIInsights();
        }, 1500);
    });

    function renderChecklist() {
        const mockResults = [
            { status: 'PASS', element: 'Global Ceiling', rule: 'B1.13', msg: '2.7m (תקין)' },
            { status: 'PASS', element: 'Room_1 (Master)', rule: 'B1.6', msg: '12.0sqm (תקין)' },
            { status: 'FAIL', element: 'Room_2 (Mamad)', rule: 'B1.6', msg: '6.0sqm נמוך מהמינימום 9.0sqm' },
            { status: 'FAIL', element: 'Room_3 (Bathroom)', rule: 'B1.6', msg: '4.0sqm נמוך מהמינימום 4.5sqm' },
            { status: 'PASS', element: 'Main Entrance', rule: 'B44', msg: '90cm רוחב תקין לנגישות' }
        ];

        checklistContainer.innerHTML = ''; // clear placeholder

        mockResults.forEach(item => {
            const isPass = item.status === 'PASS';
            const iconClass = isPass ? 'status-pass' : 'status-fail';
            const tagClass = isPass ? 'tag-pass' : 'tag-fail';
            const icon = isPass ? '✓' : '✗';

            const div = document.createElement('div');
            div.className = 'checklist-item';
            div.innerHTML = `
                <div class="status-icon ${iconClass}">${icon}</div>
                <div class="rule-info">
                    <div class="rule-name">${item.element} <span class="tag ${tagClass}">${item.status}</span></div>
                    <div class="rule-desc">Rule ${item.rule}: ${item.msg}</div>
                </div>
            `;
            checklistContainer.appendChild(div);
        });
    }

    function renderAIInsights() {
        aiInsightsContainer.innerHTML = `
            <div class="ai-report">
                <h3>⚠️ פגיעה בפרטיות (כלל B1.2)</h3>
                <p>הגרף המרחבי מראה כי דלת הכניסה הראשית נפתחת ישירות אל תוך <strong>Living Room</strong>. דבר זה מונע כל פרטיות מהמשפחה השוהה בסלון.</p>
                <p>בנוסף, ה-<strong>Bathroom</strong> נפתח גם הוא ישירות לסלון (הפרה חמורה של כלל C1).</p>
                
                <h3>🔄 זרימה ותנועה (כלל C4)</h3>
                <p>הסלון משמש כרגע כ"צומת התנועה" הראשי של כל הדירה. רוב התנועה נשענת על הסלון כמעבר, מה שפוגע בתחושת הנינוחות בו.</p>
                
                <h3>💡 המלצות אדריכליות</h3>
                <p>מומלץ לייצר <strong>מבואה (Foyer)</strong> שתחצוץ בין דלת הכניסה לסלון. בנוסף יש להזיז את דלת השירותים כך שתיפתח למסדרון שקט ולא לאזור האירוח המרכזי.</p>
            </div>
        `;
    }
});
