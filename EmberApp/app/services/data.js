import Service from '@ember/service';
import ENV from 'books-demo/config/environment';

export default Service.extend({
  getAuthors(search) {
    let queryParams = '';
    if (search) {
      queryParams=`?q=${search}`;
    }

    return fetch(`${ENV.backendURL}/Parse${queryParams}`).then((response) => response.json());
  },

  getAuthor(id) {
    return fetch(`${ENV.backendURL}/authors/${id}`).then((response) => response.json());
  },

  deleteAuthor(author) {
    return fetch(`${ENV.backendURL}/authors/${author.id}`, { method: 'DELETE'});
  },

  SengToParce(author,guid) {
    console.log(author);
    let url = new URL(`http://localhost/api/Parse`);
    var data = { "id" : guid };
    for (let k in data) { url.searchParams.append(k, data[k]); }
    return fetch(url, {
      method: 'POST',
      crossorigin: true,    
      mode: 'no-cors',   
      origin: `${ENV.backendURL}`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf8'
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
      body: JSON.stringify(author.json)
    });
  }
});
