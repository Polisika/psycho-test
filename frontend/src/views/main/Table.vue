<template>
  <v-container fluid>
    <div style="text-align: center; padding-top: 1%">{{ time }} seconds</div>
    <div style="text-align: center; padding-top: 1%">Find {{ currentIdx }}</div>
    <div class="table">
      <div v-for="(row, idx) in numbers" :key="idx" class="row">
        <div v-for="digit in row" :key="digit" class="cell" @click="onClick(digit)">
          <span
            :style="{
              color: styles[source.findIndex((x) => x === digit)],
            }"
            >{{ digit }}</span
          >
        </div>
      </div>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { IAttemptResponse, IInfo } from "@/interfaces";
import { api } from "@/api";
import { AxiosResponse } from "axios";
//import { api } from "@/api";

@Component
export default class Table extends Vue {
  numbers: Array<Array<string>> = [];
  errors: Array<string> = [];
  styles: Array<string | null> = [];
  currentIdx = 1;
  source: Array<string> = [];
  choosedNumber: Array<string> = [];
  time = 0;
  func = -1;
  table_id = -1;
  info: Array<IInfo> = [];

  async init() {
    const r = await api.getTable(this.$store.state.main.token);
    this.currentIdx = 1;
    this.time = 0;
    this.choosedNumber = [];
    this.errors = [];
    this.table_id = r.data.id;
    const list = r.data.digits.split(" ");
    for (let i = 0; i < 25; i++) this.styles.push(null);
    this.source = list;
    const result = Array<Array<string>>();
    const chunkSize = 5;
    for (let i = 0; i < list.length; i += chunkSize)
      result.push(list.slice(i, i + chunkSize));
    this.numbers = result;
  }

  async mounted() {
    await this.init();
  }

  public async onClick(digit) {
    if (this.func == -1)
      this.func = setInterval(() => {
        this.time++;
      }, 1000);

    if (this.currentIdx != digit) {
      this.errors.push(`${digit}@${this.time}`);
      const _idx = this.source.findIndex((x) => x == digit);
      this.styles[_idx] = "red";
    } else {
      for (const [idx, el] of this.styles.entries()) {
        if (el == "red") this.styles[idx] = null;
      }
      this.currentIdx++;
    }
    this.$forceUpdate();
    this.choosedNumber.push(digit);

    if (this.currentIdx === this.source.length + 1) {
      this.currentIdx = 1;
      clearInterval(this.func);
      this.func = -1;
      this.info.push({
        errors: this.errors.join(" "),
        time: this.time,
        choosed_number: this.choosedNumber.join(" "),
        table_id: this.table_id,
      });
      if (this.info.length === 5) {
        const resp: AxiosResponse<IAttemptResponse> = await api.createTests(
          this.$store.state.main.token,
          this.info,
        );
        const at_id = resp.data.attempt_id;
        await this.$router.push({
          name: "main-analytic",
          params: { attempt: at_id.toString() },
        });
      } else await this.init();
    }
  }
}
</script>
<style scoped>
.table {
  display: flex;
  flex-direction: column;
  margin-left: 25%;
  margin-right: 25%;
  margin-top: 4%;
}

.row {
  display: flex;
  flex-direction: row;
}

.cell {
  display: flex;
  flex-direction: column;
  user-select: none;
  width: 20%;
  justify-content: center;
  align-items: center;

  float: left;
  padding: 0;

  border: 1px solid #ccc;
  cursor: default;

  font-size: calc(8vmin);
  font-weight: bold;

  transition: background 800ms;
}
</style>
