// DOM is ready


$(document).ready(function () {
	$("#send").click(function() {
		$.post('/data', $('#txtInput').val(), function(data) {
			$('#txtOutput').val(data.answer)
		});
	});
});
    
$(document).ready(function() {
	$('#demoForm').hide()
});

$('input[name=demo]').click(function ()
     {
         $(this).hide();
		 $('#demoForm').show()
     }
);


