var gender_myoption = {
    tooltips: {
        enabled: true
    },
    hover: {
        animationDuration: 1
    },
    legend: {
        display: true,
        position: 'bottom',
        labels: {
            fontColor: 'rgba(132, 138, 240, 0.75)'
        }
    },
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
    },
    animation: {
        duration: 1,
        onComplete: function () {
            var chartInstance = this.chart,
            ctx = chartInstance.ctx;
            ctx.textAlign = 'center';
            ctx.fillStyle = "rgba(0, 0, 0, 1)";
            ctx.textBaseline = 'bottom';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index];
                    ctx.fillText(data, bar._model.x, bar._model.y - 0);

                });
            });
        }
    },
    layout: {
        padding: {
            left: 10, right: 10, top: 20, bottom: 10
        }
    }
};

var genderbgColors = [
        'rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)', 'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'
];

var endpoint1 = '/api/employee/u/dep/gender/'
$.ajax({
    method: "GET",
    url: endpoint1,
    success: function(data){
        const data1 = {
            labels: data.label,
            datasets: [{
                label: 'Generu',
                data: data.obj,
                backgroundColor: genderbgColors,
                borderWidth: 1
            }]
        };
        
        const config_gen = {
            type: 'pie',
            data: data1,
            options: gender_myoption
        };
        const genderChart_data1 = new Chart(
            document.getElementById('genderChart_data1'),
            config_gen
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
