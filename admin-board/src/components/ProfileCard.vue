<template>
  <v-card class="mx-auto" max-width="434" rounded="0">
    <v-img
      height="100%"
      src="https://cdn.vuetifyjs.com/images/cards/server-room.jpg"
      cover
    >
      <v-avatar color="grey" rounded="0" size="150">
        <v-img :src="iconUrl" cover></v-img>
      </v-avatar>
      <v-list-item
        class="text-white"
        :subtitle="'Level: ' + level"
        :title="'소환사명: ' + name"
      ></v-list-item>
      <v-divider thickness="20"></v-divider>
      <v-btn active color="primary" @click="Update">Update</v-btn>
    </v-img>
  </v-card>
</template>

<script>
import axiosInstance from "../setaxios.js";
import { mapState } from "vuex";
export default {
  data: () => ({
    name: "",
    level: "",
    icon: "",
    iconUrl: "",
  }),
  computed: {
    ...mapState(["userId", "userSummoner"]),
  },
  methods: {
    Update() {
      axiosInstance
        .post("http://localhost:8000/api/update/", {
          userId: this.userId,
        })
        .then((res) => {
          console.log(res.data);
          this.name = res.data.name;
          this.level = res.data.summonerLevel;
          this.icon = res.data.profileIconId;
          this.iconUrl = "../assets/profileicon/" + this.icon + ".png";
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
