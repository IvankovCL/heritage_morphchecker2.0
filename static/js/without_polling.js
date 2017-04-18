$(document).ready(function () {
	document.title = "Morphchecker";
	saveButton = document.getElementById("saveFile");
	$("#clean").click(function() {
		document.getElementById("textInput").value = '';
		document.getElementById("textOutput").innerHTML = '';
		document.getElementById("openFile").value = '';
		saveButton.disabled = true;
	});
	$("#textInput").keydown(function () {
		document.getElementById("textOutput").innerHTML = '';
		saveButton.disabled = true;		
	});
	$("#send").click(function() {
		document.getElementById("textOutput").innerHTML = 'Проверка началась. Это займёт некоторое время...';
		document.title = "Идёт проверка...";
		$.post('/data', $("#textInput").val(), function(data) {
			if (data.to_show == "none") {
				document.title = "Morphchecker";
				window.alert("В ходе проверки что-то пошло не так!");
				document.getElementById("textOutput").innerHTML = '';
			} else {
				document.getElementById("textOutput").innerHTML = data.to_show;
				document.title = "Morphchecker";
				window.alert("Текст проверен!");
				resultToSave = data.to_save;
			}
		});
	});
	$("body").on('DOMSubtreeModified', "#textOutput", function() {
		saveButton.disabled = false;		
	});
	$("#saveFile").click(function() {
		  var blob = new Blob([resultToSave], {
			"type": "application/json"
		  });
		  var a = document.createElement("a");
		  a.download = 'mchecked.txt';
		  a.href = URL.createObjectURL(blob);
		  document.body.appendChild(a);
		  a.click();
		  document.body.removeChild(a);
	});
});