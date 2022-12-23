import ApplicationSerializer from './application';

export default ApplicationSerializer.extend({
  normalize(model, hash) {
    hash = this._super(...arguments);
    return hash;
  },
});
