import Component from '@ember/component';

export default Component.extend({  

  actions: {
    updateValue: function(value) {
      console.log(value);
    },
    
  }
});
