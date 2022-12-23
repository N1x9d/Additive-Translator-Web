import Controller from '@ember/controller';
import { inject as service } from '@ember/service';

export default Controller.extend({
  dataService: service('data'),
  actions: {
    async saveAuthor(author) {
      let newAuthor = this.get('store').createRecord('author', author);
      newAuthor.serialize();
      await newAuthor.save();

      this.transitionToRoute('author.index');
    },
  }
});
