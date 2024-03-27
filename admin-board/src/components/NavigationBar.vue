<template>
  <v-app-bar app color="#26293C">
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    <v-toolbar-title>
      {{ $route.meta.dynamicTitle }}
    </v-toolbar-title>
    <v-spacer></v-spacer>
  </v-app-bar>
  <v-navigation-drawer v-model="drawer" app color="#26293C">
    <v-list-item>
      <v-list-item-title class="text-h5 white--text">
        Only Solo Rank
      </v-list-item-title>
      <v-list-item-subtitle class="white--text">
        Hello Summoners!
      </v-list-item-subtitle>
    </v-list-item>
    <v-card class="mx-auto" max-width="344" color="indigo-darken-3">
      <v-card-item>
        <div>
          <div class="text-h6 mb-1">회원정보</div>
          <div class="text-h6">ID : {{ userId }}</div>
          <div class="text-h6">계정연동 :{{ userSummoner }}</div>
        </div>
      </v-card-item>

      <v-card-actions>
        <riot-register />
        <v-btn @click="Logout"> Logout </v-btn>
      </v-card-actions>
    </v-card>
    <v-divider thickness="10"></v-divider>
    <v-card class="mx-auto" max-width="344" color="indigo-darken-3">
      <v-card-actions>
        <v-btn @click="$router.push('/mainpage')">
          Analyze your solo rank!
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-navigation-drawer>

  <v-divider></v-divider>
</template>

<script>
import { mapState } from "vuex";
import axiosInstance from "../setaxios.js";
import RiotRegister from "./RiotRegister.vue";

export default {
  name: "NavigationBar",
  data: () => ({
    drawer: false,
  }),
  computed: {
    ...mapState(["userId", "userSummoner"]),
  },
  methods: {
    Logout() {
      console.log("Logout try..");
      const axiosInstanceLogout = axiosInstance;
      console.log(axiosInstanceLogout.defaults.headers);
      axiosInstanceLogout
        .post("http://localhost:8000/api/auth/", { userId: this.userId })
        .then((res) => {
          console.log(res.data);
          this.$swal
            .fire({
              title: `Good Bye ${this.userId}!`,
              confirmButtonText: "Success Logout!",
            })
            .then((result) => {
              /* Read more about isConfirmed, isDenied below */
              if (result.isConfirmed) {
                this.$swal.fire("Logout Success!", "", "success");
              }
            });
          // 기본 path로 이동
          this.$router.push("/");
          // 인증 정보 삭제
          this.$store.commit("setUserId", "");
          this.$store.commit("setAccessToken", "");
          this.$store.commit("setRefreshIndex", "");
          this.$store.commit("setIsLoggedIn", false);
          this.$store.commit("setUserSummoner", "");
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  components: {
    RiotRegister,
  },
};
</script>
