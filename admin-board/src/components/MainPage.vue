<template>
  <v-btn>HI</v-btn>
  <v-card>
    <v-text-field placeholder="userId" required></v-text-field>
  </v-card>
</template>

<script>
export default {
  name: "MainPage",
  method: {
    SubmitTest() {
      console.log("HI");
    },
  },
};
</script>
