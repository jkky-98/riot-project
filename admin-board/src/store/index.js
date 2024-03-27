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
    summonerProfile: {},
    championUsed: {},
    matchData: {},
  },
  // 상태를 가져오는 getter를 정의합니다.
  getters: {
    getPopState: function (state) {
      return state.popStateSignin;
    },
    getisLoggedIn: function (state) {
      return state.isLoggedIn;
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
    setSummonerProfile: function (state, value) {
      state.summonerProfile = value;
    },
    setChampionUsed(state, championUsed) {
      // total을 기준으로 정렬
      const dataArray = Object.entries(championUsed);
      dataArray.sort((a, b) => b[1].total - a[1].total);
      state.championUsed = dataArray;
    },
    setMatchData(state, matchData) {
      state.matchData = matchData;
    },
  },
  // 비동기 로직을 수행하는 action을 정의합니다.
  actions: {},
  // 모듈을 정의합니다.
  modules: {},
});
