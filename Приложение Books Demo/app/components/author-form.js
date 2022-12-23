import Component from '@ember/component';

export default Component.extend({
  actions: {
    submitForm(e) {
      e.preventDefault();

      this.onsubmit({
        id: this.get('idAuthor'),
        firstName: this.get('firstName'),
        lastName: this.get('lastName')
      });
    }
  },

  didReceiveAttrs() {
    this._super(...arguments);
    // this.set('firstName', this.get('author.firstName'));
    // this.set('lastName', this.get('author.lastName'));

    this.setProperties({
      idAuthor: this.get('author.id') ? this.get('author.id') : undefined,
      firstName: this.get('author.firstName'),
      lastName: this.get('author.lastName')
    });
  },
});
