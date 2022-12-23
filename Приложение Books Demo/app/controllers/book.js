import { computed } from '@ember/object';
import Controller from '@ember/controller';

export const PER_PAGE = 2;

export default Controller.extend({
  queryParams: ['search', 'page', 'author'],
  search: '',
  page: 1,
  author: '',

  pages: computed('model.books.meta.total', function() {
    const total = Number(this.get('model.books.meta.total'));
    if (Number.isNaN(total) || total <= 0) {
      return [];
    }

    return new Array(Math.ceil(total / PER_PAGE))
      .fill()
      .map((value, index) => index + 1);
  }),

  selectedAuthor: computed('author', function() {
    const author = this.get('author');

    return author ? this.get('model.authors').findBy('id', author) : null;
  }),

  actions: {
    changeAuthor(author) {
      this.set('author', author ? author.get('id') : '');
    }
  }
});
