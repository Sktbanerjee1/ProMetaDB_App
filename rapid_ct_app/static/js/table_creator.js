$(document).ready(function () {
    $('#bleed-table').DataTable({
        "info": false,
        scrollY:"350px",
    });
} );


$(document).ready(function () {
    $('#control-table').DataTable({
        "info": false,
        scrollY:"350px",
    });
} );


$(document).ready(function () {
    var datatable = $('#lesion-table').DataTable({
        scrollY:"350px",
        "info": false,
        "scrollX": true
    });
    
} );
