<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3" style="text-align: center">
      <v-card-title primary-title>
        <div class="headline primary--text">Instructions</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">{{ instructions }}</div>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn to="/main/table">Start</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";

@Component
export default class Schulte extends Vue {
  instructions = "";
  async mounted() {
    this.instructions = (await api.getInstructions()).split("@@")[0];
  }
}
</script>
