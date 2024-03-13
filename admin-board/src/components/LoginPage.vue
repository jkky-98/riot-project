<template>
  <v-app id="app">
    <v-main>
      <div class="background-container">
        <v-container
          fluid
          fill-height
          class="d-flex justify-center align-center mt-12"
        >
          <v-layout row wrap class="text-xs-center align-self-center mt-12">
            <v-card
              flat
              class="mx-auto pa-12"
              max-width="auto"
              v-if="!$store.getters.getPopState"
              theme="dark"
              color="#26293C"
            >
              <v-card-title class="text-center" color="white"
                >League of Legend Solo Rank Analysis</v-card-title
              >
              <v-row style="margin-top: 60px">
                <v-col>
                  <v-form style="width: 400px; height: 300px">
                    <div class="mx-3">
                      userId
                      <div class="mx-1">
                        <v-text-field
                          placeholder="userId"
                          v-model="userId"
                          :rules="userIdRules"
                          required
                        ></v-text-field>
                      </div>
                    </div>
                    <div class="mx-3">
                      userPassword
                      <div class="mx-1">
                        <v-text-field
                          placeholder="userPassword"
                          type="password"
                          v-model="userPassword"
                          :rules="passwordRules"
                          required
                        ></v-text-field>
                      </div>
                    </div>

                    <v-btn color="#2c4f91" dark large block @click="Login"
                      >Login</v-btn
                    >
                    <v-card flat>
                      <v-btn
                        color="#3FB17D"
                        dark
                        large
                        block
                        @click="goToSignUp"
                        >Sign Up</v-btn
                      >
                    </v-card>
                  </v-form>
                </v-col>
              </v-row>
            </v-card>
            <SignInPage />
          </v-layout>
        </v-container>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import SigninPage from "../components/SignInPage.vue";
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      userId: null,
      userPassword: null,
      userIdRules: [
        // 사용자 입력 유효성 검사를 위한 규칙
        (v) => !!v || "아이디를 입력하세요", // 필수 입력 여부 확인
        (v) => /^[a-zA-Z0-9]*$/.test(v) || "영어 문자와 숫자만 입력하세요", // 정규 표현식을 이용한 유효성 검사
      ],
      passwordRules: [
        // 사용자 입력 유효성 검사를 위한 규칙
        (v) => !!v || "패스워드를 입력하세요", // 필수 입력 여부 확인
        (v) =>
          /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(
            v
          ) ||
          "영어 문자, 숫자, 특수 문자(@$!%*?&)를 포함하여 8자 이상 입력하세요", // 정규 표현식을 이용한 유효성 검사
      ],
    };
  },
  methods: {
    loginSubmit() {
      this.$store.dispatch("login", {
        userId: this.userId,
        userPassword: this.userPassword,
      });
    },
    goToSignUp() {
      this.$store.commit("popStateSigninChange", true);
      console.log(this.$store.state.popStateSignin);
    },
    async Login() {
      try {
        const response = await axios.post("http://localhost:8000/api/login/", {
          username: this.userId,
          password: this.userPassword,
          email: "",
        });
        console.log(response.data.message);
        const accessToken = response.data.accessToken; // access 토큰
        const refreshIndex = response.data.refreshIndex; // refresh index
        const riotID = response.data.riot_id; // riot id
        // 리프레시 인덱스를 로컬 스토리지에 저장

        // vuex에 저장
        this.$store.commit("setUserId", this.userId);
        this.$store.commit("setAccessToken", accessToken);
        this.$store.commit("setRefreshIndex", refreshIndex);
        this.$store.commit("setIsLoggedIn", true);
        this.$store.commit("setUserSummoner", riotID);
        //Swal 이라고 쓰지말고 vue에서는 this.$ 를 붙여야 한다.
        this.$swal
          .fire({
            title: `Hello ${this.userId}!`,
            confirmButtonText: "GOGO",
          })
          .then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
              this.$swal.fire("Login Success!", "", "success");
            }
          });
        this.$router.push({ name: "mainpage" }); // 다음 페이지의 이름으로 네비게이션
        // 로그인 성공 시
      } catch (error) {
        console.error(error);
        // 로그인 실패 시
      }
    },
  },
  components: {
    SignInPage: SigninPage,
  },
};
</script>

<style>
.background-container {
  /* 배경 이미지 설정 */
  background-image: url("../assets/login_background_image.jpg");
  /* 배경 이미지가 전체를 덮도록 설정 */
  background-size: cover;
  /* 배경 이미지가 중앙에 위치하도록 설정 */
  background-position: center;
  /* 배경 이미지를 고정 */
  background-attachment: fixed;
  /* 배경 이미지가 컨테이너 내에서 잘리지 않도록 설정 */
  min-height: 100vh;
  /* 다른 요소들을 위에 놓도록 설정 */
  z-index: -1;
}
</style>
