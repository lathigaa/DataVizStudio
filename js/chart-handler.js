document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.chart-card').forEach(card => {
        card.addEventListener('click', function() {
            const chartType = this.dataset.chart;
            const style = document.getElementById('style-selector')?.value || 'classic';
            const color = document.getElementById('color-selector')?.value || '#3366CC';
  
            // Show loading state
            this.classList.add('loading');
  
            fetch('/generate_chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chart_type: chartType,
                    style: style,
                    color: color
                })
            })
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                if (!data.success) throw new Error(data.error || 'Unknown error');
                
                const canvas = document.getElementById('dashboard-canvas');
                const newChart = document.createElement('div');
                newChart.className = 'chart-item';
                newChart.innerHTML = data.chart_html;
                canvas.appendChild(newChart);
            })
            .catch(error => {
                console.error('Chart error:', error);
                alert('Failed to generate chart: ' + error.message);
            })
            .finally(() => {
                this.classList.remove('loading');
            });
        });
    });
  });
