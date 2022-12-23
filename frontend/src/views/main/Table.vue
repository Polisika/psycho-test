<template>
  <v-container fluid>
    <div style="text-align: center; padding-top: 1%">{{ time }} seconds</div>
    <div class="table">
      <div v-for="(row, idx) in numbers" :key="idx" class="row">
        <div v-for="digit in row" :key="digit" class="cell" @click="onClick(digit)">
          <span>{{ digit }}</span>
        </div>
      </div>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
//import { api } from "@/api";

@Component
export default class Table extends Vue {
  numbers: Array<Array<string>> = [];
  errors = 0;
  currentIdx = 0;
  source: Array<string> = [];
  choosedNumber: Array<string> = [];
  time = 0;
  func = 0;
  async mounted() {
    const r = {
      data: {
        digits: "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25",
      },
    }; //await api.getTable(this.$store.state.main.token);
    const list = r.data.digits.split(" ");
    this.source = list;
    const result = Array<Array<string>>();
    const chunkSize = 5;
    for (let i = 0; i < list.length; i += chunkSize)
      result.push(list.slice(i, i + chunkSize));
    this.numbers = result;
    this.func = setInterval(() => {
      this.time++;
    }, 1000);
  }

  public onClick(digit) {
    if (this.source[this.currentIdx] != digit) this.errors++;
    else this.currentIdx++;

    this.choosedNumber.push(digit);

    if (this.currentIdx == this.source.length) {
      alert(
        `Тест пройден. Вы прошли тест за ${this.time} секунд, ошиблись ${this.errors} раз.`,
      );
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
