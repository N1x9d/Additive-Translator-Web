import Route from '@ember/routing/route';

export default Route.extend({
  beforeModel(transition) {
    let chi = transition.router.currentHandlerInfos;
    let currentRouteName = this.get('routeName');
    let prevRouteName = '';
    if (chi && chi.length > 0) {
      let lastRouteName = chi[chi.length - 1].name;
      prevRouteName = lastRouteName === 'loading' ? chi[chi.length - 2].name : lastRouteName;
    }

    if (prevRouteName != currentRouteName && prevRouteName !== 'application') {
      transition.promise.then(() => {
        this.send('refreshAuthors');
      });
    }
  }
});
