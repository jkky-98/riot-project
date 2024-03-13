<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <v-card>
            <v-row>
              <v-col cols="4">
                <ProfileCard />
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row>
        <v-col>
          <v-text-field></v-text-field>
        </v-col>
        <v-col>
          <v-text-field></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import ProfileCard from "./ProfileCard.vue";

export default {
  name: "MainPage",
  method: {
    SubmitTest() {
      console.log("HI");
    },
  },
  components: {
    ProfileCard,
  },
};
</script>
