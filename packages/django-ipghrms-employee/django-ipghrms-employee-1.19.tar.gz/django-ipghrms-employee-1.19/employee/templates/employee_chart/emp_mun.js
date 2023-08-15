



var endpoint = '/api/employee/mun/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        legend = data.label
        dt = data.obj
        obj = data.data2
        empMunChart2()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function empMunChart2(){
    Highcharts.chart('munChart_data', {
        chart: {
          type: 'pie',
          options3d: {
            enabled: true,
            alpha: 45
          }
        },
        title: {
          text: 'IPG Staff Based on Municipality',
          align: 'center'
        },
        plotOptions: {
          pie: {
            innerSize: 100,
            depth: 45
          }
        },
        credits: {
          enabled: false
      },
        series: [{
          name: 'Municipality',
          data: obj
        }]
      });


}










