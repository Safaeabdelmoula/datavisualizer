// charts.js
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr'],
            datasets: [{
                label: 'Ventes mensuelles',
                data: [12, 19, 3, 5],
                backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#E91E63']
            }]
        },
        options: {
            responsive: true
        }
    });
});
