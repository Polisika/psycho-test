<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Aggregation</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">
          Average error num: {{ agg_err }}
        </div>
        <div class="headline font-weight-light ma-5">
          Average time {{ agg_time }} seconds
        </div>
      </v-card-text>
    </v-card>
    <div v-for="(item, idx) in result" :key="item.id">
      <v-card class="ma-3 pa-3">
        <v-card-title primary-title>
          <div class="headline font-weight">Attempt №{{ idx + 1 }} describe</div>
        </v-card-title>
        <v-card-text>
          <div class="headline font-weight-light ma-5">
            Errors num: {{ item.errors.split(" ").length }}
          </div>
          <div class="headline font-weight-light ma-5">
            Time {{ item.time }} seconds
          </div>
          <div class="headline font-weight-light ma-5">
            Sequence: {{ item.choosed_number }}
          </div>
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { api } from "@/api";
import { ITestResponse } from "@/interfaces";

@Component
export default class Table extends Vue {
  result: Array<ITestResponse> = [];
  agg_err = 0;
  agg_time = 0;

  async mounted() {
    const attempt_id = Number(this.$router.currentRoute.params.attempt);
    this.result = await api.getAnalytic(this.$store.state.main.token, attempt_id);
    for (let i = 0; i < this.result.length; i++) {
      this.agg_err += this.result[i].errors.split(" ").length;
      this.agg_time += this.result[i].time;
    }
    this.agg_err /= this.result.length;
    this.agg_time /= this.result.length;
  }
}
</script>
