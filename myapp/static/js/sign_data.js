    // 登录功能
document.getElementById('login-submit').addEventListener('click', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username_login').value;
    const password = document.getElementById('password_login').value;

    // 前端验证
    if (!username.trim() || !password.trim()) {
        showError('login-form', '账号和密码不能为空');
        return;
    }

    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (response.ok) {
            window.location.href = '/home'; // 登录成功跳转
        } else {
            showError('login-form', data.message || '登录失败');
        }
    } catch (error) {
        showError('login-form', '网络请求失败');
    }
});

// 注册功能
document.getElementById('register-submit').addEventListener('click', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username_register').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password_register').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // 前端验证
    const errors = [];
    if (!username.trim()) errors.push('用户名不能为空');
    if (!validateEmail(email)) errors.push('邮箱格式不正确');
    if (password.length < 8) errors.push('密码至少8位');
    if (password !== confirmPassword) errors.push('两次密码不一致');

    // console.log("changdu " + password.length)
    // console.log("un " + username)
    // console.log("pa " + password)
    // console.log("em " + email)
    // console.log("cm " + confirmPassword)




    if (errors.length > 0) {
        showError('register-form', errors.join('<br>'));
        return;
    }

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();
        if (response.ok) {
            showSuccess('register-form', '注册成功，即将跳转...');
            setTimeout(() => window.location.href = '/home', 1500);
        } else {
            showError('register-form', data.message || '注册失败');
        }
    } catch (error) {
        showError('register-form', '网络请求失败');
    }
});

// 工具函数
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showError(formId, message) {
    const form = document.getElementById(formId);
    let errorBox = form.querySelector('.error-message');
    if (!errorBox) {
        errorBox = document.createElement('div');
        errorBox.className = 'alert alert-danger error-message';
        form.prepend(errorBox);
    }
    errorBox.innerHTML = message;
}

function showSuccess(formId, message) {
    const form = document.getElementById(formId);
    let successBox = form.querySelector('.success-message');
    if (!successBox) {
        successBox = document.createElement('div');
        successBox.className = 'alert alert-success success-message';
        form.prepend(successBox);
    }
    successBox.innerHTML = message;
}