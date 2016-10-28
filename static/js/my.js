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
			polling(data.task_id);
        });
    });
    
    var polling = function (task_id) {
    $.get('/result/' + task_id, function (data) {
      if (data.ready) {
          var result = data.result;
          $('#txtOutput').val(data.result);
          alert('Готово!');
      } else {
          alert('Ищем ошибки...');
          setTimeout(function () {
              polling(task_id);
              }, 1000);
     }
     }); 
     };
     

     
});
