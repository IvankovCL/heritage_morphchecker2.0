$(document).ready(function () {
	document.title = 'Morphchecker';
	$('#demoButton').click(function () {
		 $(this).hide();
		 $('#demoForm').show();
	});
	$('#demoForm').hide();
	if ($("#textInput").val() == '') {
		document.getElementById("textOutput").innerHTML = '';
	}
	$("#send").click(function() {
		$.post('/data', $('#textInput').val(), function(data) {
			document.getElementById("textOutput").innerHTML = data.result
		});
	});
});