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

        // display confirmation popup
        $("#dlt_card").css('display', 'block');

        $("#delete_cancel").click(function (){
            document.getElementById("dlt_card").style.display = "none";
        });

        // Makes post request on confirmation
        $("#delete_confirm").click(function (){
            send_post_request(file, path);

            $("#dlt_card").css('display', 'none');
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
                let endpoint = window.location.href;
                endpoint = endpoint.substring(0, endpoint.lastIndexOf('/')) + '/browser.html';
                const formData = new FormData();

                formData.append("inpFile", inpFile.files[0]);
                formData.append("path", curr_dir);
                let csrftoken = Cookies.get('csrftoken');

                fetch(endpoint, {
                    method: "post",
                    body: formData,
                    headers: {
                        "X-CSRFToken": csrftoken
                    }
                }).then(r => location.reload()).catch(console.error);
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