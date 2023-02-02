import Controller from '@ember/controller';
import { inject as service } from '@ember/service';

export default Controller.extend({
  dataService: service('data'),
  actions: {
    async saveAuthor(author) {
      let authorModel = this.get('model');
      authorModel.set('firstName', author.firstName);
      authorModel.set('lastName', author.lastName);

      await authorModel.save();

      this.transitionToRoute('author.index');
    }
  }
});
