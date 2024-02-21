<template>
  <LoginPage />
</template>

<script>
import { defineComponent } from "vue";

// Components
import LoginPage from "../components/LoginPage.vue";

export default defineComponent({
  name: "HomeView",

  components: {
    LoginPage,
  },
});
</script>
