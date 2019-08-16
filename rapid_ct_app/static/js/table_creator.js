$(document).ready(function () {
    $('#bleed-table').DataTable({
        scrollY:"450px",
        "columnDefs": [
            {"className": "dt-center", "targets": "_all"}
        ]
    });
} );


$(document).ready(function () {
    $('#control-table').DataTable({
        scrollY:"450px",
        "columnDefs": [
            {"className": "dt-center", "targets": "_all"}
        ]
    });
} );


$(document).ready(function () {
    var datatable = $('#others-table').DataTable({
        scrollY:"450px",
        "columnDefs": [
            {"className": "dt-center", "targets": "_all"}
          ]
    });
    
} );
