import Component from '@ember/component';
import fetch from 'fetch';

import ENV from 'books-demo/config/environment';

export default Component.extend({
  iAmRobot: true,
  reset: false,

  actions: {
    async saveUser(e) {
      e.preventDefault();

      this.get('onSubmit')({
        email: this.email,
        username: this.username,
        password: this.password,
        passwordConfirmation: this.passwordConfirmation
      });
    },

    async verified(key) {
      try {
        const { success } = await (await fetch(`${ENV.backendURL}/recaptcha?key=${key}`)).json();

        this.set('iAmRobot', !success);
      } catch (error) {
        this.set('reset', true);
      }
    },

    expired() {
      this.set('iAmRobot', true);
    }
  },

  didReceiveAttrs() {
    this.setProperties({
      email: this.get('user.email'),
      username: this.get('user.username'),
      password: this.get('user.password'),
      passwordConfirmation: this.get('user.passwordConfirmation'),
    });
  }
});
