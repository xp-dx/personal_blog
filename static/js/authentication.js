// static/js/authentication.js

// Make an API call to the /users/me/ endpoint
const authHeader = 'Bearer ' + localStorage.getItem('access_token')
console.log('Token:', authHeader);
fetch('/admin', {
  method: 'GET',
  headers: {
    'Authorization': authHeader
  }
})
.then(response => response.text())
.then(html => {
  document.body.innerHTML = html;
})
.catch(error => console.error(error));
  