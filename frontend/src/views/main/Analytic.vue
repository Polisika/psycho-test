<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Aggregation</div>
      </v-card-title>
      <v-card-text>
        <div class="headline font-weight-light ma-5">
          {{ err }} {{ agg_err.toFixed(2) }}
        </div>
        <div class="headline font-weight-light ma-5">
          {{ we }} {{ (result[0].time / agg_time).toFixed(2) }}
        </div>
        <div class="headline font-weight-light ma-5">
          {{ we_int }}
        </div>
        <div class="headline font-weight-light ma-5">
          {{ ps }}
          {{ (result[result.length - 1].time / agg_time).toFixed(2) }}
        </div>
        <div class="headline font-weight-light ma-5">
          {{ ps_int }}
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
            Errors num: {{ item.errors ? item.errors.split(" ").length : 0 }}
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
  err = "Average error num: ";
  we = "Work warming-up: ";
  we_int =
    "The result of 1,0 and lower shows good warming-up, while 1,0 and more means\n" +
    " that one needs more time to prepare for the main work (warm-up).";
  ps = "Psychological stability: ";
  ps_int =
    "The result of 1,0 and less shown good psychological stability. Positive\n" +
    " effects include attention stability, improved visual perception, improved\n" +
    " peripheral vision, and development of speed reading.";

  async mounted() {
    const attempt_id = Number(this.$router.currentRoute.params.attempt);
    const inter = (await api.getInstructions()).split("@@");

    this.err = inter[1];
    this.we = inter[2];
    this.we_int = inter[3];
    this.ps = inter[4];
    this.ps_int = inter[5];

    this.result = await api.getAnalytic(this.$store.state.main.token, attempt_id);
    for (let i = 0; i < this.result.length; i++) {
      const err_l = this.result[i].errors ? this.result[i].errors.split(" ").length : 0;
      this.agg_err += err_l;
      this.agg_time += this.result[i].time;
    }
    this.agg_err /= this.result.length;
    this.agg_time /= this.result.length;
  }
}
</script>
