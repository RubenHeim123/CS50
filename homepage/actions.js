let globalEmail = ''
let globalPassword = ''

document.querySelector('#auth_form').addEventListener('submit', function(event){
    event.preventDefault();

    let email = document.getElementById('typeEmailX').value;
    let pwd = document.getElementById('typePasswordX').value;
    let result = document.getElementById('signup_result');

    if (email == 'johndoe@email.com' && pwd == '123')
    {
        window.location.replace('http://127.0.0.1:8080/index.html')
        result.textContent = '';
    } else {
        result.textContent = 'Wrong email or password';
        result.style.backgroundColor = 'red';
    }
});
