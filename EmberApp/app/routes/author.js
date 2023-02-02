import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';
import { Promise } from 'rsvp';
import { later } from '@ember/runloop';
// import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Route.extend({
  dataService: service('data'),
  queryParams: {
    search: {
      refreshModel: true
    }
  },
  model({ search }) {
    // let promise = new Promise((resolve, reject) => {
    //   later(async () => {
    //     try {
    //       let authors = search ? await this.get("dataService").getAuthors(search) : await this.get("dataService").getAuthors();
    //       resolve(authors);
    //     }
    //     catch (e) {
    //       reject('Connection failed');
    //     }
    //   }, 1000);
    // }).
    // then((authors) => {
    //   this.set('controller.model', authors);
    // }).
    // finally(() => {
    //   if (promise === this.get('modelPromise')) {
    //     this.set('controller.isLoading', false);
    //   }
    // });

    // this.set('modelPromise', promise);
    // return { isLoading: true };
    return this.get('store').findAll('author');
  },

  setupController(controller, model) {
    this._super(...arguments);
    // if (this.get('modelPromise')) {
    //   controller.set('isLoading', true);
    // }
  },


  // resetController(controller, isExiting, transition) {
  //   this._super(...arguments);
  //   if (isExiting) {
  //     controller.set('isLoading', false);
  //     this.set('modelPromise', null);
  //   }
  // },

  actions: {
    refreshAuthors() {
      // this.refresh();
    },
    // loading(transition, originRoute) {
    //   return false;
    // }
  }
});
