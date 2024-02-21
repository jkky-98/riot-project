import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MainView from "../views/MainView.vue";

const routes = [
  {
    path: "/",
    name: "login",
    component: HomeView,
    meta: {
      requiresAuth: false,
      title: "Login/SignUp",
      dynamicTitle: "Login/SignUp",
    },
  },
  {
    path: "/mainpage",
    name: "mainpage",
    component: MainView,
    meta: { requiresAuth: true, title: "MainPage", dynamicTitle: "Main" },
    children: [],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
