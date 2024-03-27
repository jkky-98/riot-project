<template>
  <v-card
    :class="{
      'loss-card': !match.win,
      'win-card': match.win,
      'mvp-card': match.mvp,
    }"
    class="text-grey"
    flat
  >
    {{ match.bountyGold }}
    {{ match.damagePerMinute }}
    {{ match.ddpt.toFixed(5) * 100 }}
    {{ match.dgpt.toFixed(5) * 100 }}
    {{ match.dpg.toFixed(2) }}
    {{ match.dpt.toFixed(2) }}
    {{ match.goldPerMinute.toFixed(2) }}
    {{ match.killParticipation.toFixed(3) * 100 }}
    {{ match.killNearTurret }}
  </v-card>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: () => ({}),
  computed: {
    ...mapState(["matchData"]),
  },
  methods: {},
};
</script>

<style>
.loss {
  background-color: #f13352;
}
.win {
  background-color: #3376fe;
}
.mvp-card {
  background-image: linear-gradient(
    to right,
    #5a4cbb,
    #5a84a2,
    #8f9dbe,
    #a199bd,
    #ab81bf
  );
}
</style>
