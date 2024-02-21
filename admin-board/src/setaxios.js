import Axios from "axios";
import { setInterceptors } from "./interceptor.js";
import store from "./store/index";
import router from "./router";

// Axios 인스턴스 생성
const axiosInstance = Axios.create({
  baseURL: "http://localhost:8000",
});

setInterceptors(axiosInstance);

// 토큰 인증 //
axiosInstance
  .post("http://localhost:8000/api/auth/")
  .then((response) => {
    const { message, new_token } = response.data;
    if (message === "token is valid") {
      console.log("Token is valid");
    } else if (message === "token is expired") {
      console.log("Token is expired");
      store.commit("setAccessToken", new_token);
    } else if (message === "refresh token is expired, need to login") {
      console.log("Refresh token is expired, need to login");
      router.push({ path: "/" });
    }
  })
  .catch((error) => {
    console.error("Error while token verification:", error);
  });

export default axiosInstance; // Axios 인스턴스
