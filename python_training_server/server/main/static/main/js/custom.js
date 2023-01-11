
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
                  M.toast({html: 'Great Job!', classes: 'green rounded'});
                  $("#flag").val('');
                  $("#quest_message").html(json.quest);
                  $("#quest_tip").html(json.tips);
                }
              
        });
          } catch(err) {
            console.error(`Error: ${err}`);
          }
        
    });

