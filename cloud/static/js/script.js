$(document).ready(function(){

  function refreshFunc() {
     $.getJSON('/instance',function(data){update_values(data);} );
  }

  timeint = setInterval(refreshFunc, 3000);

  function update_values(data){
    $.each(data, function(index, element) {
    if (index=='b1' || index=='b2' || index=='f1' || index=='ai' )
    {
      if(element==1)
      {
        $("input[name='"+ index +"']").prop('checked', true);
      } 
      else{
        $("input[name='"+ index +"']").prop('checked', false);        
      }     
    }else{
      $("#"+index).html(element);
    }
    });
  }


$("input[type='checkbox']").change(function()
{
  $val=$(this).is(":checked") ? 1 : 0;
  if(this.name=="all" && $val )
  {
    $("input[name='b1']").prop('checked', true);
    $("input[name='b2']").prop('checked', true);
    $("input[name='f1']").prop('checked', true);
    all("1");
  }
  else if(this.name=="all" && !($val) )
  {
    $("input[name='b1']").prop('checked', false);
    $("input[name='b2']").prop('checked', false);
    $("input[name='f1']").prop('checked', false);
    all("0");
  }
});

function all(status)
{
    $.get("/req",
      {
        bname: 'b1',
        bstatus: status
      });
      $.get("/req",
      {
        bname: 'b2',
        bstatus: status
      });
      $.get("/req",
      {
        bname: 'f1',
        bstatus: status
      });
}

$("input[type='checkbox']").change(function()
{
  if(this.name != "all" && this.name !="simulate" && this.name !="insert" )
  {
      $val=$(this).is(":checked") ? 1 : 0;
       $.get("/req",
      {
        bname: this.name,
        bstatus: $val
      });
  }

});

$("input[name='simulate']").change(function()
{
    if($(this).is(":checked") ? 1 : 0)
    {
      $.get("/req_rasp",
      {
        l: $("input[name='l_in']").val(),
        m: $("input[name='m_in']").val(),
        m2: $("input[name='m2_in']").val(),
        t: $("input[name='t_in']").val(),
        c: $("input[name='c_in']").val(),
        h: $("input[name='h_in']").val()
      }).done(function(){
        alert('Initialising Simulation..');
        $.get("/predict").done(function() 
        {
          alert('Simulation complete!');
          $("input[name='simulate']").prop('checked', false);
        });
      });


    }   
});

$("input[name='insert']").change(function()
{
    if($(this).is(":checked") ? 1 : 0)
    {
      $.get("/req_rasp",
      {
        l: $("input[name='l_in']").val(),
        m: $("input[name='m_in']").val(),
        m2: $("input[name='m2_in']").val(),
        t: $("input[name='t_in']").val(),
        c: $("input[name='c_in']").val(),
        h: $("input[name='h_in']").val()
      }).done(function(){
      alert('Processing data!');
      $.get("/insert").done(function() 
        {
          alert('Insertion complete!');
          $("input[name='insert']").prop('checked', false);
        });
    });

    }   
});

});
