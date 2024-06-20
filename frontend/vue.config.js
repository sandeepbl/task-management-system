const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  devServer: {
    port: 5000,
    proxy: 'http://127.0.0.1/'
  }
}
