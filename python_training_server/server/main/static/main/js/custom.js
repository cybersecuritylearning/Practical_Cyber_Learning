
    const button = document.getElementById('Flag-btn');
    var flag_input = document.getElementById('flag');

    button.addEventListener('click', async _ => {
        try {     
              $.ajax({
                type: "POST",
                url: "/home/learn/",
                headers: {
                  "X-CSRFToken": getCookie("csrftoken")
                },
                mode: "same-origin",
                data: {
                  'Flag': flag_input.value // from form
                },
                success:function(json){
                  
                  $("#flag").val('');
                  $("#quest_message").html(json.quest);
                  $("#quest_tip").html(json.tips);
                  try {
                    if (json.fail){
                    M.toast({html: json.fail, classes: 'red rounded'});
                    }
                    else{
                    M.toast({html: 'Great Job!', classes: 'green rounded'});  
                    }
                  }
                  catch(err) {
                    console.log("It's correct");
                  }

                }
              
        });
          } catch(err) {
            console.error(`Error: ${err}`);
          }
        
    });

    const prev = document.getElementById('prev');
    prev.addEventListener('click', async _ => {
      try {     
            $.ajax({
              type: "GET",
              url: "/home/move/",
              mode: "same-origin",
              data: {
                'pos': 'prev' // from form
              },
              success:function(json){
                $("#flag").val('');
                $("#quest_message").html(json.quest);
                $("#quest_tip").html(json.tips);
              }
            
      });
        } catch(err) {
          console.error(`Error: ${err}`);
        }
      
  });

  const next = document.getElementById('next');
  next.addEventListener('click', async _ => {
    try {     
          $.ajax({
            type: "GET",
            url: "/home/move/",
            mode: "same-origin",
            data: {
              'pos': 'next' // from form
            },
            success:function(json){
              $("#flag").val('');
              $("#quest_message").html(json.quest);
              $("#quest_tip").html(json.tips);
            }
          
    });
      } catch(err) {
        console.error(`Error: ${err}`);
      }
    
});


