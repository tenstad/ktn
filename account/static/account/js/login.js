$(function() {

  $('.submit').click(function(){
    $('form').submit();
  });

  $("#id_username").keypress(function(event) {
    if (event.which == 13) {
      event.preventDefault();
      $("#id_password").focus();
    }
  });
  
  $("#id_password").keypress(function(event) {
    if (event.which == 13) {
      event.preventDefault();
      $('form').submit();
    }
  });

});
