import Service from '@ember/service';
import ENV from 'books-demo/config/environment';

export default Service.extend({
  getAuthors(search) {
    let queryParams = '';
    if (search) {
      queryParams=`?q=${search}`;
    }

    return fetch(`${ENV.backendURL}/authors${queryParams}`).then((response) => response.json());
  },

  getAuthor(id) {
    return fetch(`${ENV.backendURL}/authors/${id}`).then((response) => response.json());
  },

  deleteAuthor(author) {
    return fetch(`${ENV.backendURL}/authors/${author.id}`, { method: 'DELETE'});
  },

  SengToParce(author) {
    console.log(author);
    return fetch(`${ENV.backendURL}/authors`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(author)
    });
  },

  updateAuthor(author) {
    return fetch(`${ENV.backendURL}/authors/${author.id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(author)
    });
  }
});
