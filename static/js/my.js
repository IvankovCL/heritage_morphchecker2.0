// DOM is ready
$(document).ready(function () {
	$("#send").click(function() {
		$.post('/data', $('#txtInput').val(), function(data) {
			$('#txtOutput').val(data.answer)
		});
	});
});
	
		
var toggle = function() {
  var mydiv = document.getElementById('demoForm');
  if (mydiv.style.display === 'block' || mydiv.style.display === '')
    mydiv.style.display = 'none';
  else
    mydiv.style.display = 'block'
  }