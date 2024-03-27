<template>
  <v-container>
    <v-card class="mx-auto" max-width="434" rounded="0" color="#26293C">
      <v-avatar color="grey" rounded="0" size="150">
        <v-img :src="this.summonerProfile.iconUrl" cover></v-img>
      </v-avatar>
      <v-list-item
        class="text-white"
        :subtitle="'Level: ' + this.summonerProfile.level"
        :title="'소환사명: ' + this.summonerProfile.name"
      >
        <span class="tagname">#{{ tagname }}</span></v-list-item
      >
      <v-container class="pa-2">
        <v-btn active color="indigo-darken-3" @click="Update" :loading="loading"
          >Update
          <template v-slot:loader>
            <v-progress-linear indeterminate></v-progress-linear>
          </template>
        </v-btn>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import axiosInstance from "../setaxios.js";
import { mapState } from "vuex";
export default {
  data: () => ({
    loading: false,
    name: "",
    level: "",
    icon: "",
    iconUrl: "",
    tagName: "",
  }),
  computed: {
    ...mapState(["userId", "userSummoner", "summonerProfile"]),
    tagname() {
      return this.summonerProfile.tagName.split("#")[1];
    },
  },
  methods: {
    Update() {
      this.loading = true;
      axiosInstance
        .post("http://localhost:8000/api/update/", {
          userId: this.userId,
        })

        .then((res) => {
          console.log(res.data);
          this.name = res.data.name;
          this.level = res.data.summonerLevel;
          this.icon = res.data.profileIconId;
          this.iconUrl = require("../assets/profileicon/" + this.icon + ".png");
          this.tagName = this.userSummoner;
        })

        .catch((err) => {
          console.log(err);
        })
        .finally(() => (this.loading = false));
    },
  },
};
</script>

<style>
.tagname {
  color: grey;
}
</style>
