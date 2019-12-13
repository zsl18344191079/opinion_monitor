/*
*Vue-CLI项目的核心配置文件
*/
const webpack = require("webpack");

module.exports = {
 configureWebpack: {
   plugins: [
     new webpack.ProvidePlugin({
       $: "jquery",
       jQuery: "jquery",
       "window.jQuery": "jquery",
       Popper: ["popper.js", "default"]
     })
   ]
 },
    devServer: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000/api',
                changeOrigin: true,
                // ws: true,
                pathRewrite: {
                  '^/api': ''
                }
            }
        }
    }
};