
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: "/",
        name: "Home",
        component: () => import('pages/Home.vue'),
        props: true
      },
      {
          path: "/article/:id",
          name: "ArticleDetail",
          component: () => import('pages/ArticleDetail.vue'),
          props: true
      },
      {
          path: "/Login",
          name: "Login",
          component: () => import('pages/Login.vue'),
          props: true
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes

