import Component from '@ember/component';

export default Component.extend({
  actions: {
    login(e) {
      e.preventDefault();

      this.get('onSubmit')({
        email: this.email,
        password: this.password
      });
    }
  },

  didReceiveAttrs() {
    this.setProperties({
      email: this.get('user.email'),
      password: this.get('user.password')
    });
  }
});
