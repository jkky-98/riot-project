<template>
  <v-card color="#1A1627" rounded="LG"
    ><v-card-subtitle class="text-white pa-2 pb-0 pl-3"
      >Your Champion</v-card-subtitle
    >
    <v-card
      v-for="(champion, index) in championUsed.slice(0, 6)"
      :key="index"
      color="#1A1627"
      class="pa-2 box glow"
    >
      <v-row>
        <v-col cols="3">
          <v-img
            class="custom-cropped round ml-4 mt-2"
            :src="`https://raw.communitydragon.org/14.5/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${champion[0]}.png`"
          >
          </v-img>
        </v-col>
        <v-col cols="5" class="pt-4" :style="{ 'font-weight': 'bold' }">
          {{ champion[1].name }}
          <br />
          <span :style="getKDAStyle(champion[1].avg_kda, champion[1].total)">
            {{ champion[1].avg_kda }} KDA
          </span>
        </v-col>

        <v-col cols="4" class="pt-4">
          <span
            :style="getWinRateStyle(champion[1].win_rate, champion[1].total)"
          >
            {{ champion[1].win_rate }} %
          </span>
          <br class=/>
          <span :style="{ fontWeight: 'bold' }">
            {{ champion[1].total }} 게임
          </span>
        </v-col>
      </v-row>
    </v-card>
    <v-expansion-panels color="#1A1627">
      <v-expansion-panel title="More">
        <v-expansion-panel-text>
          <v-card
            v-for="(champion, index) in championUsed.slice(
              6,
              championUsed.length
            )"
            :key="index"
            color="#1A1627"
            class="pa-2"
          >
            <v-row>
              <v-col cols="3">
                <v-img
                  class="custom-cropped round ml-4 mt-2"
                  :src="`https://raw.communitydragon.org/14.5/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${champion[0]}.png`"
                >
                </v-img>
              </v-col>
              <v-col cols="5" class="pt-4">
                {{ champion[1].name }}
                <br />
                <span
                  :style="getKDAStyle(champion[1].avg_kda, champion[1].total)"
                >
                  {{ champion[1].avg_kda }} KDA
                </span>
              </v-col>

              <v-col cols="4" class="pt-4">
                <span
                  :style="
                    getWinRateStyle(champion[1].win_rate, champion[1].total)
                  "
                >
                  {{ champion[1].win_rate }} %
                </span>
                <br class=/>
                <span :style="{ fontWeight: 'bold' }">
                  {{ champion[1].total }} 게임
                </span>
              </v-col>
            </v-row>
          </v-card>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import axiosInstance from "../setaxios.js";

export default {
  data: () => ({}),
  computed: {
    ...mapState(["userId", "userSummoner", "summonerProfile", "championUsed"]),
    championIconUrl() {
      return `https://raw.communitydragon.org/14.5/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${this.championUsed}.png`;
    },
  },

  mounted() {
    axiosInstance
      .get("http://localhost:8000/api/championused/", {
        params: {
          userId: this.userId,
        },
      })
      .then((res) => {
        const data = JSON.parse(res.data);
        this.$store.commit("setChampionUsed", data);
        console.log(this.championUsed);
      })
      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    getKDAStyle(kda, total) {
      if (total <= 5) {
        return { color: "white" };
      } else if (kda < 1.5) {
        return { color: "grey" };
      } else if (kda >= 1.5 && kda < 3) {
        return { color: "white", fontWeight: "bold" };
      } else if (kda >= 3 && kda < 4) {
        return { color: "#FF8029", fontWeight: "bold" };
      } else if (kda >= 4 && kda < 6) {
        return { color: "#F70069", fontWeight: "bold" };
      } else {
        return { color: "red", fontWeight: "bold" };
      }
    },
    getWinRateStyle(winRate, total) {
      if (total <= 5) {
        return { color: "white" };
      } else if (winRate <= 50) {
        return { color: "white" };
      } else if (winRate > 50 && winRate <= 60) {
        return { color: "white" };
      } else if (winRate > 60 && winRate <= 70) {
        return { color: "red", fontWeight: "bold" };
      } else {
        return { color: "red", fontWeight: "bold" };
      }
    },
  },
};
</script>

<style>
.custom-cropped {
  clip-path: inset(6% 6% 6% 6%);
  border-radius: 30%;
  transform: scale(1.2);
}
.v-expansion-panel-text__wrapper {
  padding: 1px 1px 1px;
  flex: 1 1 auto;
  max-width: 100%;
}
.v-expansion-panel {
  background-color: "#1A1627";
  color: "#1A1627";
}
</style>
