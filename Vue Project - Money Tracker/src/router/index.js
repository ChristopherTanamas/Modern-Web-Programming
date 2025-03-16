import { createRouter, createWebHistory } from 'vue-router';
import RegisterPage from '../components/RegisterPage.vue';
import LoginPage from '../components/LoginPage.vue';
import WorkSpace from '../components/WorkSpace.vue';
import NewTransaction from '../components/NewTransaction.vue';

const routes = [
  { path: '/register', 
    name:'Register',
    component: RegisterPage 
    },
  { path: '/', 
    name: 'Login',
    component: LoginPage },
  { path: '/workspace', 
    name: 'Workspace',
    component: WorkSpace},
  { 
    path: '/newtransaction', 
    name: 'NewTransaction',
    component: NewTransaction,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;