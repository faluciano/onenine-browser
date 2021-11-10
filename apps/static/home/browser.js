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
    var dir = curr_dir;

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

window.onload = () => {

    const curr_dir = JSON.parse(document.getElementById('curr_path').textContent);

    populate_nav(curr_dir);

    populate_fld_btn(curr_dir);

}