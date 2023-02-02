import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';
import { compactGuid, createGuid, expandGuid } from 'ember-cli-guid';

export default Route.extend({
  dataService: service('data'),
  model() {
    return {
      guid: createGuid(true),
      x: '88',
      y: '',
      a: '50'
    }},
});
