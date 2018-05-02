function trainhistory_chart(url, renderTo) {
    $.getJSON(url, function(data) {
        Highcharts.chart(renderTo, {
            title: {
                text: 'Train-history'
            },
            tooltip: {
                crosshairs: true,
                shared: true,
                valueDecimals: 4,
                valueSuffix: ''
            },
            legend: {
                enabled: true
            },
            xAxis: {
                crosshair: true,
                title: {
                    text: 'Epoch'
                }
            },
            yAxis: [{
                title: {
                    text: 'Loss'
                }
            }, {
                opposite: true,
                title: {
                    text: 'Acc'
                }
            }],
            series: data.series,
        });
    });
}
