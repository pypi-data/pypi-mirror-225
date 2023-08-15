{% load static %}
var endpoint = '/api/employee/all/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        label= data.label,
        all= data.tot,
        male= data.male,
        female= data.female,
        science= data.science,
        notscience= data.notscience,
        setFlowAllEmp()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setFlowAllEmp(){

    Highcharts.chart('setFlowAllEmp', {
        chart: {
          height: 500,
          color: 'white',
          inverted: true
        },
      
        title: {
          text: 'TOTAL FUNSIONARIO IPG TIMOR LESTE'
        },
      
        accessibility: {
          point: {
            descriptionFormatter: function (point) {
              var nodeName = point.toNode.name,
                nodeId = point.toNode.id,
                nodeDesc = nodeName === nodeId ? nodeName : nodeName + ', ' + nodeId,
                parentDesc = point.fromNode.id;
              return point.index + '. ' + nodeDesc + ', reports to ' + parentDesc + '.';
            }
          }
        },
      
        series: [{
          type: 'organization',
          name: 'Total Funsionario',
          keys: ['from', 'to'],
          data: [
            ['Male', 'ALL'],
            ['Female', 'ALL'],
            ['ALL', 'SCIENCE'],
            ['ALL', 'NONSCIENCE'],
          ],
          levels: [
      
          {
            level: 0,
            color: 'white',
            dataLabels: {
              color: 'black',
              fontSize: '16px',
              style: {
                fontSize: '16px'
              }
            },
            height: 25,
          }, 
      
          {
            level: 1,
            color: '#0879ff',
            height: 25,
            
          }, 
      
          {
            level: 2,
            color: 'white',
            height: 25,
            dataLabels: {
              color: 'black',
              fontSize: '14px',
              style: {
                fontSize: '14px'
              }
            },
          }, 
        ],
        
          nodes: [
            
          {
            id: 'Male',
            name: male,
            title: 'MALE',
            image: '{% static 'main/images/man.png' %}',
            borderColor: 'black',
            
          }, {
            id: 'Female',
            name: female,
            title: 'FEMALE',
            image: '{% static 'main/images/female.png' %}',
            borderColor: 'black',
          }, 
          
          
          {
            id: 'ALL',
            name:  all + ' ALL STAFF',
            image: '{% static 'main/images/all.png' %}',
            
          }, 
          
          
          {
            id: 'NONSCIENCE',
            title: 'NON SCIENCE',
            name: notscience,
            image: '{% static 'main/images/computer.png' %}',
            borderColor: 'black',
          }, {
            id: 'SCIENCE',
            title: 'SCIENCE',
            name: science,
            image: '{% static 'main/images/science.png' %}',
            borderColor: 'black',
            labelColor: 'green'
          }, 
        ],
      
      
          colorByPoint: false,
          dataLabels: {
            color: 'white',
            
          style: {
            fontSize: '26px'
          }
          },
          borderColor: 'black',
          nodeWidth: 85,
        
          
        }
      ],
        tooltip: {
          outside: true
        },
        exporting: {
          allowHTML: true,
          sourceWidth: 800,
          sourceHeight: 600
        },
        credits: {
              enabled: false
        }
      
      });
}


