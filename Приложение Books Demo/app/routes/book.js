import RSVP from 'rsvp';
import Route from '@ember/routing/route';

import { PER_PAGE } from '../controllers/book';

export default Route.extend({
  queryParams: {
    search: {
      refreshModel: true
    },
    page: {
      refreshModel: true
    },
    author: {
      refreshModel: true
    }
  },

  model({ search, page, author }) {
    const query = {
      _page: page,
      _limit: PER_PAGE,
    };

    if (search) {
      query.q = search;
    }

    if (author) {
      query.author = author;
    }

    return RSVP.hash({
      authors: this.store.findAll('author'),
      books: this.store.query('book', query),
    });
  },

  actions: {
    loading() {
      return false;
    }
  }
});
