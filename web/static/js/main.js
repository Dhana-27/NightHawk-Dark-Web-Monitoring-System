document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    // Refresh stats every 10 seconds for demo
    setInterval(fetchStats, 10000); 
});

let chartInstance = null;

async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        updateKPIs(data);
        updateAlerts(data.recent_alerts);
        updateChart(data.top_keywords);
    } catch (error) {
        console.error("Failed to fetch stats", error);
    }
}

function updateKPIs(data) {
    document.getElementById('total-crawled').textContent = data.total_crawled.toLocaleString();
    document.getElementById('threats-detected').textContent = data.threats_detected.toLocaleString();
    document.getElementById('active-alerts').textContent = data.active_alerts.toLocaleString();
}

function updateAlerts(alerts) {
    const list = document.getElementById('alert-list');
    list.innerHTML = ''; // Clear existing
    
    alerts.forEach(alert => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span class="alert-time">${alert.time}</span>
            <span class="alert-type">[${alert.type}]</span> 
            ${alert.domain}
        `;
        list.appendChild(li);
    });
}

function updateChart(keywordsData) {
    const ctx = document.getElementById('keywordChart').getContext('2d');
    
    const labels = keywordsData.map(k => k.keyword);
    const data = keywordsData.map(k => k.count);

    if (chartInstance) {
        chartInstance.data.labels = labels;
        chartInstance.data.datasets[0].data = data;
        chartInstance.update();
        return;
    }

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Keyword Mentions',
                data: data,
                backgroundColor: '#58a6ff',
                borderColor: '#1f6feb',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#30363d' },
                    ticks: { color: '#8b949e' }
                },
                x: {
                    grid: { color: '#30363d' },
                    ticks: { color: '#8b949e' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#c9d1d9' }
                }
            }
        }
    });
}
