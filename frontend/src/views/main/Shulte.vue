<template>
  <v-container fluid>
    <div>{{ instructions }}</div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";

@Component
export default class Dashboard extends Vue {
  data() {
    let field = "";
    api.getInstructions().then((resp) => {
      field = resp;
    });
    return {
      instructions: field,
    };
  }
}
</script>
