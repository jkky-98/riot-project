import store from "./store/index";

export function setInterceptors(instance) {
  // axios interceptors 설정
  instance.interceptors.request.use(
    function (config) {
      // 토큰을 헤더에 추가
      const accessToken = store.state.accessToken;
      config.headers["Authorization"] = `${accessToken}`;
      config.headers["refreshIndex"] = store.state.refreshIndex;
      return config;
    },
    function (error) {
      // 요청 에러 처리
      return Promise.reject(error);
    }
  );

  // 응답 받기 전 인터셉터
  instance.interceptors.response.use(
    function (response) {
      return response;
    },
    function (error) {
      return Promise.reject(error);
    }
  );

  // 인터셉터가 정의된 인스턴스 반환
  return instance;
}
