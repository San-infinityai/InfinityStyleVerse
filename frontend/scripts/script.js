// dashboard
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const mainContent = document.getElementById('main-content');
    const currentDateElement = document.getElementById('current-date');


    const today = new Date();
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    currentDateElement.textContent = today.toLocaleDateString('en-US', options);


    hamburgerMenu.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });


    mainContent.addEventListener('click', (event) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('active') && !sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });


    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            sidebar.classList.remove('hidden');
        } else {
            sidebar.classList.add('hidden');
        }
    });


    if (window.innerWidth <= 768) {
        sidebar.classList.add('hidden');
    }

    Chart.defaults.font.family = 'DM Sans, sans-serif';
    Chart.defaults.color = 'var(--text-gray)';
    Chart.defaults.font.size = 12;


    function createGradient(ctx) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 220);
        gradient.addColorStop(0, 'rgba(193, 154, 107, 0.3)');
        gradient.addColorStop(1, 'rgba(193, 154, 107, 0)');
        return gradient;
    }


    const userGrowthCtx = document.getElementById('userGrowthChart').getContext('2d');
    let userGrowthChart = new Chart(userGrowthCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'User Growth',
                data: [100, 120, 150, 130, 180, 200, 250, 280, 320, 380, 450, 520],

                backgroundColor: createGradient(userGrowthCtx),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6,
                pointBackgroundColor: 'var(--accent-color)',
                pointBorderColor: '#C2A57D',
                pointBorderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'DM Sans', size: 12 },
                    backgroundColor: 'rgba(34,34,34,0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 10,
                    cornerRadius: 6,
                    borderColor: 'var(--accent-color)',
                    borderWidth: 1,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'var(--text-gray)',
                        font: { family: 'DM Sans', size: 11, weight: 'normal' }
                    },
                    border: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.08)'
                    },
                    ticks: {
                        color: 'var(--text-gray)',
                        font: { family: 'DM Sans', size: 11, weight: 'normal' },
                        callback: function (value) {
                            return value > 999 ? (value / 1000).toFixed(0) + 'k' : value;
                        }
                    },
                    border: {
                        display: false
                    }
                }
            }
        }
    });


    const userDistributionCtx = document.getElementById('userDistributionChart').getContext('2d');
    let userDistributionChart = new Chart(userDistributionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Admin', 'Executive', 'User', 'Guest'],
            datasets: [{
                data: [52.1, 22.8, 13.9, 11.2],
                backgroundColor: [
                    '#232321',
                    '#C19A6B',
                    '#E6C89C',
                    '#C27D7E'


                ],
                hoverOffset: 8,

                borderWidth: 2,
                spacing: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    titleFont: { family: 'Inter', size: 14, weight: 'bold' },
                    bodyFont: { family: 'DM Sans', size: 12 },
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += context.parsed.toFixed(1) + '%';
                            }
                            return label;
                        }
                    },
                    backgroundColor: 'rgba(34,34,34,0.9)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 10,
                    cornerRadius: 6,
                    borderColor: 'var(--accent-color)',
                    borderWidth: 1,
                    displayColors: true,
                    boxWidth: 10,
                    boxHeight: 10
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            elements: {
                arc: {
                    hoverBorderColor: 'var(--accent-color)',
                }
            }
        }
    });
    const weeklyBtn = document.getElementById('weeklyBtn');
    const monthlyBtn = document.getElementById('monthlyBtn');
    const yearlyBtn = document.getElementById('yearlyBtn');

    const updateChartData = (period) => {
        let newData;
        let newLabels;

        if (period === 'weekly') {
            newLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            newData = [80, 100, 120, 90, 130, 110, 150];
        } else if (period === 'monthly') {
            newLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            newData = [100, 120, 150, 130, 180, 200, 250, 280, 320, 380, 450, 520];
        } else if (period === 'yearly') {
            newLabels = ['2022', '2023', '2024', '2025'];
            newData = [800, 1000, 1250, 1500];
        }

        userGrowthChart.data.labels = newLabels;
        userGrowthChart.data.datasets[0].data = newData;
        userGrowthChart.data.datasets[0].backgroundColor = createGradient(userGrowthCtx);
        userGrowthChart.update();


        [weeklyBtn, monthlyBtn, yearlyBtn].forEach(btn => btn.classList.remove('active'));
        if (period === 'weekly') weeklyBtn.classList.add('active');
        else if (period === 'monthly') monthlyBtn.classList.add('active');
        else if (period === 'yearly') yearlyBtn.classList.add('active');
    };

    weeklyBtn.addEventListener('click', () => updateChartData('weekly'));
    monthlyBtn.addEventListener('click', () => updateChartData('monthly'));
    yearlyBtn.addEventListener('click', () => updateChartData('yearly'));

    updateChartData('monthly');
});



//add product
const fileInput = document.getElementById('product-images');
const previewContainer = document.getElementById('preview-container');

fileInput.addEventListener('change', function () {
  previewContainer.innerHTML = '';
  const files = this.files;

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement('img');
      img.src = e.target.result;
      previewContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});


//onboarding

window.addEventListener('load', () => {
  const modal = new bootstrap.Modal(document.getElementById('welcomeModal'));
  modal.show();
});

function goToHome() {
  window.location.href = "index.html";
}

//profile

 function showTab(tabId, event) {
      document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }

    function saveCard(button) {
      const card = button.closest('.card');
      card.classList.add('saved');
      button.disabled = true;
      button.textContent = '✔';
      setTimeout(() => {
        card.classList.remove('saved');
        button.disabled = false;
        button.textContent = '💾';
      }, 2000);
    }

