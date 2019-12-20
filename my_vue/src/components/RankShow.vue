<template>
	<div class="show">
			<span><a @click="show_e()">图像展示</a></span>
			<span>|</span>
			<span><a @click="show_u()">相关用户</a></span>
			<br>	

			<span v-if="user_list.length==0" style="margin-left:410px">暂无数据，请先筛选数据！</span>
<!-- 		<img src="../assets/zhu.png" v-if="show_echar"> -->
			<!-- 数据可视化 -->
			<div id="myChart" style="width:850px;height:450px" v-if="user_list.length!=0 &&show_echar"></div>
			<!-- 相关用户展示 -->
			<user-list v-show="show_use&&user_list.length!=0"></user-list>		
		</div>	 
</template>

<script>
export default {
	data(){
		return{
			url:"",
			show_echar:true,
			show_use:false,
			user_list:[],
			con_list:[],
			url:"",
		}
	},
	components: {
		'v-rank':rank,
		'user-list':userlist
  },
	mounted(){
		this.getData()
	},
	methods: {
		drawPicture(){
			// 可视化函数
			var myChart = this.$echarts.init(document.getElementById('myChart'));
			var option = {
				title: {
					text: ''
				},
				tooltip: {},
				legend: {
					data:['影响力']
				},
				xAxis: {
					data: this.user_list
				},
				yAxis: {},
				series: [{
					name: '影响力',
					type: 'bar',
					data: this.con_list
				}]
			};
			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option);
		},
		}
}
</script>