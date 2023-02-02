import Component from '@ember/component';
import { computed } from '@ember/object';
import { set } from '@ember/object';


export default Component.extend({
  A: '',
  B: '',
  W: '',
  actions: {
       
    async submitForm(e) {
      e.preventDefault();
        this.onsubmit({
          input: this.input,
          x: this.x,
          y: this.y,
          z: this.z,
          w: this.w,
          p: this.p,
          r: this.r,
          A: this.A,
          W: this.W,
          B: this.B,
          PUF: this.PUF,
          PUT: this.PUT,
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
    },
    
    changeWrist(value) {
        this.W = value
        console.log(this.W)
    },

    changeArm(value) {
        this.A = value
        console.log(this.W)
    },
    changeBase(value) {
        this.B = value
        console.log(this.W)
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