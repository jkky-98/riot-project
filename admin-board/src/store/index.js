import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  // 상태를 정의합니다.
  plugins: [createPersistedState()],

  state: {
    popStateSignin: false,
    userId: "로그인이 필요합니다.",
    accessToken: "",
    refreshIndex: "",
    isLoggedIn: false,
    userSummoner: "",
  },
  // 상태를 가져오는 getter를 정의합니다.
  getters: {
    getPopState: function (state) {
      return state.popStateSignin;
    },
  },
  // 상태를 변경하는 mutation을 정의합니다.
  mutations: {
    popStateSigninChange: function (state, value) {
      state.popStateSignin = value;
    },
    setUserId: function (state, value) {
      state.userId = value;
    },
    setAccessToken: function (state, value) {
      state.accessToken = value;
    },
    setRefreshIndex: function (state, value) {
      state.refreshIndex = value;
    },
    setIsLoggedIn: function (state, value) {
      state.isLoggedIn = value;
    },
    setUserSummoner: function (state, value) {
      state.userSummoner = value;
    },
  },
  // 비동기 로직을 수행하는 action을 정의합니다.
  actions: {},
  // 모듈을 정의합니다.
  modules: {},
});
