
var endpoint = '/api/employee/age/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = data.label
        setEmpAge()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setEmpAge(){
    Highcharts.chart('setEmpAge', {
        chart: {
            type: 'column'
        },
        title: {
            align: 'center',
            text: 'DISTRIBUISAUN FUNSIONARIO TUIR IDADE'
        },
        accessibility: {
            announceNewData: {
                enabled: true
            }
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'Total Funsionario'
            }
    
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        },
    
        tooltip: {
            formatter: function () {
                return this.point.name + ': ' + this.y;
            }
        },
        credits: {
                enabled: false
        },
    
        series: [
            {
                name: "Browsers",
                colorByPoint: true,
                data: obj
            }
        ],
        drilldown: {
            breadcrumbs: {
                position: {
                    align: 'right'
                }
            },
            series: []
        }
    });


}




