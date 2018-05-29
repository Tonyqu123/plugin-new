// see http://vuejs-templates.github.io/webpack for documentation.
var path = require('path')
var fs = require('fs')
// var dcvPath = path.resolve(process.cwd(), '../lib/config.json');
// var dcvConfig = JSON.parse(fs.readFileSync(dcvPath).toString());

var baseApi = 'http://106.75.116.205';

// var baseApi = 'http://localhost:5000';
// var basePluginApi = 'http://localhost:5000';

module.exports = {
  build: {
    env: require('./prod.env'),
    index: path.resolve(__dirname, '../dist/index.html'),
    assetsRoot: path.resolve(__dirname, '../dist'),
    assetsSubDirectory: 'static',
    assetsPublicPath: './',
    productionSourceMap: true,
    // Gzip off by default as many popular static hosts such as
    // Surge or Netlify already gzip all static assets for you.
    // Before setting to `true`, make sure to:
    // npm install --save-dev compression-webpack-plugin
    productionGzip: false,
    productionGzipExtensions: ['js', 'css'],
    // Run the build command with an extra argument to
    // View the bundle analyzer report after build finishes:
    // `npm run build --report`
    // Set to `true` or `false` to always turn it on or off
    bundleAnalyzerReport: process.env.npm_config_report,
    name: '应用作业',
  },
  dev: {
    env: require('./dev.env'),
    port: 7000,
    autoOpenBrowser: true,
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    proxyTable: {
        '/api/apps': {
            target: baseApi,
            changeOrigin: true,
        },
        '/api/jobs': {
            // target: 'http://106.75.116.205',
            target: baseApi,
            changeOrigin: true,
            pathRewrite: {
                '^/api/jobs': '/plugin/30000/api/jobs'
            }
        },
        '/tasks': {
            target: baseApi,
            changeOrigin: true,
        },
    },
    // CSS Sourcemaps off by default because relative paths are "buggy"
    // with this option, according to the CSS-Loader README
    // (https://github.com/webpack/css-loader#sourcemaps)
    // In our experience, they generally work as expected,
    // just be aware of this issue when enabling this option.
    cssSourceMap: false,
    name: '应用作业',
  }
}
