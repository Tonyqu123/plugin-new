// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import daoStyle from 'dao-style-vue';
import Vue from 'vue';
import VueResource from 'vue-resource';
import lodash from 'lodash';
import store from 'store';
import App from './App';
import router from './router';

import '../node_modules/dao-style-vue/styles/dao-style.css';
import '../node_modules/noty/lib/noty.css';

Vue.config.productionTip = false;
Vue.use(VueResource);
Vue.use(daoStyle);

Object.defineProperty(Vue.prototype, '$lodash', { value: lodash });

Vue.http.interceptors.push((request, next) => {
  const token = store.get('DCE_TOKEN');
  // const token = JSON.parse(store.get('DCE_TOKEN'));
  if (token) {
    Vue.http.headers.common.Authorization = token;
    Vue.http.headers.common['X-DCE-Access-Token'] = token;
  } else {
    delete Vue.http.headers.common.Authorization;
  }
  next(response => response);
});

// Vue.http.options.emulateJSON = true;
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
});
