var endpoint = '/api/leave/emp/leave/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        categories = data.categories
        al = data.al
        sicleave = data.sicleave,
        spleave = data.spleave,
        matleave = data.matleave,
        patleave = data.patleave,
        chileave = data.chileave,

        lenged = data.legend
        setEmpLeave()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setEmpLeave(){

Highcharts.chart('allEmpLeave_chart', {
    chart: {
        type: 'bar',
        height: 700,
    },
    title: {
        text: lenged
    },
    xAxis: {
        categories: categories
    },
    series: [
        { name: 'Annual Leave', data: al }, 
        { name: 'Sick Leave', data: sicleave },
        { name: 'Special Leave', data: spleave },
        { name: 'Maternity Leave', data: matleave },
        { name: 'Paternity Leave', data: patleave },
        { name: 'Childcare Leave', data: chileave },
    ],
    credits: {
        enabled: false
    }
});
}

