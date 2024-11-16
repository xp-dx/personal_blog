document.querySelectorAll('.delete-link').forEach(link => {
  link.addEventListener('click', async event => {
    event.preventDefault();
    const articleId = link.dataset.articleId;
    if (confirm('Are you sure you want to delete this article?\nThis action cannot be undone.')) {
      const response = await fetch(`/delete/${articleId}/`, {
        method: 'DELETE',
      });
      if (response.ok) {
        link.closest('.article_container').remove();
        // document.querySelector('.article_container').remove();
        // handle success
      } else {
        console.error('Article deletion error:', response.status, response.statusText);
        if (response.status == 404){
          alert('Error deleting article. Article not found.');
        }
        alert('Error deleting article. More details in the console.');
        // handle error
        }
    }
  });
});