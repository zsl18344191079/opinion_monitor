<template>
	<!-- 地理位置分析 -->
	<div>
		<v-rank :title="title" :introduce="introduce"></v-rank>

		<div class="echarts" style="margin-left:150px">
			<iframe width="100%" height="500"  src="./中国地图2.html"  frameborder="no" border="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>
		</div>	
	</div> 
</template>

<script>
import rank from "./RankList.vue" 

export default {
	data(){
		return{
			title:'地理位置分析',
			introduce:'首先将得到的用户被关注度取代当前存在虚假的用户粉丝数,通过较为合理的用户被关注度计算得到微博用户的用户活跃度与微博影响力,最后将用户活跃度与微博影响力作为用户影响力的影响因子合成微博用户的用户影响力',

		}
	},
	components: {
		'v-rank':rank,
  }
}
</script>