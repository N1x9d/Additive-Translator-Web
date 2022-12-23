import Component from '@ember/component';
import { inject as service } from '@ember/service';

export default Component.extend({
  store: service(),

  init() {
    this._super(...arguments);
    this.setProperties({
      showModal: false,
      author: {
        firstName: '',
        lastName: ''
      }
    });
  },

  actions: {
    async save(e) {
      e.preventDefault();

      let newAuthor = this.get('store').createRecord('author', this.author);
      await newAuthor.save();

      this.set('showModal', false);
      this.get('onSave')(newAuthor);
    }
  }
});
