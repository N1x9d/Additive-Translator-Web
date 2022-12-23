import Component from '@ember/component';
import { inject as service } from '@ember/service';

export default Component.extend({
  store: service(),
  currentUser: service(),

  actions: {
    async saveBook(e) {
      e.preventDefault();
      this.get('onSubmit')({
        title: this.get('title'),
        isbn: this.get('isbn'),
        publishDate: this.get('publishDate'),
        author: this.get('author'),
        user: this.get('currentUser.user')
      });
    },

    searchAuthor(query) {
      return this.get('store').query('author', { q: query })
    }
  },

  didReceiveAttrs() {
    this.setProperties({
      title: this.get('book.title'),
      isbn: this.get('book.isbn'),
      publishDate: this.get('book.publishDate'),
      author: this.get('book.author')
    });
  },
});
