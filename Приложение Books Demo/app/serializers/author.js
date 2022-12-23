// import DS from 'ember-data';
import ApplicationSerializer from './application';

export default ApplicationSerializer.extend(/*DS.EmbeddedRecordsMixin,*/ {
  // attrs: {
  //   books: {
  //     serialize: 'records',
  //     deserialize: 'records'
  //   }
  // },

  normalize(model, hash) {
    hash = this._super(...arguments);
    // let hashCopy = Object.assign({}, hash);
    // hashCopy.attributes = {};
    // hashCopy.attributes.firstName = hashCopy.firstName;
    // hashCopy.attributes.lastName = hashCopy.lastName;
    // delete hashCopy.firstName;
    // delete hashCopy.lastName;
    // hash = {
    //   data: hashCopy
    // };

    return hash;
  },


  extractRelationship(relationshipModelName, relationshipHash) {
    return this._super(...arguments);
  }

  // serialize(snapshot, options) {
  //   let json = this._super(...arguments);
  //   json.type = snapshot.modelName;
  //   return json;
  // }
});
