// change_info.js
function selectAvatar(url) {
    document.getElementById('avatarPreview').src = url;
    document.getElementById('selectedAvatar').value = url;
    $('#avatarModal').modal('hide');
}

function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function() {
        document.getElementById('avatarPreview').src = reader.result;
        document.getElementById('selectedAvatar').value = '';
    }
    reader.readAsDataURL(event.target.files[0]);
}

document.getElementById('profileForm').addEventListener('submit', function(e) {
    const username = document.getElementById('username').value.trim();
    const errorElement = document.getElementById('usernameError');

    if (!username) {
        e.preventDefault();
        errorElement.textContent = '用户名不能为空';
    } else {
        errorElement.textContent = '';
    }
});