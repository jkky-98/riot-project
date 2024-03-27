<template>
  <v-main class="main-container">
    <v-container>
      <v-row>
        <v-col>
          <v-card variant="elevated" color="#26293C">
            <v-row>
              <v-col cols="4">
                <ProfileCard />
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-container class="pt-0">
      <v-card variant="elevated" color="#26293C">
        <v-tabs v-model="tab" bg-color="#1A1627">
          <v-tab value="one">종합</v-tab>
          <v-tab value="two">챔피언</v-tab>
          <v-tab value="three">상세분석</v-tab>
        </v-tabs>

        <v-card-text>
          <v-window v-model="tab">
            <v-window-item value="one">
              <v-card
                variant="elevated"
                color="#26293C"
                class="pa-0"
                rounded="sm"
                ><v-row>
                  <v-col cols="4">
                    <v-card color="#1A1627" rounded="LG" class="pb-4 pl-3">
                      <v-card-subtitle class="text-white pa-2 pb-0 pl-3"
                        >솔로 랭크</v-card-subtitle
                      >
                      <v-container class="mx-4 pl-3">
                        <v-row>
                          <v-col cols="2" class="pa-1 pl-0 pr-3">
                            <v-img
                              class="custom-cropped"
                              cover
                              aspect-ratio="1"
                              :src="emblemSrc"
                            ></v-img>
                          </v-col>
                          <v-col cols="6" class="pa-0 px-3">
                            <v-card color="#1A1627" class="text-h5" flat>
                              <span
                                :style="{
                                  color: emblemFontColor,
                                  'font-weight': 'bold',
                                  textAlign: 'right',
                                }"
                              >
                                {{ this.summonerProfile.tier }}
                                {{ this.summonerProfile.rank }}
                              </span>
                            </v-card>
                            <v-card color="#1A1627" class="text-white" flat>
                              <span
                                :style="{
                                  textAlign: 'right',
                                  'font-weight': 'bold',
                                }"
                              >
                                {{ this.summonerProfile.leaguePoints }} LP
                              </span>
                            </v-card>
                          </v-col>
                          <v-col cols="4" class="pa-0">
                            <v-card
                              color="#1A1627"
                              class="text-white mt-1"
                              flat
                            >
                              <span :style="{ 'font-weight': 'bold' }">
                                {{ this.summonerProfile.wins }}W
                                {{ this.summonerProfile.losses }}L
                              </span>
                            </v-card>
                            <v-card
                              color="#1A1627"
                              class="text-white mt-1"
                              flat
                              :style="{ 'font-weight': 'bold' }"
                            >
                              승률 {{ this.summonerProfile.winrate }}%
                            </v-card>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card>
                    <ChampionUsedInfo />
                  </v-col>
                  <v-col cols="8" class="pl-0">
                    <v-card
                      variant="elevated"
                      color="#26293C"
                      class="pa-0"
                      rounded="sm"
                    >
                      <v-row>
                        <v-col cols="12" class="pb-0">
                          <v-card
                            color="#1A1627"
                            rounded="LG"
                            class="pa-3"
                            max-height="100%"
                          >
                            <div class="image-container">
                              <v-img
                                v-for="(champion, index) in championUsed.slice(
                                  0,
                                  9
                                )"
                                :key="index"
                                :src="`https://raw.communitydragon.org/14.5/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${champion[0]}.png`"
                                max-width="45"
                                max-height="45"
                                min-height="30"
                                min-width="30"
                                class="custom-cropped.champion round pa-1"
                              >
                                <div class="image-overlay">
                                  <span class="number">{{
                                    champion[1].total
                                  }}</span>
                                </div>
                              </v-img>
                            </div>
                          </v-card>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col>
                          <v-card
                            v-for="(match, index) in Object.values(
                              matchData
                            ).slice(0, 10)"
                            :key="index"
                            rounded="LG"
                            class="pa-3 mb-1 text-white"
                            max-height="100%"
                            :class="{
                              'loss-card ': !match.win,
                              'win-card': match.win,
                              'mvp-card': match.mvp,
                            }"
                          >
                            <v-row class="pa-2">
                              <div
                                class="custom-bar"
                                :class="{ loss: !match.win, win: match.win }"
                              ></div>
                              <v-col cols="3" class="pa-0">
                                <div class="pt-2 pl-3">
                                  <h3>Ranked Solo</h3>
                                  <h6>
                                    {{ formatUnixTime(match.gameEndTimestamp) }}
                                  </h6>
                                  <p class="mt-1"></p>
                                  <span
                                    :class="{
                                      'loss-font': !match.win,
                                      'win-font': match.win,
                                    }"
                                  >
                                    {{ match.win ? "승리" : "패배" }}
                                  </span>
                                  <span style="font-size: x-small">
                                    {{ formatUnixTime_m(match.gameLength) }}
                                  </span>
                                  <h5>Emerald 2</h5>
                                </div>
                              </v-col>
                              <v-col cols="5" class="pa-0">
                                <div style="display: flex; align-items: center">
                                  <v-img
                                    :src="`https://raw.communitydragon.org/14.5/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/${match.championId}.png`"
                                    max-width="55"
                                    max-height="55"
                                    min-height="30"
                                    min-width="30"
                                    class="custom-cropped.champion round pa-1"
                                    @click="
                                      filterChampionMatch(match.championId)
                                    "
                                    style="display: flex"
                                  ></v-img>
                                  <div
                                    style="
                                      display: flex;
                                      flex-direction: column;
                                    "
                                    class="pl-1"
                                  >
                                    <v-img
                                      :src="`https://ddragon.leagueoflegends.com/cdn/14.6.1/img/spell/${
                                        this.spell[match.summoner1Id].name
                                      }.png`"
                                      max-width="27.5"
                                      max-height="27.5"
                                      min-height="27.5"
                                      min-width="27.5"
                                      class="custom-cropped.champion round pl-3"
                                    >
                                    </v-img>
                                    <p></p>
                                    <v-img
                                      :src="`https://ddragon.leagueoflegends.com/cdn/14.6.1/img/spell/${
                                        this.spell[match.summoner2Id].name
                                      }.png`"
                                      max-width="27.5"
                                      max-height="27.5"
                                      min-height="27.5"
                                      min-width="27.5"
                                      class="custom-cropped.champion round pa-1"
                                    >
                                    </v-img>
                                  </div>
                                  <div class="px-4"></div>
                                  <div style="text-align: center">
                                    <h4>
                                      {{ match.kills }} /
                                      <span style="color: red">{{
                                        match.deaths
                                      }}</span>
                                      /
                                      {{ match.assists }}
                                    </h4>
                                    <h6 :class="{ 'high-kda': match.kda >= 4 }">
                                      {{ match.kda.toFixed(1) }} KDA
                                    </h6>
                                  </div>
                                </div>
                                <p class="pt-2"></p>
                                <div
                                  style="
                                    display: flex;
                                    flex-direction: row;
                                    align-items: center;
                                    height: 30px;
                                  "
                                  class="pa-0"
                                >
                                  <v-img
                                    v-for="(item, index) in itemViewer(match)"
                                    :key="index"
                                    :src="`https://ddragon.leagueoflegends.com/cdn/14.6.1/img/item/${item}.png`"
                                    max-width="24"
                                    max-height="24"
                                    min-height="22"
                                    min-width="22"
                                    class="pl-6"
                                  ></v-img>
                                </div>
                              </v-col>
                              <v-col cols="3"> </v-col>
                              <v-col cols="1">
                                <v-card-actions>
                                  <v-spacer></v-spacer>

                                  <v-btn
                                    :icon="
                                      show
                                        ? 'mdi-chevron-up'
                                        : 'mdi-chevron-down'
                                    "
                                    @click="show = !show"
                                  ></v-btn>
                                </v-card-actions>
                              </v-col>
                            </v-row>
                            <v-expand-transition>
                              <div v-show="show">
                                <p class="py-1"></p>
                                <v-divider class="py-1"></v-divider>

                                <v-card color="#1A1627" class="text-grey" flat>
                                  <v-dialog
                                    transition="dialog-bottom-transition"
                                    width="auto"
                                  >
                                    <template
                                      v-slot:activator="{
                                        props: activatorProps,
                                      }"
                                    >
                                      <v-btn
                                        v-bind="activatorProps"
                                        text="Stats Info"
                                        block
                                        class="text-white"
                                        color="#1A1627"
                                      ></v-btn>
                                    </template>

                                    <template v-slot:default="{ isActive }">
                                      <v-card color="#1A1627">
                                        <v-toolbar
                                          title="Stats Info"
                                        ></v-toolbar>

                                        <v-card-text class="text-h6 pa-12">
                                          <div
                                            style="
                                              display: flex;
                                              flex-direction: column;
                                              align-items: left;
                                            "
                                          >
                                            <h5>
                                              생성 현상금 : 매치동안 형성된
                                              자신의 총 현상금 골드
                                            </h5>
                                            <h5>DPM : 분당 데미지</h5>
                                            <h5>GPM : 분당 획득 골드</h5>
                                            <h5>DPG : 골드당 데미지</h5>
                                            <h5>
                                              DPT : 입힌 데미지 / 받은 데미지
                                            </h5>
                                            <h5>
                                              DDPT : 매치동안 죽은 시간 비율
                                            </h5>
                                            <h5>
                                              DGPT : 매치동안 스킬샷 피한 비율
                                            </h5>
                                            <h5>
                                              암살 : 팀원또는 혼자 적이 보이지
                                              않는 시야에서 급습하여 킬관여 횟수
                                            </h5>
                                            <h5>
                                              다이브 점수 : 자신의 포탑 또는
                                              상대 포탑 아래에서 기록한 킬
                                              횟수(자신의 포탑 아래 킬에서는
                                              가산점 - 1점당 1킬의 가치)
                                            </h5>
                                            <h5>
                                              10분 cs : 10분 이전까지의 처치한
                                              미니언 마지막 타수
                                            </h5>
                                            <h5>
                                              포탑 방패 파괴횟수 : 14분 이전까지
                                              생성되는 포탑 방패에 대한 파괴
                                              횟수
                                            </h5>
                                            <h5>VSPM : 분당 시야점수</h5>
                                            <h5>
                                              핑 횟수 : 해당 매치에서의 모든
                                              종류의 나의 핑의 횟수
                                            </h5>
                                            <h5>
                                              MY팀 핑 횟수 : 해당 매치에서의
                                              모든 종류의 나의 팀의 핑의 횟수
                                            </h5>
                                          </div>
                                        </v-card-text>

                                        <v-card-actions class="justify-end">
                                          <v-btn
                                            text="Close"
                                            @click="isActive.value = false"
                                          ></v-btn>
                                        </v-card-actions>
                                      </v-card>
                                    </template>
                                  </v-dialog>
                                  <v-data-table
                                    :headers="headers"
                                    :items="tableDataMaker(match)"
                                  >
                                  </v-data-table>
                                </v-card>
                              </div>
                            </v-expand-transition>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card>
            </v-window-item>

            <v-window-item value="two"> Two </v-window-item>

            <v-window-item value="three"
              ><DetailStats></DetailStats>
            </v-window-item>
          </v-window>
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
</template>

