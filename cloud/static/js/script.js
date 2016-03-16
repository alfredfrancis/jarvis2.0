$(document).ready(function(){

  $.getJSON('switch.json', { get_param: 'value' },function(data){update_values(data);} );

  function update_values(data){
    $.each(data, function(index, element) {
      if(element==1)
      {
        $("input[name='"+ index +"']").prop('checked', true);
      }
    });
  }

  $( this ).load( "weather.php", function( response) {
    var array = response.split(',');
     $('#temp').html(array[0]+"°C");
     $('#weather').html(array[1]);
});

$("input[type='checkbox']").change(function()
{
  $val=$(this).is(":checked") ? 1 : 0;
  if(this.name=="all" && $val )
  {
    $("input[name='l1']").prop('checked', true);
    $("input[name='l2']").prop('checked', true);
    $("input[name='f1']").prop('checked', true);
    all("1");
  }
  else if(this.name=="all" && !($val) )
  {
    $("input[name='l1']").prop('checked', false);
    $("input[name='l2']").prop('checked', false);
    $("input[name='f1']").prop('checked', false);
    all("0");
  }
});
function all(status)
{
    $.post("switch.php",
      {
        bname: 'l1',
        bstatus: status
      });
      $.post("switch.php",
      {
        bname: 'l2',
        bstatus: status
      });
      $.post("switch.php",
      {
        bname: 'f1',
        bstatus: status
      });
}

$("input[type='checkbox']").change(function()
{
  if(this.name!="all")
  {
      $val=$(this).is(":checked") ? 1 : 0;
       $.post("switch.php",
      {
        bname: this.name,
        bstatus: $val
      });
  }

});



});
