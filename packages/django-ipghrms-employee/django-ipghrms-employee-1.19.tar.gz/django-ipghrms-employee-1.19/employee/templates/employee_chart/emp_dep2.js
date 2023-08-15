

var endpoint = '/api/employee/dep/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = 'All Staff By TEAM'
        categories = data.label
        setEmpDep()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setEmpDep(){
    const chart = new Highcharts.Chart({
        chart: {
            renderTo: 'depChart_data',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 15,
                depth: 50,
                viewDistance: 25
            }
        },
        xAxis: {
            categories: categories
        },
        yAxis: {
            title: {
                enabled: false
            }
        },
        tooltip: {
            headerFormat: '<b>{point.key}</b><br>',
            pointFormat: 'Total Funsionario: {point.y}'
        },
        title: {
            text: legend
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
        series: [{
            data: obj,
            colorByPoint: true
        }]
    });
    
    function showValues() {
        document.getElementById('alpha-value').innerHTML = chart.options.chart.options3d.alpha;
        document.getElementById('beta-value').innerHTML = chart.options.chart.options3d.beta;
        document.getElementById('depth-value').innerHTML = chart.options.chart.options3d.depth;
    }
    
    // Activate the sliders
    document.querySelectorAll('#sliders input').forEach(input => input.addEventListener('input', e => {
        chart.options.chart.options3d[e.target.id] = parseFloat(e.target.value);
        showValues();
        chart.redraw(false);
    }));
    
    showValues();


}




