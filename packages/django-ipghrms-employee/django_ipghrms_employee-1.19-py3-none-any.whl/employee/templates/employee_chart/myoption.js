var myoption = {
    tooltips: {
        enabled: true
    },
    hover: {
        animationDuration: 1
    },
    legend: {
        display: false,
        position: 'bottom',
        labels: {
            fontColor: 'rgb(255, 99, 132)'
        }
    },
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true,
                precision: 0
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