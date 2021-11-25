// Updates navigation bar with current file path
function populate_nav(curr_dir) {
    let dir_list = curr_dir.split('/');
    let file_nav = document.getElementById("file_nav");
    
    for(let i = 1; i < dir_list.length; i++) {
        let item;
        if(i === 1) {
            item = `<li class="breadcrumb-item text-primary"><a><i class="fas fa-home"></i></a></li>`;
        }
        else if(i === (dir_list.length - 1)) {
            item = `<li class="breadcrumb-item active" aria-current="page"><a>${dir_list[i]}</a></li>`;
        }
        else {
            item = `<li class="breadcrumb-item text-primary"><a>${dir_list[i]}</a></li>`;
        }
        file_nav.innerHTML += item;
    }
}

// add folder button function
function populate_fld_btn(curr_dir) {
    let dir = curr_dir;

    $("#add_folder").click(function () {
        $("#fld_card").css('display', 'block');
        $("#input-name").css('border-color', '#dee2e6');
        $("#ValdtFldName").css('display', 'none');
    });

    $(".btn_close").click(function () {
        $("#fld_card").css('display', 'none');
    });

    $("#btn_submit").click(function () {
        let dir_name = document.getElementById("input-name").value; // Name of the new folder

        if(dir_name === '') {
            $("#input-name").css('border-color', '#fc4d44');
            $("#ValdtFldName").css('display', 'block');
        }
        else {
            send_post_request({dir_name, dir}, "/addFolder");
            document.getElementById("fld_card").style.display = "none";
        }
    });

}

// Delete button
function populate_delete_btn(curr_dir) {

    $(".delete_btn").click(function() {

        // finds the file name
        let file_name = $(this).closest("tr")
                           .find(".name")
                           .text();

        let file = curr_dir + "/" + file_name;
        let path = "/delete";

        swal({
            title: "Are you sure?",
            text: "Once deleted, you will not be able to recover this file!",
            icon: "warning",
            dangerMode: true,
            buttons: true,
        })
        .then((willDelete) => {
          if (willDelete) {
            send_post_request(file, path);
          }
        });
    });
}

function populate_upload_btn(curr_dir) {
    $("#upload_file").click(function() {
        $("#upload_card").css('display', 'block');

        $("#ValdtFile").css('display', 'none');
        $(".custom-file-label").css('border-color', '#dee2e6');

        $(".btn_close").click(function () {
            $("#upload_card").css('display', 'none');
            $("#progress-wrapper").css('display', 'none');
            location.reload();
        });
        const myForm = document.getElementById("myForm");
        const inpFile = document.getElementById("inpFile");

        $("#inpFile").change(function() {
            let file = $("#inpFile").val().split('\\').pop();
            if(file == "")
                $("#inFileLabel").text("Choose a file...");
            else
                $("#inFileLabel").text(file);
        });
        myForm.addEventListener("submit", ev => {
            ev.preventDefault();

            if(inpFile.files.length === 0) {
                $("#ValdtFile").css('display', 'block');
                $(".custom-file-label").css('border-color', '#fc4d44');
            }
            else {

                let file_name = $("#inpFile").val().split('\\').pop();

                $("#myForm").css('display', 'none');
                $("#progress-wrapper").css('display', 'block');
                $(".progress-label").text("Uploading " + file_name);

                let endpoint = window.location.href;
                endpoint = endpoint.substring(0, endpoint.lastIndexOf('/')) + '/browser.html';
                const formData = new FormData();

                let csrftoken = Cookies.get('csrftoken');

                formData.append("inpFile", inpFile.files[0]);
                formData.append("path", curr_dir);

                $.ajax({
                    type:'POST',
                    url: endpoint,
                    enctype: 'multipart/form-data',
                    data: formData,
                    headers: {
                        "X-CSRFToken": csrftoken
                    },
                    beforeSend: function() {

                    },
                    xhr: function() {
                        const xhr = new window.XMLHttpRequest();
                        xhr.upload.addEventListener('progress', e=>{
                            if(e.lengthComputable) {
                                const percent = e.loaded / e.total * 100;
                                $('.progress-bar').css('width', percent + '%');
                                $('#progress').html(percent.toFixed() + ' %');
                            }
                        })
                        $("#cancel").click(function () {
                            $("#progress-wrapper").css('display', 'none');
                            $("#myForm").css('display', 'block');
                            xhr.abort();
                        });
                        return xhr;
                    },
                    success: function(response) {
                        $("#upload_card").css('display', 'none');
                        swal({
                          title: "Done!",
                          text: "file upload successful!",
                          icon: "success",
                          button: "Done",
                        })
                        .then((willDelete) => {
                          location.reload();
                        });
                    },
                    error: function(error) {
                        $("#upload_card").css('display', 'none');
                        swal({
                          title: "Error!",
                          text: "file upload unsuccessful!",
                          icon: "error",
                          button: "Done",
                        })
                        .then((willDelete) => {
                          location.reload();
                        });
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                });
            }
        });
    });
}

function send_post_request(file, path) {
    let url = window.location.href;     // url of current window
    url = url.substring(0, url.lastIndexOf('?')) + path;    // post url
    let csrftoken = Cookies.get('csrftoken');   // csrftoken

    fetch(url, {
        method: "POST",
        body: JSON.stringify({file}),
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }).then(response => location.reload());
}

window.onload = () => {
    let curr_dir = JSON.parse(document.getElementById('curr_path').textContent);
    curr_dir = curr_dir.replaceAll('\\\\','/');
    populate_nav(curr_dir);

    populate_fld_btn(curr_dir);
    
    populate_delete_btn(curr_dir);

    populate_upload_btn(curr_dir);

}