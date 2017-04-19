$(document).ready(function () {
	
	document.title = "Morphchecker";
	
	$("#help").click(function() {
		window.alert("Для проверки введите текст в поле слева или выберите файл в формате txt. Нажмите 'Проверить'. \nКогда проверка будет закончена, в поле справа появится проверенный текст. \nСлова, содержащие ошибки, будут подсвечены красным цветом.\nВарианты исправления можно увидеть, наведя курсор на интересующее слово.\nПоследовательности символов, содержащие латиницу или цифры обработаны не будут.");
	});
	
	$("#clean").click(function() {
		document.getElementById("textInput").value = '';
		document.getElementById("openFile").value = '';
		cleanOutput();
	});
	
	$("#textInput").keydown(function (e) {
		if(e.which == 8 || e.which == 46){ 
			document.getElementById("openFile").value = '';
			cleanOutput();
		}			
	});
	
	$("#send").click(function() {
		document.getElementById("textOutput").innerHTML = 'Проверка началась. Это займёт некоторое время...';
		document.title = "Идёт проверка...";
		disableAll();
		$.post('/data', $("#textInput").val(), function(data) {
			if (data.to_show == "none") {
				document.title = "Morphchecker";
				window.alert("В ходе проверки что-то пошло не так!");
				document.getElementById("textOutput").innerHTML = '';
				enableAll();
			} else {
				document.getElementById("textOutput").innerHTML = data.to_show;
				document.title = "Morphchecker";
				window.alert("Текст проверен!");
				resultToSave = data.to_save;
				document.getElementById("saveFile").disabled = false;
				enableAll();
			}
		});
	});
	
	var control = document.getElementById("openFile");
	control.addEventListener("change", function(event) {
		var i = 0,
			files = control.files,
			len = files.length;         
		for (; i < len; i++) {
			if (files[i].type.match('text/plain')) {            
				var reader = new FileReader();
				reader.onload = function(event) {
					var contents = event.target.result;
					document.getElementById("textInput").value = contents;
					cleanOutput();					
				}; 
				reader.onerror = function(event) {
					console.error("Файл не может быть прочитан! код " + event.target.error.code);
				};
				reader.readAsText(files[i]);
			} else {
				window.alert('Поддерживаются только файлы в формате txt');
				document.getElementById("openFile").value = '';
			}
		}
	}, false);	
	
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
	
	function disableAll() {
		document.getElementById("textInput").readOnly = true;
		document.getElementById("send").disabled = true;
		document.getElementById("clean").disabled = true;
		document.getElementById("openFile").disabled = true;
	}

	function enableAll() {
		document.getElementById("textInput").readOnly = false;
		document.getElementById("send").disabled = false;
		document.getElementById("clean").disabled = false;
		document.getElementById("openFile").disabled = false;
	}
	
	function cleanOutput() {
		document.getElementById("textOutput").innerHTML = '';
		document.getElementById("saveFile").disabled = true;
	}
	
});