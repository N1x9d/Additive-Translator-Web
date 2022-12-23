import DS from 'ember-data';

export default DS.Model.extend({
  user: DS.attr('string'),
  body: DS.attr('string'),
  createdAt: DS.attr('date-string'),

  book: DS.belongsTo('book')
});
