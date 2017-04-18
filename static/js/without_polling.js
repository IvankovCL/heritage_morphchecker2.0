$(document).ready(function () {
	document.title = 'Morphchecker';
	$("#clean").click(function() {
		document.getElementById("textInput").value = '';
		document.getElementById("textOutput").innerHTML = '';
		document.getElementById("openFile").value = '';
	});
	$("#textInput").keydown(function () {
		document.getElementById("textOutput").innerHTML = '';	
	});
	$("#send").click(function() {
		$.post('/data', $("#textInput").val(), function(data) {
			document.getElementById("textOutput").innerHTML = data.result
		});
	});
});