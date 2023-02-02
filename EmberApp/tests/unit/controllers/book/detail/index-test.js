import { module, test } from 'qunit';
import { setupTest } from 'ember-qunit';

module('Unit | Controller | book/detail/index', function(hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function(assert) {
    let controller = this.owner.lookup('controller:book/detail/index');
    assert.ok(controller);
  });
});
