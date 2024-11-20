var xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
var yValues = [55, 49, 44, 24, 15];
var barColors = ["red", "green","blue","orange","brown"];
let delayed;

new Chart(document.getElementById("bigChart"), {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
            {
                label: '<50%',
                data: [8, 5, 5, 5, 0, 0, 4],
                borderWidth: 1,
                fill: true,
                backgroundColor: 'rgba(220, 53, 69, 1)',
                tension: 0.1
            },
            {
                label: '>50%',
                data: [30, 15, 20, 10, 8, 15, 12],
                borderWidth: 1,
                fill: true,
                backgroundColor: 'rgba(255, 193, 7, 1)',
                tension: 0.1
            },
            {
                label: '>100%',
                data: [62, 80, 70, 85, 92, 85, 83],
                borderWidth: 1,
                fill: true,
                backgroundColor: 'rgba(141, 212, 19, 1)',
                tension: 0.1
            },
    ]
    },
    options: {
        plugins: {
            legend: {
               display: false
            }
         },
        tooltips: {
            callbacks: {
                label: function(tooltipItem) {
                    return tooltipItem.yLabel;
               }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                min: 0,
                ticks: {
                    stepSize: 20,
                    autoSkip: false
                }
            },
            x: { 
                grid : {display : false}
            }
        },
        animation: {
            onComplete: () => {
              delayed = true;
            },
            delay: (context) => {
            let delay = 0;
            if (context.type === 'data' && context.mode === 'default' && !delayed) {
                delay = context.dataIndex * 100 + context.datasetIndex * 100;
            }
            return delay;
            },
        },
    }
});

new Chart(document.getElementById("smallChart1"), {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3, 4],
        borderWidth: 1
        }]
    },
    options: {
        plugins: {
            legend: {
               display: false
            }
         },
        scales: {
            y: {
                beginAtZero: true
            },
            x: { 
                grid : {display : false}
            }
        }
    }
});

new Chart(document.getElementById("smallChart2"), {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3, 4],
        borderWidth: 1
        }]
    },
    options: {
        plugins: {
            legend: {
               display: false
            }
         },
        scales: {
            y: {
                beginAtZero: true
            },
            x: { 
                grid : {display : false}
            }
        }
    }
});