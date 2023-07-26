const signin = document.querySelector("#signin")
const signup = document.querySelector("#signup")
const signinbtn = document.querySelector("#signinbtn")
const signupbtn = document.querySelector("#signupbtn")
const container = document.querySelector(".container")
signup.addEventListener("click",()=>{
    container.classList.add("sign-up-mode")
});
signin.addEventListener("click",()=>{
    container.classList.remove("sign-up-mode")
})
signupbtn.addEventListener("click",()=>{
    container.classList.add("sign-up-mode2")
});
signinbtn.addEventListener("click",()=>{
    container.classList.remove("sign-up-mode2")
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        username: formData.get('username'),
        password: formData.get('password')
    };
    fetch('/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            alert('Login successful');
        } else {
            alert('Invalid credentials');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        username: formData.get('username'),
        email:formData.get("email"),
        password: formData.get('password')
    };
    fetch('/signup',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});