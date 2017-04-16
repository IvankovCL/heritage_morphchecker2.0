$(document).ready(function () {    
    $('#demoButton').click(function () {
         $(this).hide();
         $('#demoForm').show();
    });    
    $('#demoForm').hide();    
    $("#txtInput").focus(function () {
        $('#txtOutput').val('')
    });    
    $("#send").click(function() {
        $.post('/data', $('#txtInput').val(), function(data) {
            $('#txtOutput').val(data.result)
        });
    });     
});
