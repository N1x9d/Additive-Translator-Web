import Component from '@ember/component';
import { computed } from '@ember/object';
import { set } from '@ember/object';


export default Component.extend({
  
  actions: {
       
    async submitForm(e) {
      e.preventDefault();
        console.log(this.get('x'));
        this.onsubmit({
          input: this.input,
          x: this.x,
          y: this.y,
          z: this.z,
          w: this.w,
          p: this.p,
          r: this.r,
          DUF: this.DUF,
          DUT: this.DUT,
          RUF: this.RUF,
          RUT: this.RUT,
          nm: this.nm,
          wm:  this.wm,
          j1:  this.j1,
          j4: this.j4,
          j6: this.j6,
          Arc_disable: this.Arc_disable,
          Auto_arc: this.Auto_arc,
          WELD_SPEED: this.WELD_SPEED,
          WSE: this.WSE,
          WS:  this.WS,
          WEE: this.WEE,
          WE: this.WE,
          RO: this.RO
        });
      console.log(this.input);
    },
    removeFile() {
      set(this, 'uploadData', null);
    },
    didReceiveAttrs() {
      this._super(...arguments);
  
      this.setProperties({
        
        idAuthor: this.get('fanuc.x') ? this.get('fanuc.x') : undefined,
        firstName: this.get('fanuc.y'),
        lastName: this.get('fanuc.z')
      });
    },
      
}
});