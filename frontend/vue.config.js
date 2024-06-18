const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  devServer: {
    port: 5000,
    proxy: 'http://127.0.0.1/'
  },
  devServer: {
    port: 5000,
    proxy: 'http://192.168.1.12/'
  }
}