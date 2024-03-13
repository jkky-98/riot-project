<template>
  <div class="text-center pa-4">
    <v-btn @click="dialog = true"> 소환사명 등록 </v-btn>

    <v-dialog v-model="dialog" width="auto">
      <v-card
        max-width="400"
        text="소환사명 + 태그까지 입력하세요. (예시 : Hide on bush#KR1)"
        title="Update your Summoner Name"
      >
        <v-text-field placeholder="소환사명" required v-model="summonerName">
        </v-text-field>
        <template v-slot:actions>
          <v-btn class="ms-auto" text="연동" @click="submitSummoner"></v-btn>
        </template>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axiosInstance from "@/setaxios";
import { mapState } from "vuex";
export default {
  data() {
    return {
      dialog: false,
      summonerName: "",
    };
  },
  computed: {
    ...mapState(["userId", "userSummoner"]),
  },
  methods: {
    submitSummoner() {
      axiosInstance
        .post("http://localhost:8000/api/summoner/", {
          userId: this.userId,
          summonerName: this.summonerName,
        })
        .then((res) => {
          console.log(res.data);
          this.$store.commit("setUserSummoner", res.data.riot_id);
          this.dialog = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
