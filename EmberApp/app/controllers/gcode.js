import Controller from "@ember/controller";
import { inject as service } from '@ember/service';

export default Controller.extend({
  dataService: service('data'),

  actions: {
      async sendGcode(gcode) {

        
        let authorModel = this.get('model');
      try {
        console.log(gcode);
        await this.get("dataService").SengToParce(gcode,authorModel.guid);
      }
      catch(e) {
        console.log(e);
        e.user = authorModel;
        this.send('error', e);
      } 
        
      },
  }
});