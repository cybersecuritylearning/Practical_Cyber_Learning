$(document).ready(function() {
const buttonDocker = document.getElementById('Instance-btn');
const instance_docker = document.getElementById('Instance-input');

buttonDocker.addEventListener('click', async _ => {
    try {     
          $.ajax({
            type: "POST",
            url: "/home/docker/",
            headers: {
              "X-CSRFToken": getCookie("csrftoken")
            },
            mode: "same-origin",
            data: {
              'con_data': instance_docker.value // from form
            },
            dataType: "json",
            success:
              function (json) {
                M.toast({html: json.status, classes: 'green rounded'});
              }
        });
    }
        catch(err) {
            console.error(`Error: ${err}`);
          }
        });
      });