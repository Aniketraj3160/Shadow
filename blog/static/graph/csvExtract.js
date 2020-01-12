var csvData;
(function (d3) {
    'use strict';
    d3.csv('dataa.csv')
        .then(data => {
            data.forEach(d => {
                d.case_total=+d.case_total;
            });
        console.log(data)
        Plot(data);
    })
    function Plot(data) {
        csvData=data;
    }
}(d3));