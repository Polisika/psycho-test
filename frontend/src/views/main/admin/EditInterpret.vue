<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline">Average error num text</div>
      </v-card-title>
      <v-text-field v-model="err" required />
      <v-card-title primary-title>
        <div class="headline">Warmup coefficient text</div>
      </v-card-title>
      <v-text-field v-model="we" required />
      <v-card-title primary-title>
        <div class="headline">Warmup coefficient interpretation text</div>
      </v-card-title>
      <v-textarea v-model="we_int" required />
      <v-card-title primary-title>
        <div class="headline">Psychological stability coefficient text</div>
      </v-card-title>
      <v-text-field v-model="ps" required />
      <v-card-title primary-title>
        <div class="headline">Psychological stability interpretation text</div>
      </v-card-title>
      <v-textarea v-model="ps_int" required />
      <v-btn @click="onClick()">Save</v-btn>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { api } from "@/api";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class EditUser extends Vue {
  remains = "";
  err = "";
  we = "";
  we_int = "";
  ps = "";
  ps_int = "";

  public async mounted() {
    const inter = (await api.getInstructions()).split("@@");
    this.remains = inter[0];
    this.err = inter[1];
    this.we = inter[2];
    this.we_int = inter[3];
    this.ps = inter[4];
    this.ps_int = inter[5];
  }

  public async onClick() {
    await api.setInstructions(
      this.$store.state.main.token,
      `${this.remains}@@${this.err}@@${this.we}@@${this.we_int}@@${this.ps}@@${this.ps_int}`,
    );
    await this.$router.push("/main/dashboard");
  }
}
</script>
