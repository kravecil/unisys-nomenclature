import 'vite/modulepreload-polyfill';

import '@/bootstrap';


import 'quasar/src/css/index.sass'
import quasarIconSet from 'quasar/icon-set/svg-material-icons'
import '@quasar/extras/material-icons/material-icons.css'
import quasarLang from 'quasar/lang/ru'
import { matAllInbox } from '@quasar/extras/material-icons'

import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import { Quasar, Loading, Dialog, Notify, Cookies } from 'quasar'

import '@/assets/css/app.sass'
import 'animate.css'

import App from '@/App.vue'
import routes from '@/routes.js'
import { authenticate, authenticated, unauthenticate } from '@/api/auth.js'

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to) => {
  if (!authenticated.value) unauthenticate()
})

authenticate()
.then(() => {
  createApp(App)
    .use(Quasar, {
      plugins: { Loading, Notify, Dialog, Cookies },
      iconSet: quasarIconSet,
      lang: quasarLang,
    })
    .use(router)
    .mount('#app')
})
