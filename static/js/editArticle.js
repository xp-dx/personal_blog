const form = document.querySelector('.articles_card form');

const titleInput = document.querySelector('.title.data');
const dateInput = document.querySelector('.date.data');
const contentInput = document.querySelector('.content.data');

form.addEventListener('submit', (e) => {
e.preventDefault();

const url = new URL(window.location.href);
const articleId = url.pathname.split('/').pop();
const title = titleInput.value;
const created_at = dateInput.value;
const content = contentInput.value;

fetch('/edit/' + articleId, {
    method: 'PATCH',
    headers: {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `title=${title}&created_at=${created_at}&content=${content}`,
})
.then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })

.then((data) => {
    alert('Article updated successfully!');
    console.log(data);
  })
.catch((error) => {
    alert('Error updating article. More details in the console.');
    console.error(error);
  });
});