
var endpoint = '/api/employee/age/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = data.label
        age2=data.age2
        title = data.title
        empChart()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function empChart(){
    Highcharts.chart('ageChart_data', {
        chart: {
            type: 'cylinder',
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 15,
                depth: 50,
                viewDistance: 50
            }
        },
        title: {
            text: title
        },
        xAxis: {
            categories: legend,
            title: {
                text: 'Age groups'
            }
        },
        yAxis: {
            title: {
                margin: 20,
                text: 'Total Staff'
            }
        },
        tooltip: {
            headerFormat: '<b>Age: {point.x}</b><br>'
        },
        plotOptions: {
            series: {
                depth: 25,
                colorByPoint: true,
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            data: age2,
            name: 'Total Staff',
            showInLegend: false

        }]
    });


}




