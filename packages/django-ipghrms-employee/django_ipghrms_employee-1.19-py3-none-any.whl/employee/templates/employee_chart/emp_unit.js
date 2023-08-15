
var endpoint = '/api/employee/unit/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        d = data,
        obj = data.obj
        legend = data.label
        dt = data.datas
        setEmpDivision()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setEmpDivision(){
    Highcharts.chart('setEmpDivision', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'DISTRIBUISAUN FUNSIONARIO TUIR DIVIZAUN',
            align: 'center'
        },
        tooltip: {
            formatter: function () {
                return this.point.name + ': ' + this.y;
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '{point.name}: {point.y}'
                }
            }
        },
        credits: {
              enabled: false
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: dt
        }]
    });


}



