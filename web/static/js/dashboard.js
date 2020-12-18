Chart.defaults.global.responsive = true;

//charts/get_cve_types_chart
var ctx = document.getElementById("severitytypes-chart");
if (ctx) {
    ctx.height = 120;
    var myChart_severitytypes = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [],
            defaultFontFamily: '"NeuePlakText-Regular", "Helvetica Neue", Helvetica, Arial, sans-serif',
            datasets: [
                {
                    label: "Severity Types",
                    data: [],
                    backgroundColor: ['#305868', '#F96702', '#00828C', '#A94442', '#76BC21', '#66512C', '#99DADF', '#4D4D4D'],
                    hoverBackgroundColor: "#969696"
                }
            ]
        },
        options: {
            legend: {
                position: 'top'
            },
        }

    });
}
var getData_severitytypes = function () {
    
    $.ajax({
        type: 'GET',
        dataType: 'JSON',
        url: '/charts/get_cve_types_chart',
        success: function (response) {
            myChart_severitytypes.data.datasets[0].data = response.values;
            myChart_severitytypes.data.labels = response.labels;
            myChart_severitytypes.update();
        }
    });
}
getData_severitytypes();


//charts/last_month_alarms_chart
var ctx = document.getElementById("numberofalarms_chart");
if (ctx) {
    ctx.height = 120;
    var myChart_numberofalarms = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            defaultFontFamily: '"NeuePlakText-Regular", "Helvetica Neue", Helvetica, Arial, sans-serif',
            datasets: [
                {
                    label: "Vulnerabilities found last 30 days",
                    data: [],
                    backgroundColor: ['#99DADF'],
                    hoverBackgroundColor: "#969696"
                }
            ]
        },
        options: {
            legend: {
                position: 'top'
            },
        }

    });
}
var getData_numberofalarms = function () {
    
    $.ajax({
        type: 'GET',
        dataType: 'JSON',
        url: '/charts/last_month_alarms_chart',
        success: function (response) {
            myChart_numberofalarms.data.datasets[0].data = response.values;
            myChart_numberofalarms.data.labels = response.labels;
            myChart_numberofalarms.update();
        }
    });
}
getData_numberofalarms();

//charts/unresolved_alarms

var ctx = document.getElementById("unresolvedalarms_chart");
if (ctx) {
    ctx.height = 120;
    var myChart_unresolvedalarmss = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            defaultFontFamily: '"NeuePlakText-Regular", "Helvetica Neue", Helvetica, Arial, sans-serif',
            datasets: [
                {
                    label: "Critical",
                    data: [],
                    backgroundColor: ['#FF2D00'],
                    barThickness: 10,
                },
                {
                    label: "High",
                    data: [],
                    backgroundColor: ['#FE9600'],
                    barThickness: 10,
                },
                {
                    label: "Medium",
                    data: [],
                    backgroundColor: ['#FEEB00'],
                    barThickness: 10,
                },
                {
                    label: "Low",
                    data: [],
                    backgroundColor: ['#00FE2E'],
                    barThickness: 10,
                },
            ]
        },
        options: {
            legend: {
                position: 'top'
            },
            scales: {
                xAxes: [{
                    ticks: {
                        autoSkip: false
                    },
                    stacked: true
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }

    });
}
var getData_unresolvedalarms = function () {
    
    $.ajax({
        type: 'GET',
        dataType: 'JSON',
        url: '/charts/unresolved_alarms_chart',
        success: function (response) {
            myChart_unresolvedalarmss.data.datasets[0].data = response.critical_values;
            myChart_unresolvedalarmss.data.datasets[1].data = response.high_values;
            myChart_unresolvedalarmss.data.datasets[2].data = response.medium_values;
            myChart_unresolvedalarmss.data.datasets[3].data = response.low_values;
            myChart_unresolvedalarmss.data.labels = response.labels;
            myChart_unresolvedalarmss.update();
        }
    });
}
getData_unresolvedalarms();