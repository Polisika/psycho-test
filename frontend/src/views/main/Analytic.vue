<template>
  <v-container fluid>
    <div>Attempt describe</div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
//import { api } from "@/api";

@Component
export default class Table extends Vue {
  async mounted() {
    const attempt_id = Number(this.$router.currentRoute.params.attempt);
    console.log(attempt_id);
    //const result = await api.getAnalytic(this.$store.state.main.token, attempt_id);
  }
}
</script>
