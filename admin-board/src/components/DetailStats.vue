<template>
  <v-btn @click="PingsAnalysis"></v-btn>
  <v-btn @click="calculatePointBiserialCorrelation"></v-btn>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: () => ({}),
  computed: {
    ...mapState(["matchData"]),
  },
  methods: {
    PingsAnalysis() {
      const matchData = this.matchData;
      // totalPingsRank 값과 win 값 간의 관계를 저장할 객체 초기화
      const pingsWinRelationship = {
        winCountByTotalPingsRank: Array.from({ length: 10 }, () => 0), // totalPingsRank에 해당하는 승리 횟수를 저장할 배열
        totalCountByTotalPingsRank: Array.from({ length: 10 }, () => 0), // totalPingsRank에 해당하는 전체 플레이 횟수를 저장할 배열
        winRateByTotalPingsRank: Array.from({ length: 10 }, () => 0), // totalPingsRank에 해당하는 승률을 저장할 배열
      };

      // 주어진 데이터를 기반으로 관계 분석
      for (const key in matchData) {
        if (Object.prototype.hasOwnProperty.call(matchData, key)) {
          const match = matchData[key];
          const { totalPingsRank, win } = match;
          if (totalPingsRank >= 1 && totalPingsRank <= 10) {
            pingsWinRelationship.totalCountByTotalPingsRank[
              totalPingsRank - 1
            ]++;
            if (win) {
              pingsWinRelationship.winCountByTotalPingsRank[
                totalPingsRank - 1
              ]++;
            }
          }
        }
      }

      // 승률 계산
      for (let i = 0; i < 10; i++) {
        if (pingsWinRelationship.totalCountByTotalPingsRank[i] !== 0) {
          // 분모가 0이 아닌 경우에만 승률 계산
          pingsWinRelationship.winRateByTotalPingsRank[i] =
            pingsWinRelationship.winCountByTotalPingsRank[i] /
            pingsWinRelationship.totalCountByTotalPingsRank[i];
        }
      }

      // 결과 출력
      console.log(
        "totalPingsRank에 따른 승리 횟수:",
        pingsWinRelationship.winCountByTotalPingsRank
      );
      console.log(
        "totalPingsRank에 따른 전체 플레이 횟수:",
        pingsWinRelationship.totalCountByTotalPingsRank
      );
      console.log(
        "totalPingsRank에 따른 승률:",
        pingsWinRelationship.winRateByTotalPingsRank
      );
    },
    calculatePointBiserialCorrelation() {
      const xValues = [];
      const yValues = [];
      let sumX = 0;
      let sumY = 0;
      let countY = 0;

      // 데이터 추출
      for (const key in this.matchData) {
        if (Object.prototype.hasOwnProperty.call(this.matchData, key)) {
          const { myTeamPingsOppo, win } = this.matchData[key];
          // 만약 myTeamPingsOppo가 -3부터 3 사이의 값이 아니라면 무시
          if (myTeamPingsOppo >= -1 && myTeamPingsOppo <= 1) {
            xValues.push(myTeamPingsOppo);
            yValues.push(win ? 1 : 0); // 이진 변수를 1과 0으로 변환하여 저장
            sumX += myTeamPingsOppo;
            sumY += win ? 1 : 0;
            countY += 1;
          }
        }
      }

      // x의 평균 계산
      const xMean = sumX / xValues.length;

      // y의 평균 계산
      const yMean = sumY / countY;

      // 분자 계산
      let numerator = 0;
      for (let i = 0; i < xValues.length; i++) {
        numerator += (xValues[i] - xMean) * (yValues[i] - yMean);
      }

      // x의 표준편차 계산
      let xVariance = 0;
      for (let i = 0; i < xValues.length; i++) {
        xVariance += Math.pow(xValues[i] - xMean, 2);
      }
      xVariance /= xValues.length;

      // 상관계수 계산
      const correlation =
        numerator / Math.sqrt(xVariance * (1 - yMean) * yMean);

      // 결과 설정
      this.correlation = correlation;
      console.log(correlation);
    },
  },
};
</script>

<style></style>
