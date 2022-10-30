
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
        });
          } catch(err) {
            console.error(`Error: ${err}`);
          }
    });
