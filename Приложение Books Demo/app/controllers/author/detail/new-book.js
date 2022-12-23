import Controller from '@ember/controller';

export default Controller.extend({
  actions: {
    async saveBook(e) {
      try {
        e.preventDefault();
        let newBook = this.get('store').createRecord('book', this.get('model.book'));
        await newBook.save();

        this.transitionToRoute('author.detail', this.get('model.author.id'));
      }
      catch (e) {
        this.send('error', e);
      }
    }
  }
});
