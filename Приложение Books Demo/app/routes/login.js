import Route from '@ember/routing/route';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Route.extend(UnauthenticatedRouteMixin, {
  model() {
    return {
      email: '',
      password: ''
    }
  },

  resetController(controller, isExiting, transition) {
    this._super(...arguments);
    if (isExiting) {
      controller.resetErrors();
    }
  }
});
