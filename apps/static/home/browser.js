function populate_nav(curr_dir) {
    var dir_list = curr_dir.split('\\\\');
    var file_nav = document.getElementById("file_nav");

    for(let i = 1; i < dir_list.length; i++) {
        var item;

        if(i === 1) {
            item = `<li class="breadcrumb-item"><a href="#"><i class="fas fa-home"></i></a></li>`;
        }
        else if(i === (dir_list.length - 1)) {
            item = `<li class="breadcrumb-item active" aria-current="page"><a href="#">${dir_list[i]}</a></li>`;
        }
        else {
            item = `<li class="breadcrumb-item"><a href="#">${dir_list[i]}</a></li>`;
        }
        file_nav.innerHTML += item;
    }
}

function populate_fld_btn(curr_dir) {
    let dir = curr_dir;

    document.getElementById("add_folder").addEventListener("click", function () {
        document.getElementById("fld_card").style.display = "block";
    });

    document.getElementById("btn_close").addEventListener("click", function () {
        document.getElementById("fld_card").style.display = "none";
    });

    document.getElementById("btn_submit").addEventListener("click", function () {
        var dir_name = document.getElementById("input-name").value; // Name of the new folder
        let url = window.location.href;
        url = url.substring(0, url.lastIndexOf('/')) + "/addFolder";    // post url
        let csrftoken = Cookies.get('csrftoken');   // csrftoken

        fetch(url, {
            method: "POST",
            body: JSON.stringify({dir_name, dir}),
            headers: {
                "X-CSRFToken": csrftoken,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
            .then(response => location.reload())

        document.getElementById("fld_card").style.display = "none";
    });

}

function populate_delete_btn(curr_dir) {

    $(".delete_btn").click(function() {
        let file_name = $(this).closest("tr")   // Finds the closest row <tr>
                           .find(".name")     // Gets a descendent with class="nr"
                           .text();         // Retrieves the text within <td>

        let file = curr_dir + "\\\\" + file_name;
        console.log(file)

        $("#dlt_card").css('display', 'block');

        $("#delete_cancel").click(function (){
            document.getElementById("dlt_card").style.display = "none";
        });

        $("#delete_confirm").click(function (){
            let url = window.location.href;
            url = url.substring(0, url.lastIndexOf('/')) + "/delete";    // post url
            let csrftoken = Cookies.get('csrftoken');   // csrftoken

            fetch(url, {
                method: "POST",
                body: JSON.stringify({file}),
                headers: {
                    "X-CSRFToken": csrftoken,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then(response => location.reload())

            $("#dlt_card").css('display', 'none');
        });

    });
}

window.onload = () => {

    const curr_dir = JSON.parse(document.getElementById('curr_path').textContent);

    populate_nav(curr_dir);

    populate_fld_btn(curr_dir);
    
    populate_delete_btn(curr_dir);

}