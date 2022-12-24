<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline">Edit instruction</div>
      </v-card-title>
      <v-textarea v-model="instructions" required />
      <v-btn @click="onClick()">Save</v-btn>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { api } from "@/api";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class EditUser extends Vue {
  instructions = "";
  remains = "";

  public async mounted() {
    const r = (await api.getInstructions()).split("@@");
    this.instructions = r[0];
    this.remains = r.slice(1, r.length).join("@@");
  }

  public async onClick() {
    await api.setInstructions(
      this.$store.state.main.token,
      this.instructions + `@@${this.remains}`,
    );
    await this.$router.push("/main/dashboard");
  }
}
</script>
