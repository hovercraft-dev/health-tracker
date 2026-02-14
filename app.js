// HealthOS v2 — Core Logic

const STORAGE_KEY = 'healthos_data_v2';
const DATA_FILE = './data.json';

// API base: auto-detect (same origin when deployed, or explicit for dev)
// For static hosting (GitHub Pages): '' (empty = same origin)
// For local Flask backend: 'http://localhost:5000'
const API_BASE = '';  // Default: static hosting (no backend)

// Goals
const GOALS = {
    primary: { label: '100kg', value: 100 },
    secondary: { label: '95kg', value: 95 },
    startWeight: 112, // approx highest recent weight for progress calc
    calorieTarget: 2400,
    proteinTarget: 180
};

// State
let healthData = [];
let trendChart = null;
let waistChart = null;
let currentRange = 30;
let syncTimer = null;
let lastSyncTime = null;

// ─── Helpers ────────────────────────────────────────────────

function cleanNum(val) {
    if (val == null) return null;
    if (typeof val === 'number') return val;
    if (typeof val === 'string') return parseFloat(val.replace(/,/g, '')) || null;
    return null;
}

function fmtDate(dateStr) {
    const d = new Date(dateStr + 'T00:00:00');
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${d.getDate()} ${months[d.getMonth()]}`;
}

function $(id) { return document.getElementById(id); }

// ─── Server Sync ────────────────────────────────────────────

const ServerSync = {
    async pull() {
        try {
            updateSyncUI('syncing', 'Pulling...');
            const res = await fetch(`${API_BASE}/api/data`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const serverData = await res.json();
            if (Array.isArray(serverData) && serverData.length > 0) {
                // Merge: server is source of truth, but keep any local-only entries
                const serverMap = {};
                serverData.forEach(d => { serverMap[d.date] = d; });

                // Add local entries not on server
                healthData.forEach(d => {
                    if (!serverMap[d.date]) serverMap[d.date] = d;
                });

                healthData = Object.values(serverMap);
                healthData.sort((a, b) => a.date.localeCompare(b.date));
                localStorage.setItem(STORAGE_KEY, JSON.stringify(healthData));
                console.log(`[HealthOS] Pulled ${serverData.length} entries from server`);
                lastSyncTime = new Date();
                updateSyncUI('ok', fmtTime(lastSyncTime));
                return true;
            }
        } catch (e) {
            console.warn('[HealthOS] Server pull failed (offline?)', e.message);
            updateSyncUI('offline', 'Offline');
        }
        return false;
    },

    async push() {
        try {
            updateSyncUI('syncing', 'Saving...');
            const res = await fetch(`${API_BASE}/api/data`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(healthData)
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const result = await res.json();
            lastSyncTime = new Date();
            updateSyncUI('ok', fmtTime(lastSyncTime));
            console.log(`[HealthOS] Pushed ${result.count} entries to server`);
            return true;
        } catch (e) {
            console.warn('[HealthOS] Server push failed (offline?)', e.message);
            updateSyncUI('offline', 'Offline');
            return false;
        }
    },

    schedulePush() {
        if (syncTimer) clearTimeout(syncTimer);
        syncTimer = setTimeout(() => ServerSync.push(), 2000);
    }
};

function updateSyncUI(status, label) {
    const el = document.getElementById('syncStatus');
    const labelEl = document.getElementById('syncLabel');
    if (!el || !labelEl) return;

    labelEl.textContent = label;
    const iconMap = { ok: 'cloud', syncing: 'loader', offline: 'cloud-off' };
    const colorMap = { ok: 'var(--green)', syncing: 'var(--blue)', offline: 'var(--text-dim)' };
    el.style.color = colorMap[status] || 'var(--text-dim)';

    const icon = el.querySelector('[data-lucide]');
    if (icon) {
        icon.setAttribute('data-lucide', iconMap[status] || 'cloud');
        lucide.createIcons();
    }
}

function fmtTime(d) {
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// ─── Init ───────────────────────────────────────────────────

async function init() {
    // Try server first, fall back to local
    const serverOk = await ServerSync.pull();
    if (!serverOk || !healthData.length) {
        await loadLocalData();
    }
    render();
    setupListeners();
}

// ─── Data Layer ─────────────────────────────────────────────

async function loadLocalData() {
    const local = localStorage.getItem(STORAGE_KEY);
    let loaded = false;

    if (local) {
        try {
            const parsed = JSON.parse(local);
            if (Array.isArray(parsed) && parsed.length > 0 && parsed.some(d => d.weight)) {
                healthData = parsed;
                loaded = true;
                console.log(`[HealthOS] Loaded ${healthData.length} entries from localStorage`);
            } else {
                console.warn('[HealthOS] localStorage data empty or invalid, will re-seed');
            }
        } catch (e) {
            console.warn('[HealthOS] localStorage parse error, will re-seed', e);
        }
    }

    if (!loaded) {
        try {
            console.log('[HealthOS] Fetching seed data from', DATA_FILE);
            const res = await fetch(DATA_FILE);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const json = await res.json();
            healthData = json.map(d => {
                const dateStr = d.date.split('T')[0];
                return { ...d, date: dateStr };
            });
            persist();
            console.log(`[HealthOS] Seeded ${healthData.length} entries from data.json`);
        } catch (e) {
            console.error('[HealthOS] Seed load failed', e);
            healthData = [];
        }
    }

    healthData.sort((a, b) => a.date.localeCompare(b.date));
    console.log(`[HealthOS] Total entries: ${healthData.length}, weight entries: ${healthData.filter(d => d.weight).length}`);
}

function persist() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(healthData));
    ServerSync.schedulePush();
}

// ─── Render All ─────────────────────────────────────────────

function render() {
    if (!healthData.length) return;

    const weightEntries = healthData.filter(d => d.weight).sort((a, b) => a.date.localeCompare(b.date));
    const waistEntries = healthData.filter(d => d.waist_cm).sort((a, b) => a.date.localeCompare(b.date));

    renderHero(weightEntries, waistEntries);
    renderGoals(weightEntries);
    renderMacros();
    renderTrendChart(weightEntries, waistEntries);
    renderWaistChart(waistEntries);
    renderHistory();
}

// ─── Hero Card ──────────────────────────────────────────────

function renderHero(wEntries, waistEntries) {
    const last = wEntries[wEntries.length - 1];
    const prev = wEntries[wEntries.length - 2];

    // Weight
    $('currentWeight').textContent = last ? last.weight.toFixed(1) : '--.-';

    // Trend
    if (last && prev) {
        const diff = last.weight - prev.weight;
        const icon = diff <= 0 ? 'trending-down' : 'trending-up';
        const color = diff <= 0 ? 'var(--green)' : 'var(--red)';
        const el = $('trendIndicator');
        el.innerHTML = `<i data-lucide="${icon}" style="width:14px;height:14px;"></i> ${Math.abs(diff).toFixed(1)}kg`;
        el.style.color = color;
        el.style.background = diff <= 0 ? 'rgba(16,185,129,0.12)' : 'rgba(239,68,68,0.12)';
        lucide.createIcons();
    }

    // Waist
    const lastW = waistEntries[waistEntries.length - 1];
    $('currentWaist').textContent = lastW ? `${lastW.waist_cm}cm` : '--';

    // BMI (assuming ~183cm height based on data context)
    const height = 1.83;
    if (last) {
        const bmi = (last.weight / (height * height)).toFixed(1);
        $('currentBMI').textContent = bmi;
    }

    // Last logged date
    if (last) {
        $('lastLogDate').textContent = fmtDate(last.date);
    }
}

// ─── Goal Milestones ────────────────────────────────────────

function renderGoals(wEntries) {
    const last = wEntries[wEntries.length - 1];
    if (!last) return;

    const w = last.weight;
    const range = GOALS.startWeight - GOALS.primary.value; // e.g. 112 - 100 = 12
    const range2 = GOALS.startWeight - GOALS.secondary.value; // 112 - 95 = 17

    // Primary
    const progress1 = Math.min(100, Math.max(0, ((GOALS.startWeight - w) / range) * 100));
    const remaining1 = Math.max(0, w - GOALS.primary.value);
    $('goal1Bar').style.width = progress1.toFixed(0) + '%';
    $('goal1Remaining').textContent = remaining1 > 0 ? `${remaining1.toFixed(1)}kg to go` : '✓ Reached!';

    // Secondary
    const progress2 = Math.min(100, Math.max(0, ((GOALS.startWeight - w) / range2) * 100));
    const remaining2 = Math.max(0, w - GOALS.secondary.value);
    $('goal2Bar').style.width = progress2.toFixed(0) + '%';
    $('goal2Remaining').textContent = remaining2 > 0 ? `${remaining2.toFixed(1)}kg to go` : '✓ Reached!';
}

// ─── Macros ─────────────────────────────────────────────────

function renderMacros() {
    const logs = healthData
        .filter(d => cleanNum(d.calories) || cleanNum(d.protein_g))
        .sort((a, b) => b.date.localeCompare(a.date))
        .slice(0, 7);

    if (!logs.length) return;

    const totalCals = logs.reduce((s, d) => s + (cleanNum(d.calories) || 0), 0);
    const totalProt = logs.reduce((s, d) => s + (cleanNum(d.protein_g) || 0), 0);

    $('avgCals').textContent = Math.round(totalCals / logs.length).toLocaleString();
    $('avgProtein').textContent = Math.round(totalProt / logs.length) + 'g';
}

// ─── Trend Chart (Weight + Waist, dual Y-axis) ─────────────

function renderTrendChart(wEntries, waistEntries) {
    const ctx = $('trendChart').getContext('2d');

    // Get data for selected range
    let wData, waData;
    if (currentRange === 'all') {
        // Filter to recent journey only (Nov 2025+)
        wData = wEntries.filter(d => d.date >= '2025-11-01');
        waData = waistEntries.filter(d => d.date >= '2025-11-01');
    } else {
        wData = wEntries.slice(-currentRange);
        waData = waistEntries.slice(-currentRange);
    }

    // Build unified label set from weight dates
    const labels = wData.map(d => d.date);
    const weightValues = wData.map(d => d.weight);

    // Map waist to same date axis (sparse)
    const waistMap = {};
    waData.forEach(d => { waistMap[d.date] = d.waist_cm; });
    const waistValues = labels.map(d => waistMap[d] || null);

    if (trendChart) trendChart.destroy();

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.map(d => fmtDate(d)),
            datasets: [
                {
                    label: 'Weight (kg)',
                    data: weightValues,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59,130,246,0.08)',
                    borderWidth: 2.5,
                    tension: 0.35,
                    pointRadius: currentRange === 'all' ? 0 : 3,
                    pointHoverRadius: 5,
                    pointBackgroundColor: '#3b82f6',
                    fill: true,
                    yAxisID: 'y'
                },
                {
                    label: 'Waist (cm)',
                    data: waistValues,
                    borderColor: '#10b981',
                    borderWidth: 2,
                    borderDash: [4, 3],
                    tension: 0.35,
                    pointRadius: currentRange === 'all' ? 0 : 3,
                    pointHoverRadius: 5,
                    pointBackgroundColor: '#10b981',
                    fill: false,
                    spanGaps: true,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1e293b',
                    borderColor: '#334155',
                    borderWidth: 1,
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    padding: 10,
                    cornerRadius: 8,
                    displayColors: true
                },
                annotation: {
                    annotations: {
                        goalPrimary: {
                            type: 'line',
                            yMin: GOALS.primary.value,
                            yMax: GOALS.primary.value,
                            yScaleID: 'y',
                            borderColor: 'rgba(59,130,246,0.5)',
                            borderWidth: 2,
                            borderDash: [8, 4],
                            label: {
                                display: true,
                                content: '100kg',
                                position: 'start',
                                backgroundColor: 'rgba(59,130,246,0.2)',
                                color: '#60a5fa',
                                font: { size: 11, weight: '600' },
                                padding: { top: 2, bottom: 2, left: 6, right: 6 }
                            }
                        },
                        goalSecondary: {
                            type: 'line',
                            yMin: GOALS.secondary.value,
                            yMax: GOALS.secondary.value,
                            yScaleID: 'y',
                            borderColor: 'rgba(167,139,250,0.5)',
                            borderWidth: 2,
                            borderDash: [6, 4],
                            label: {
                                display: true,
                                content: '95kg',
                                position: 'start',
                                backgroundColor: 'rgba(167,139,250,0.2)',
                                color: '#c4b5fd',
                                font: { size: 11, weight: '600' },
                                padding: { top: 2, bottom: 2, left: 6, right: 6 }
                            }
                        }
                    }
                }
            },
            scales: {
                y: {
                    position: 'left',
                    grid: { color: 'rgba(51,65,85,0.5)', lineWidth: 0.5 },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 },
                        callback: v => v + 'kg'
                    },
                    // Let it breathe below 95 target
                    suggestedMin: 90,
                    title: {
                        display: false
                    }
                },
                y1: {
                    position: 'right',
                    grid: { display: false },
                    ticks: {
                        color: 'rgba(16,185,129,0.6)',
                        font: { size: 11 },
                        callback: v => v + 'cm'
                    },
                    title: { display: false }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#475569',
                        font: { size: 10 },
                        maxRotation: 45,
                        maxTicksLimit: 12
                    }
                }
            }
        }
    });
}

// ─── Waist Chart ────────────────────────────────────────────

function renderWaistChart(waistEntries) {
    const ctx = $('waistChart').getContext('2d');

    // Show recent journey waist data
    const data = waistEntries.filter(d => d.date >= '2025-11-01');
    if (!data.length) return;

    const labels = data.map(d => fmtDate(d.date));
    const values = data.map(d => d.waist_cm);

    if (waistChart) waistChart.destroy();

    waistChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Waist (cm)',
                data: values,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16,185,129,0.08)',
                borderWidth: 2.5,
                tension: 0.35,
                pointRadius: 3,
                pointHoverRadius: 5,
                pointBackgroundColor: '#10b981',
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1e293b',
                    borderColor: '#334155',
                    borderWidth: 1,
                    titleColor: '#f1f5f9',
                    bodyColor: '#94a3b8',
                    padding: 10,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(51,65,85,0.5)', lineWidth: 0.5 },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 },
                        callback: v => v + 'cm'
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: '#475569',
                        font: { size: 10 },
                        maxRotation: 45,
                        maxTicksLimit: 10
                    }
                }
            }
        }
    });
}

// ─── History / Log Viewer ───────────────────────────────────

function renderHistory() {
    const container = $('historyList');

    // Remove old rows (keep header)
    const header = container.querySelector('.header');
    container.innerHTML = '';
    container.appendChild(header);

    // Show last 20 entries that have any data, newest first
    const entries = [...healthData]
        .filter(d => d.weight || d.waist_cm || d.calories || d.protein_g)
        .sort((a, b) => b.date.localeCompare(a.date))
        .slice(0, 20);

    $('entryCount').textContent = `${healthData.length} total`;

    entries.forEach(d => {
        const row = document.createElement('div');
        row.className = 'history-row';

        const cal = cleanNum(d.calories);
        const prot = cleanNum(d.protein_g);
        const macroStr = (cal || prot)
            ? `${cal ? Math.round(cal) : '-'} / ${prot ? Math.round(prot) + 'g' : '-'}`
            : '-';

        row.innerHTML = `
            <span style="color:var(--text-muted)">${fmtDate(d.date)}</span>
            <span style="font-weight:600">${d.weight ? d.weight + 'kg' : '-'}</span>
            <span style="color:var(--green)">${d.waist_cm ? d.waist_cm + 'cm' : '-'}</span>
            <span style="color:var(--text-dim);font-size:0.8rem">${macroStr}</span>
        `;
        container.appendChild(row);
    });
}

// ─── Event Listeners ────────────────────────────────────────

function setupListeners() {
    // Log modal
    $('logBtn').addEventListener('click', () => {
        $('logModal').classList.add('open');
    });

    $('closeLogBtn').addEventListener('click', () => {
        $('logModal').classList.remove('open');
    });

    // Click backdrop to close
    $('logModal').addEventListener('click', (e) => {
        if (e.target === $('logModal')) $('logModal').classList.remove('open');
    });

    // Save entry
    $('saveLogBtn').addEventListener('click', () => {
        const entry = {
            date: new Date().toISOString().split('T')[0],
            weight: parseFloat($('inputWeight').value) || null,
            waist_cm: parseFloat($('inputWaist').value) || null,
            calories: parseFloat($('inputCals').value) || null,
            protein_g: parseFloat($('inputProtein').value) || null,
            type: 'daily_log'
        };

        // Merge or add
        const idx = healthData.findIndex(d => d.date === entry.date);
        if (idx >= 0) {
            // Only overwrite non-null fields
            Object.keys(entry).forEach(k => {
                if (entry[k] != null) healthData[idx][k] = entry[k];
            });
        } else {
            healthData.push(entry);
        }

        healthData.sort((a, b) => a.date.localeCompare(b.date));
        persist();
        render();

        $('logModal').classList.remove('open');
        ['inputWeight', 'inputWaist', 'inputCals', 'inputProtein'].forEach(id => $(id).value = '');
    });

    // Tab bar for chart range
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const range = btn.dataset.range;
            currentRange = range === 'all' ? 'all' : parseInt(range);

            const wEntries = healthData.filter(d => d.weight).sort((a, b) => a.date.localeCompare(b.date));
            const waistEntries = healthData.filter(d => d.waist_cm).sort((a, b) => a.date.localeCompare(b.date));
            renderTrendChart(wEntries, waistEntries);
        });
    });

    // Export
    $('exportBtn').addEventListener('click', () => {
        const blob = new Blob([JSON.stringify(healthData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `healthos_backup_${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
    });

    // Import
    $('importFile').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
            try {
                const json = JSON.parse(ev.target.result);
                if (Array.isArray(json)) {
                    healthData = json;
                    persist();
                    render();
                }
            } catch (err) {
                alert('Invalid JSON file');
            }
        };
        reader.readAsText(file);
    });

    // Refresh
    $('refreshBtn').addEventListener('click', () => location.reload());
}

// ─── Boot ───────────────────────────────────────────────────
init();
