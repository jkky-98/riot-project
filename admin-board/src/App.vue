<template>
  <v-app>
    <NavigationBar />
    <router-view />
  </v-app>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";
export default {
  name: "App",
  components: {
    NavigationBar,
  },

  data: () => ({}),
};
</script>

<style></style>
