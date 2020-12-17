Chart.defaults.global.responsive = true;

//dashboard/"cve Types"
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
    ctx.onclick = function (e) {
        var slice = myChart_anomalytypes.getElementAtEvent(e);
        if (!slice.length) return; // return if not clicked on column
        var clickedElementindex = slice[0]["_index"];
        var anomaly = myChart_anomalytypes.data.labels[clickedElementindex];
        location.href = "/anomalies/createdAt:[NOW-1DAY TO NOW] AND anomalyType:" + anomaly;

    }
}
var getData_severitytypes = function () {
    
    $.ajax({
        type: 'GET',
        dataType: 'JSON',
        url: '/charts/get_cve_types_chart',
        success: function (response) {
            console.log(response.values)
            myChart_severitytypes.data.datasets[0].data = response.values;
            myChart_severitytypes.data.labels = response.labels;
            myChart_severitytypes.update();
        }
    });
}
getData_severitytypes();