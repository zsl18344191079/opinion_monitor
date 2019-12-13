<template>
	<div>
		{{user_list}}
		<span v-if="user_list.length==0">暂无数据，请先筛选数据！</span>
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
		alert("this.user_list : "+this.user_list)
		this.drawLine()
	},
	methods: {
		getData(){
			this.$axios.get("api/rank")
				.then(response => {
					// this.$set(this.user_list,'a',response.data.message);
					this.user_list = (response.data.message);
					this.con_list = (response.data.con);
				}).catch(err => {                 //请求失败后的处理函数
					console.log(err)
				});
		},
		drawLine(){
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

<style>
	#myChart{
		width:850px;
		height:450px;
	}
</style>