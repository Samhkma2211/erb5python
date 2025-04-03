$(document).on('click',"#changeBtn", function(){
  if ($("#register").hasClass('d-none')) {
    $("#register").removeClass('d-none');
    $("#login").addClass('d-none');
  } else {
    $("#register").addClass('d-none');
    $("#login").removeClass('d-none');
  }
})