<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Main page</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">Welcome {{ greetedUser }}</div>
      </v-card-text>
      <v-card-actions>
        <v-btn to="/main/profile/view">View Profile</v-btn>
        <v-btn to="/main/profile/edit">Edit Profile</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Tests</div>
      </v-card-title>
      <v-card-actions>
        <v-btn to="/main/shulte">Start Schulte test</v-btn>
      </v-card-actions>
    </v-card>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Results</div>
      </v-card-title>
      <div v-for="(item, idx) in attempts" :key="item[0]">
        <v-card-text>
          <a class="headline main" @click="onClick(item[0])">
            Attempt #{{ idx }} date {{ item[1].split("T")[0] }} time
            {{ item[1].split("T")[1].slice(0, 8) }}
          </a>
        </v-card-text>
      </div>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { readUserProfile } from "@/store/main/getters";
import { api } from "@/api";
import { IAttempt } from "@/interfaces";

@Component
export default class Dashboard extends Vue {
  attempts: Array<Array<string>> = [];

  async onClick(amt) {
    await this.$router.push({
      name: "main-analytic",
      params: { attempt: amt.toString() },
    });
  }
  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
    return "";
  }
  onlyUnique(input) {
    const indices = input.map((el) => input.indexOf(el));
    const output = new Set<number>(indices);
    const result: Array<number> = [...output];
    return result;
  }
  async mounted() {
    const ids = Array<number>();
    const dates = Array<string>();
    const resp: Array<IAttempt> = (await api.getAttempts(this.$store.state.main.token))
      .data;
    for (let i = 0; i < resp.length; i++) {
      ids.push(resp[i].id);
      dates.push(resp[i].created);
    }
    const indices = this.onlyUnique(ids);
    for (const i of indices) {
      this.attempts.push([ids[i].toString(), dates[i]]);
    }
  }
}
</script>
<style scoped>
.main:hover {
  box-shadow: inset 0 0 0 0 #54b3d6;
  color: #54b3d6;
  margin: 0 -0.25rem;
  padding: 0 0.25rem;
  transition: color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
</style>
