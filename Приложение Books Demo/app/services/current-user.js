import Service from '@ember/service';
import { inject as service } from '@ember/service';

export default Service.extend({
  store: service(),
  user: null,

  async load() {
    let user = await this.get('store').queryRecord('user', { me: true });
    this.set('user', user);
  },

  resetCurrentUser() {
    this.set('user', null);
  }
});
