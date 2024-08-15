function login() {
    window.location.replace("/login")
}

function sign_in() {
    let username = $("#input-username").val();
    let password = $("#input-password").val();

    if (username === "") {
        $("#help-id-login").text("Please input your id.");
        $("#input-username").focus();
        return;
    } else {
        $("#help-id-login").text("");
    }

    if (password === "") {
        $("#help-password-login").text("Please input your password.");
        $("#input-password").focus();
        return;
    } else {
        $("#help-password-login").text("");
    }

    console.log(username, password);
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password,
        },
        success: function (response) {
            if (response["result"] === "success") {
                $.cookie("mytoken", response["token"], { path: "/" });
                window.location.replace("/admin");
            } else {
                alert(response["msg"]);
            }
        },
    });
}

function toggle_kembali() {
    window.location.replace('/')
}

function clearInputs() {
    $("#input-username").val("");
    $("#input-password").val("");
    $("#input-password2").val("");
}

function sign_out() {
    // Menghapus cookie dengan nama "mytoken"
    $.removeCookie("mytoken", { path: "/" });

    // Menampilkan SweetAlert2 di tengah layar
    Swal.fire({
        position: "center", // Menempatkan SweetAlert di tengah layar
        icon: "success",
        title: "Anda berhasil logout",
        showConfirmButton: false,
        timer: 1500
    });

    // Mengalihkan pengguna ke halaman login setelah logout
    setTimeout(function () {
        window.location.href = "/login";
    }, 2000); // Memberikan waktu untuk melihat alert sebelum mengalihkan halaman
}
