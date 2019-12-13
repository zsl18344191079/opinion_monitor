import Vue from 'vue'
import App from './App.vue'
// 引用Bootstrap
import "bootstrap"
import "./bootstrap/dist/css/bootstrap.min.css"
Vue.config.productionTip = false;



//引入路由
import VueRouter from 'vue-router';
Vue.use(VueRouter);

// 创建组件
import home from './components/HomePage.vue';
import screen from './components/ConditionScreening';
import daywc from './components/DayWordCloud';
import weekwc from './components/WeekWordCloud';
import wctrend from './components/WordCloudTrend';
import influence from './components/InfluenceRank';
import activity from './components/ActivityRank';
import pointpraise from './components/PointPraiseRank';
import comment from './components/CommentRank';
import forward from './components/ForwardRank';

// 配置路由
const routes = [
	{path:'*',component:home},
	{path:'/home',component:home},
	{path:'/screen',component:screen},
	{path:'/daywc',component:daywc},
	{path:'/weekwc',component:weekwc},
	{path:'/wctrend',component:wctrend},
	{path:'/influence',component:influence},
	{path:'/activity',component:activity},
	{path:'/pointpraise',component:pointpraise},
	{path:'/comment',component:comment},
	{path:'/forward',component:forward},
]

//实例化VueRouter
const router = new VueRouter({
	routes //缩写，相当于routes:routes
})

// 引入echarts
import echarts from 'echarts'

import './plugins/element.js'
Vue.prototype.$echarts = echarts

// 引入element ui
import ElementUI from 'element-ui' 
// import 'element-ui/lib/theme-chalk/index.css' 

 Vue.use(ElementUI)


// 引入axios
import axios from 'axios'
Vue.prototype.$axios = axios

new Vue({
  render: h => h(App),
  router, //挂载路由
}).$mount('#app')
