<template>
	<div>
		<span v-if="user_list.length==0" style="margin-left:410px">暂无数据，请先筛选数据！</span>
		<div id="myChart" v-if="user_list.length!=0"></div>
	</div>

</template>

<script>
export default {
	data () {
		return {
			user_list:[],
			con_list:[],
		}
	},
	mounted(){
		this.getData()
	},
	methods: {
		async getData(){
			await this.$axios.get("api/rank")
				.then(response => {
					this.user_list = (response.data.message);
					this.con_list = (response.data.con);
				}).catch(err => {                 //请求失败后的处理函数
					console.log(err)
				});

			this.drawLine()
		},
		drawLine(){
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

<style scoped>
	#myChart{
		width:850px;
		height:450px;
	}
</style>