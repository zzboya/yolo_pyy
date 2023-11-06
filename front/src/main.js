import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import VueAppend from 'vue-append'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';


Vue.use(ElementUI);
Vue.config.productionTip = false;


import axios from "axios"
const baseUrl = "/";
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
axios.defaults.baseURL = baseUrl
axios.defaults.withCredentials=true;

// Add a request interceptor
axios.interceptors.request.use(function (config) {
  // 在发送请求之前做些什么
  if   (config.url.indexOf("login") == -1) {  //不是登录
    var token = sessionStorage.getItem('token');
    if(token) {
      config.headers.Authorization = token;
    } else {
      router.push("login")
      // window.location.href= "/";
    }
  } 
  return config;
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

// Add a response interceptor
axios.interceptors.response.use(function (response) {
  // Do something with response data

    return response;
  
});
Vue.prototype.$http  = axios;

Vue.config.productionTip = false
Vue.use(VueAppend)
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
