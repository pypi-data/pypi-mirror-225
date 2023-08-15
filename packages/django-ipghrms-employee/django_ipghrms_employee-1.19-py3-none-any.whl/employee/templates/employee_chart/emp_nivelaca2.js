
var endpoint = '/api/employee/nivelaca/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        legend = data.label
        dt = data.obj
        categories = data.label2
        setEmpNivelAca2()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setEmpNivelAca2(){
    Highcharts.chart('nivelacaChart_data1', {
        
        chart: {
            type: 'bar'
        },
        title: {
            align: 'center',
            text: 'IPG All Staff Education Qualification'
        },
        subtitle: {
        },
        accessibility: {
            announceNewData: {
                enabled: true
            }
        },
        xAxis: {
            categories: categories,
            title: {
                text: null
            },
            
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Staff',
                align: 'high'
            },
            allowDecimals: false,
            labels: {
                formatter: function () {
                    return this.value; // Return the original value
                }
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
        credits: {
            enabled: false
        },
    
        tooltip: {
            formatter: function () {
                return this.point.name + ': ' + this.y;
            }
        },
    
        series: [
            {
                name: "Ekipa",
                colorByPoint: true,
                data:dt
            }
        ],
        drilldown: {
            breadcrumbs: {
                position: {
                    align: 'right'
                }
            },
            series: [
            ]
        }
    });


}









