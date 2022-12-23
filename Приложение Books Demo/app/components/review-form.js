import Component from '@ember/component';
import { inject as service } from '@ember/service';

export default Component.extend({
  moment: service(),
  currentUser: service(),

  didInsertElement() {
    this.set('body', this.get('review.body'));
  },

  actions: {
    async saveReview(e) {
      e.preventDefault();

      this.get('onSubmit')({
        user: this.get('currentUser.user.username'),
        body: this.get('body'),
        createdAt: this.get('moment').moment(new Date()).format('YYYY-MM-DD'),
        book: this.get('review.book')
      });
    }
  }
});
