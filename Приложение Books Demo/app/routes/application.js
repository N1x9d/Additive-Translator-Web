import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';
import ApplicationRouteMixin from 'ember-simple-auth/mixins/application-route-mixin';

export default Route.extend(ApplicationRouteMixin, {
  session: service(),
  currentUser: service(),

  beforeModel() {
    this._super(...arguments);

    //this.loadUser();
  },

  // sessionAuthenticated() {
  //   this._super(...arguments);

  //   this.loadUser();
  // },

  

  loadUser() {
    if (this.get('session.isAuthenticated')) {
      this.get('currentUser').load();
    }
  },

  actions: {
    error(error, transition) {
      if (transition) {
        transition.abort();
      }
      this.intermediateTransitionTo('error', { error: error.message});
      return true;
    }
  }
});
