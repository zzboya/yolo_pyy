import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "index",
    component: () => import("../views/home.vue"),
    meta: {
      requireLogin: true
  }
  },

  {
    path: "/login",
    name: "login",
    component: () => import("../views/login.vue"),
  },
  {
    path:'/layout',
    component:()=>import('../views/layout'),
    redirect:'/layout/index',
    children:[
      // 首页
      {
        path:'/layout/index',
        component:()=>import('../views/home.vue'),
        meta: {
          requireLogin: true
      }
      },
      // 图像增强
      {
        path:'/layout/imageprocessing',
        name: "imageprocessing",
        component:()=>import('../views/imageProcessing.vue'),
        meta: {
          requireLogin: true
            }
      },
        // 历史查询
      {
        path:'/layout/history',
        name: "history",
        component:()=>import('../views/dataHistory.vue'),
        meta: {
          requireLogin: true
            }
      },
      // 个人信息修改
      {
        path: "/layout/profile",
        name: "profile",
        component: () => import("../views/profile.vue"),
        meta: {
          requireLogin: true
      }
      },

    ]
  },
  
];

const router = new VueRouter({
  routes,
});
router.beforeEach((to, from, next) => {
  var token = sessionStorage.getItem('token');
  if (to.matched.some(record => record.meta.requireLogin) &&!token) {
    // console.log('No token');
    next({ name: 'login', query: { to: to.path } });
  } else {
    // console.log('beforeEachtoken');
    next()
  }
})
const VueRouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push (to) {
  return VueRouterPush.call(this, to).catch(err => err)
}
export default router;