<script>
import ProfileCard from "./ProfileCard.vue";
import ChampionUsedInfo from "./ChampionUsedInfo.vue";
import DetailStats from "./DetailStats.vue";

import axiosInstance from "../setaxios.js";
import { mapState } from "vuex";
export default {
  data() {
    return {
      showTooltip: false,
      headers: [
        {
          align: "start",
          key: "name",
          sortable: false,
          title: "Your stats on match",
        },
        { key: "stats", title: "스텟" },
        { key: "oppo", title: "맞 라인 대비" },
        { key: "rank", title: "순위" },
      ],
      show: false,
      tab: null,
      emblemColor: {
        BRONZE: "brown", // BRONZE 티어에 대한 색상
        SILVER: "silver", // SILVER 티어에 대한 색상
        GOLD: "gold", // GOLD 티어에 대한 색상
        PLATINUM: "cyan", // PLATINUM 티어에 대한 색상
        EMERALD: "#12C3C9", // EMERALD 티어에 대한 색상
        DIAMOND: "#3F80C9", // DIAMOND 티어에 대한 색상
        MASTER: "purple", // MASTER 티어에 대한 색상
        GRANDMASTER: "red", // GRANDMASTER 티어에 대한 색상
        CHALLENGER: "orange", // CHALLENGER 티어에 대한 색상
      },
      emblem: {
        BRONZE:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-bronze.png",
        SILVER:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-silver.png",
        GOLD: "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-gold.png",
        PLATINUM:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-platinum.png",
        EMERALD:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-emerald.png",
        DIAMOND:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-diamond.png",
        MASTER:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-master.png",
        GRANDMASTER:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-grandmaster.png",
        CHALLENGER:
          "https://raw.communitydragon.org/14.5/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-challenger.png",
      },
      spell: {
        baseUrl: "https://ddragon.leagueoflegends.com/cdn/14.6.1/img/spell/",
        21: {
          name: "SummonerBarrier",
          name_ko: "방어막",
          description:
            "2초 동안 방어막으로 감싸 피해를 105~411(챔피언 레벨에 따라 변동)만큼 흡수합니다.",
        },
        1: {
          name: "SummonerBoost",
          name_ko: "정화",
          description:
            "챔피언에 걸린 모든 이동 불가와 (제압 및 공중으로 띄우는 효과 제외) 소환사 주문에 의한 해로운 효과를 제거하고 새로 적용되는 이동 불가 효과들의 지속시간을 3초간 65% 감소시킵니다.",
        },
        4: {
          name: "SummonerFlash",
          name_ko: "점멸",
          description: "커서 방향으로 챔피언이 짧은 거리를 순간이동합니다.",
        },
        14: {
          name: "SummonerDot",
          name_ko: "점화",
          description:
            "적 챔피언을 불태워 5초 동안 70~410의 고정 피해(챔피언 레벨에 따라 변동)를 입히고 모습을 드러내며 치료 효과를 감소시킵니다.",
        },
        3: {
          name: "SummonerExhaust",
          name_ko: "탈진",
          description:
            "적 챔피언을 지치게 만들어 3초 동안 이동 속도를 30% 느리게 하고 적 챔피언이 가하는 피해량을 35% 낮춥니다.",
        },
        6: {
          name: "SummonerHaste",
          name_ko: "유체화",
          description:
            "챔피언이 15초 동안 유닛과 충돌하지 않게 되며 챔피언 레벨에 따라 이동 속도가 24~48% 증가합니다.",
        },
        7: {
          name: "SummonerHeal",
          name_ko: "회복",
          description:
            "자신과 대상 아군 챔피언의 체력을 80~318만큼 회복시키고 1초 동안 이동 속도가 30% 증가합니다. 최근 소환사 주문 회복의 영향을 받은 유닛의 경우 치유량이 절반만 적용됩니다.",
        },
        13: {
          name: "SummonerMana",
          name_ko: "총명",
          description:
            "최대 마나량의 50%를 회복합니다. 주변 아군도 최대 마나량의 25%가 회복됩니다.",
        },
        11: {
          name: "SummonerSmite",
          name_ko: "강타",
          description: "대상 몬스터에게 600~1,200의 고정 피해를 입힙니다.",
        },
        12: {
          name: "SummonerTeleport",
          name_ko: "순간이동",
          description:
            "4초 동안 정신을 집중한 다음, 대상으로 지정한 아군 구조물로 순간이동합니다. 10분에 강력 순간이동으로 업그레이드됩니다. 강력 순간이동은 아군 구조물, 미니언, 혹은 와드를 대상으로 지정할 수 있습니다.",
        },
      },
    };
  },
  name: "MainPage",
  computed: {
    ...mapState([
      "userId",
      "userSummoner",
      "summonerProfile",
      "championUsed",
      "matchData",
    ]),
    emblemSrc() {
      // this.summonerProfile.tier 값에 따라 해당하는 emblem 경로를 반환합니다.
      return this.emblem[this.summonerProfile.tier];
    },
    emblemFontColor() {
      return this.emblemColor[this.summonerProfile.tier];
    },
  },
  mounted() {
    axiosInstance
      .get("http://localhost:8000/api/update/", {
        params: {
          userId: this.userId,
        },
      })
      .then((res) => {
        console.log(res.data);
        this.name = res.data.name;
        this.level = res.data.summonerLevel;
        this.icon = res.data.profileIconId;
        this.iconUrl = require("../assets/profileicon/" + this.icon + ".png");
        this.tagName = this.userSummoner;
        this.tier = res.data.tier;
        this.rank = res.data.rank;
        this.leaguePoints = res.data.leaguePoints;
        this.wins = res.data.wins;
        this.losses = res.data.losses;
        this.winrate = (this.wins / (this.wins + this.losses)) * 100;
        this.winrate = this.winrate.toFixed(1);

        this.$store.commit("setSummonerProfile", {
          name: this.name,
          level: this.level,
          icon: this.icon,
          iconUrl: this.iconUrl,
          tagName: this.tagName,
          tier: this.tier,
          rank: this.rank,
          leaguePoints: this.leaguePoints,
          wins: this.wins,
          losses: this.losses,
          winrate: this.winrate,
        });
        axiosInstance
          .get("http://localhost:8000/api/match_individual/", {
            params: {
              userId: this.userId,
            },
          })
          .then((res) => {
            const data = JSON.parse(res.data);
            this.$store.commit("setMatchData", data);
          })
          .catch((err) => {
            console.log(err);
          });
      })

      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    formatUnixTime(unixTime) {
      // 유닉스 시간을 초 단위로 변환
      let seconds = unixTime;

      // Date 객체 생성
      let date = new Date(parseInt(seconds));

      // 년도, 월, 일, 시간을 가져옴
      let year = date.getFullYear();
      let month = date.getMonth() + 1;
      let day = date.getDate();
      let hours = date.getHours();
      let minutes = date.getMinutes();

      // 두 자리로 만들기 위해 10 미만의 숫자에는 '0'을 추가
      if (month < 10) {
        month = "0" + month;
      }
      if (day < 10) {
        day = "0" + day;
      }
      if (hours < 10) {
        hours = "0" + hours;
      }
      if (minutes < 10) {
        minutes = "0" + minutes;
      }

      // 결과 반환
      return `${year}-${month}-${day} ${hours}시 ${minutes}분`;
    },
    formatUnixTime_m(seconds) {
      let minutes = Math.floor(seconds / 60);
      let remainingSeconds = Math.floor(seconds % 60);
      // 결과를 문자열로 반환
      return `${minutes}분 ${remainingSeconds}초`;
    },
    filterChampionMatch(championId) {
      console.log(championId);
    },
    itemViewer(match) {
      const items = [];
      for (let i = 0; i <= 5; i++) {
        const itemName = `item${i}`;
        items.push(match[itemName]);
      }
      return items;
    },
    tableDataMaker(match) {
      const data = [];
      const field = [
        {
          name: "생성 현상금",
          stats: match.bountyGold + "골드",
          oppo: match.bountyGoldOppo + "골드 우위",
          rank: match.bountyGoldRank + "위",
        },
        {
          name: "DPM",
          stats: match.damagePerMinute.toFixed(1) + "딜",
          oppo: (match.damagePerMinuteOppo * 100).toFixed(1) + "% 우위",
          rank: match.damagePerMinuteRank + "위",
        },
        {
          name: "GPM",
          stats: match.goldPerMinute.toFixed(1) + "골드",
          oppo: match.goldPerMinuteOppo * 100 + "% 우위",
          rank: match.goldPerMinuteRank + "위",
        },
        {
          name: "DPG",
          stats: match.dpg.toFixed(1) + "딜",
          oppo: (match.dpgOppo * 100).toFixed(1) + "% 우위",
          rank: match.dpgRank + "위",
        },
        {
          name: "DPT",
          stats: match.dpt.toFixed(1) + "딜",
          oppo: (match.dptOppo * 100).toFixed(1) + "% 우위",
          rank: match.dptRank + "위",
        },
        {
          name: "DDPT",
          stats: (match.ddpt * 100).toFixed(1) + "%",
          oppo: (match.ddptOppo * 100).toFixed(1) + "% 우위",
          rank: match.ddptRank + "위",
        },
        {
          name: "DGPT",
          stats: (match.dgpt * 100).toFixed(1) + "%",
          oppo: (match.dgptOppo * 100).toFixed(1) + "% 우위",
          rank: match.dgptRank + "위",
        },
        {
          name: "암살",
          stats: match.killAfterHiddenWithAlly + "번",
          oppo: match.killAfterHiddenWithAllyOppo + "번 우위",
          rank: match.killAfterHiddenWithAllyRank + "위",
        },
        {
          name: "다이브 점수",
          stats: match.killsNearTurret + "점",
          oppo: match.killsNearTurretOppo + "점 우위",
          rank: match.killsNearTurretRank + "위",
        },
        {
          name: "10분 CS",
          stats: match.laneMinionsFirst10Minutes + " cs",
          oppo: match.laneMinionsFirst10MinutesOppo + " cs 우위",
          rank: match.laneMinionsFirst10MinutesRank + "위",
        },
        {
          name: "수적 열세 클러치",
          stats: match.outnumberedKills + "킬",
          oppo: match.outnumberedKillsOppo + "킬 우위",
          rank: match.outnumberedKillsRank + "위",
        },
        {
          name: "10분 적 처치관여",
          stats: match.takedownsFirstXMinutes + "킬 관여",
          oppo: match.takedownsFirstXMinutesOppo + "킬 우위",
          rank: match.takedownsFirstXMinutesRank + "위",
        },
        {
          name: "포탑 방패 파괴횟수",
          stats: match.turretPlatesTaken + "번",
          oppo: match.turretPlatesTakenOppo + "번 우위",
          rank: match.turretPlatesTakenRank + "위",
        },
        {
          name: "VSPM",
          stats: match.visionScorePerMinute.toFixed(1),
          oppo: match.visionScorePerMinuteOppo.toFixed(1) + "% 우위",
          rank: match.visionScorePerMinuteRank + "위",
        },
        {
          name: "핑 횟수",
          stats: match.totalPings + "번",
          oppo: match.totalPingsOppo + "번 우위",
          rank: match.totalPingsRank + "위",
        },
        {
          name: "MY팀 핑 횟수",
          stats: match.myTeamPings + "번",
          oppo: (match.myTeamPingsOppo * 100).toFixed(1) + "% 우위",
          rank: "--",
        },
      ];
      // field 안의 객체들을 data에 푸쉬
      for (let i = 0; i < field.length; i++) {
        data.push(field[i]);
      }
      return data;
    },
  },
  components: {
    ProfileCard,
    ChampionUsedInfo,
    DetailStats,
  },
};
</script>

