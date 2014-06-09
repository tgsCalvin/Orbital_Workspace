$(document).ready(function(){
  $(".main3").click(function(){
     $(this).toggleClass("main2");
   var currentid = $(this).attr('id');  
    if ($("#updown"+currentid).text() == "-")
    {
     $("#updown"+currentid).text("+");
    }
    else
       $("#updown"+currentid).text("-");
         $("#under"+currentid).slideToggle("fast");
  }); 
});
