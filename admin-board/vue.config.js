// vue.config.js
const webpack = require("webpack");

module.exports = {
  productionSourceMap: false, // 소스 맵 생성 비활성화
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      // 필요에 따라 해당 플러그인을 사용하여 플래그를 전역으로 주입합니다.
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false),
      }),
    ],
  },
  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    },
  },
};
