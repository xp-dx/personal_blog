// function deleteToUrl(path, params, method) {
//     method = method || "delete"; // Устанавливаем метод отправки.

//     var form = document.createElement("form");
//     form.setAttribute("method", method);
//     form.setAttribute("action", path);
//     for(var key in params) {
//         var hiddenField = document.createElement("input");
//         hiddenField.setAttribute("type", "hidden");
//         hiddenField.setAttribute("name", key);
//         hiddenField.setAttribute("value", params[key]);

//         form.appendChild(hiddenField);
//     }

//     document.body.appendChild(form);
//     form.submit();
// }
document.querySelectorAll('.delete-link').forEach(link => {
    link.addEventListener('click', async event => {
      event.preventDefault();
      const articleId = link.dataset.articleId;
      const response = await fetch(`/delete/${articleId}/`, {
        method: 'DELETE',
      });
      if (response.ok) {
        // handle success
      } else {
        // handle error
      }
    });
  });