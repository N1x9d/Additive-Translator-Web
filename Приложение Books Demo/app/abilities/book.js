import { computed } from '@ember/object';
import { Ability } from 'ember-can';
import { inject as service } from '@ember/service';
import { Promise } from 'rsvp';

export default Ability.extend({
  currentUser: service(),
  session: service(),

  // only the person who wrote a post can edit it
  canEdit: computed(function () {
    if (!this.get('session.isAuthenticated')) {
      return false;
    }

    return new Promise((resolve, reject) => {
      return this.get('model.user').then((user) => {
        resolve(user.get('username') === this.get('currentUser.user.username'));
      }).catch(() => {
        reject(false);
      });
    });

  }).volatile()
});
