/* eslint-disable */
<template>
	<!-- 点赞量排行榜 -->
	<div>
		<keep-alive exclude="needExcludeComponentName">
			<v-rank :title="title" 
				:introduce="introduce"
				:url="url"
				:drawPicture="drawPicture"
				:screen="screen"
			></v-rank>	
		</keep-alive>

		
	</div> 
</template>

<script>
import rank from "./RankList.vue" 

export default {
	data(){
		return{
			title:'点赞量排行榜',
			introduce:'首先将得到的用户被关注度取代当前存在虚假的用户粉丝数,通过较为合理的用户被关注度计算得到微博用户的用户活跃度与微博影响力,最后将用户活跃度与微博影响力作为用户影响力的影响因子合成微博用户的用户影响力',
			url:"api/conrank",
			screen:"point"
		}
	},
	components: {
		'v-rank':rank,
  },
	methods: {
		drawPicture(x_val, y_val){
			// 可视化函数
			var myChart = this.$echarts.init(document.getElementById('myChart'));
			var option = {
				title: {
					text: '',
					subtext: '数据来自网络'
				},
				tooltip: {
					trigger: 'axis',
					axisPointer: {
					type: 'shadow'
					}
				},
				legend: {
					data: ['点赞量']
				},
				grid: {
					left: '3%',
					right: '4%',
					bottom: '3%',
					containLabel: true
				},
				xAxis: {
					type: 'value',
					boundaryGap: [0, 0.01]
				},
				yAxis: {
					type: 'category',
					data: x_val
				},
				series: [
					{
						name: '点赞量',
						type: 'bar',
						data: y_val
					},
				]
			};
			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option);
		},

	}
}
</script>

<style scped>
</style>