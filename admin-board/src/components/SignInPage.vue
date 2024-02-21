<template>
  <v-card
    flat
    class="mx-auto"
    max-width="800"
    v-if="this.$store.getters.getPopState"
    theme="dark"
    color="indigo"
  >
    <v-card-title class="text-center">Sign In</v-card-title>
    <v-alert v-if="isSignUpSuccessful" type="success" title="회원가입 성공">{{
      this.signUpText
    }}</v-alert>
    <v-alert v-if="signUpError" type="error" title="회원가입 실패">{{
      this.signUpText
    }}</v-alert>
    <v-col>
      <v-form style="width: 400px; height: 300px">
        <div class="mx-3">
          <v-icon icon="md:home"></v-icon>
          userId
          <div class="mx-1">
            <v-text-field
              placeholder="userId"
              v-model="userId"
              required
              :rules="userIdRules"
            ></v-text-field>
          </div>
        </div>
        <div class="mx-3">
          <v-icon color="black" size="30px">lock</v-icon>
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

        <v-btn color="green" dark large block @click="SignUpSubmit"
          >회원가입완료</v-btn
        >
        <v-card flat> </v-card>
      </v-form>
    </v-col>
    <v-btn @click="closeModal()" color="gray" theme="dark">닫기!</v-btn>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  methods: {
    closeModal() {
      this.$store.commit("popStateSigninChange", false);
    },
    SignUpSubmit() {
      console.log("회원가입시도중");
      const userSignUpData = {
        userId: this.userId,
        userPassword: this.userPassword,
        email: "",
      };
      axios
        .post("http://localhost:8000/api/signup/", userSignUpData)
        .then((response) => {
          console.log("회원가입 성공:", response.data);
          this.isSignUpSuccessful = true;
          this.signUpText = "회원가입 성공";

          // 성공한 경우 처리
        })
        .catch((error) => {
          console.error("회원가입 실패:", error.response.data);
          this.signUpError = true;
          this.signUpText = error.response.data.error;
          // 실패한 경우 처리
        });
    },
  },
  data: () => ({
    userId: "",
    userPassword: "",
    isSignUpSuccessful: false,
    signUpError: false,
    signUpText: "",
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
  }),
};
</script>

<style></style>
