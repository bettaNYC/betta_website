// market-data.js
const marketData = {
    aluminum: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        values2024: [2100, 2150, 2080, 2200, 2180, 2250, 2300, 2280, 2320, 2340, 2290, 2234],
        values2025: [2234, 2265, 2290, 2310]
    },
    copper: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        values2024: [8200, 8300, 8450, 8400, 8600, 8550, 8500, 8480, 8520, 8490, 8470, 8453],
        values2025: [8453, 8420, 8390, 8410]
    },
    steel: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        values2024: [680, 695, 710, 700, 715, 725, 730, 720, 718, 722, 728, 725],
        values2025: [725, 730, 735, 740]
    }
};

function createChart(metal) {
    const ctx = document.getElementById('metalChart').getContext('2d');
    
    if (window.currentChart) {
        window.currentChart.destroy();
    }

    window.currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: marketData[metal].labels,
            datasets: [
                {
                    label: '2024',
                    data: marketData[metal].values2024,
                    borderColor: '#2c3e50',
                    backgroundColor: 'rgba(44, 62, 80, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
                },
                {
                    label: '2025',
                    data: marketData[metal].values2025,
                    borderColor: '#8e44ad',
                    backgroundColor: 'rgba(142, 68, 173, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#333',
                    bodyColor: '#666',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}