<style scoped>
.main-container {
  background-image: url("../assets/mainpage_bg.png");
}
.neon {
  animation: neon 1s ease infinite;
  -moz-animation: neon 1s ease infinite;
  -webkit-animation: neon 1s ease infinite;
}
.custom-cropped {
  object-fit: cover; /* 이미지를 부모 요소에 맞추고, 가로세로 비율을 유지한 채로 중앙에 배치합니다. */
  transform: scale(3.5);
  transform-origin: center; /* 변환의 기준점을 이미지의 중심으로 설정합니다. */
}
.custom-cropped.champion {
  transform: scale(1);
}
.image-overlay {
  position: absolute;
  bottom: 8%;
  left: 50%;
  transform: translate(-50%, 50%);
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 4px;
  border-radius: 4px;
}

.number {
  font-weight: bold;
}
.image-container {
  display: flex;
  flex-wrap: wrap;
}
.custom-bar {
  position: absolute; /* 절대적 위치 설정 */
  top: 0;
  left: 0;
  width: 1%; /* 카드의 3%로 설정 */
  height: 100%; /* 높이를 카드의 높이와 동일하게 설정 */
}
.loss {
  background-color: #f13352;
}
.win {
  background-color: #3376fe;
}
.loss-font {
  color: #f13352;
}
.win-font {
  color: #3376fe;
}
.kda-font {
  color: #3376fe;
  font-weight: bold;
}
.win-card {
  background-color: #1f2d55;
}
.loss-card {
  background-color: #432124;
}
.mvp-card {
  background-image: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.25) 40%,
      rgba(255, 255, 255, 0.3) 50%,
      rgba(255, 255, 255, 0.25) 60%,
      rgba(255, 255, 255, 0) 100%
    ),
    linear-gradient(to right, #5a4cbb, #5a84a2, #8f9dbe, #a199bd, #ab81bf);
  background-repeat: repeat-y;
  background-size: 200px 120px, auto;
  background-position: 0, 0 0;

  animation: glow 3.5s infinite;
}

@keyframes glow {
  to {
    background-position: 100% 0, 0 0;
  }
}
.mvp-card-detail {
  background-image: linear-gradient(
    to right,
    #5a4cbb,
    #5a84a2,
    #8f9dbe,
    #a199bd,
    #ab81bf
  );
}
.high-kda {
  color: #ba1457;
}
.v-table {
  background-color: #1a1627;
  color: white;
  font-size: 0.65rem;
}
</style>
