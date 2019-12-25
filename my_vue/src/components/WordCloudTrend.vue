<template>
	<!-- 人员分布 -->
		<div class="ranking_list">
			<span>人员分布</span>
			<span class="glyphicon glyphicon-question-sign help" @mouseenter="onMouseOver" @mouseleave="onMouseOut"></span>		
			<div class="introduce" v-if="seen">
				<i class="triangle" v-if="seen"></i>
				<div class="con" >
					<span>人员分布</span>
					<p>首先将得到的用户被关注度取代当前存在虚假的用户粉丝数,通过较为合理的用户被关注度计算得到微博用户的用户活跃度与微博影响力,最后将用户活跃度与微博影响力作为用户影响力的影响因子合成微博用户的用户影响力</p>
				</div>
			</div>
			<i class="el-icon-refresh refresh" title="点击刷新页面" v-if="ref1" @click="refresh"></i>
			<i class="el-icon-loading refresh" title="刷新ing...." v-if="ref2"></i>
			<hr>

			<div class="show">
				<span v-if="datat_li.length==0" style="margin-left:410px">暂无数据，请先筛选数据！</span>
				<div id="myChart" style="width:850px;height:450px;margin-left:170px" v-show="datat_li.length!=0"></div>	
			</div>	 			
		</div> 
</template>

<script>
import VueEvent from "../model/VueEvent.js" // 引入广播实例
import storage from "../model/storage.js" 

export default {
	data(){
		return{
			seen:false,
			ref1:true,
			ref2:false,
			datat_li:[]
		}
	},
	created(){
		VueEvent.$on('if_screened',(value)=>{
			this.if_screened = value
		})
		
	},
	mounted(){
		// this.drawLine()
		// 只有进行筛选后才会请求数据并渲染图像
		var if_screened = storage.get('if_screened');
		if(if_screened){
			this.getData()
		}
	},
	methods:{
		onMouseOver(){
			this.seen = true
		},
		onMouseOut(){
			this.seen = false
		},
		refresh(){
			if(!this.if_screened){
				alert("暂无数据,请先筛选数据！")
			}else{
				this.ref1=false
				this.ref2=true
				setTimeout(() =>{
					this.ref1=true
					this.ref2=false
					},1000);
				this.getData()
			}			
		},
		async getData(){
			await this.$axios.get("api/wordcloudtrend")
				.then(response => {
					this.datat_li = (response.data.data);

				}).catch(err => {                 //请求失败后的处理函数
					console.log(err)
				});

			this.drawLine(this.datat_li)
		},
		drawLine(datat_li){
			// 基于准备好的dom，初始化echarts实例
			var myChartContainer = document.getElementById('myChart');
			var myChartChina = this.$echarts.init(myChartContainer); 

			// 绘制图表
			var data = datat_li
			var yData = [];
			var barData = [];

			for (var i = 0; i < 10; i++) {
				barData.push(data[i]);
				yData.push(i + data[i].name);
			}

			var option = {
				title: [{
					show: true,
					text: '排名情况',
					textStyle: {
					color: '#2D3E53',
					fontSize: 18
					},
				right: 180,
				top: 100
				}],
				tooltip: {
					show: true,
					// 控制鼠标移入时的显示
					formatter: function(params) {
						return params.name + '：' + params.data['value']
					},
				},
				visualMap: {
					type: 'continuous',
					orient: 'horizontal',
					itemWidth: 10,
					itemHeight: 80,
					text: ['高', '低'],
					showLabel: true,
					seriesIndex: [0],
					min: 0,
					max: 2,
					inRange: {
						// 地图颜色
						// color: ['#6FCF6A', '#FFFD64', '#FF5000']
						color:['#0b50b9','#c3e2f4']
					},
					textStyle: {
						color: '#7B93A7'
					},
					bottom: 30,
						left: 'left',
				},
				grid: {
					right: 10,
					top: 135,
					bottom: 100,
					width: '20%'
				},
				xAxis: {
					show: false
				},
				yAxis: {
					type: 'category',
					inverse: true,
					nameGap: 16,
					axisLine: {
						show: false,
						lineStyle: {
							color: '#ddd'
						}
					},
					axisTick: {
						show: false,
						lineStyle: {
							color: '#ddd'
						}
					},
					axisLabel: {
						interval: 0,
						margin: 85,
						textStyle: {
							color: '#455A74',
							align: 'left',
							fontSize: 14
						},
						rich: {
							a: {
								color: '#fff',
								backgroundColor: '#FAAA39',
								width: 20,
								height: 20,
								align: 'center',
								borderRadius: 2
							},
							b: {
								color: '#fff',
								backgroundColor: '#4197FD',
								width: 20,
								height: 20,
								align: 'center',
								borderRadius: 2
							}
						},
							formatter: function(params) {
								if (parseInt(params.slice(0, 1)) < 3) {
									return [
										'{a|' + (parseInt(params.slice(0, 1)) + 1) + '}' + '  ' + params.slice(1)].join('\n')
								} else {
									return [
										'{b|' + (parseInt(params.slice(0, 1)) + 1) + '}' + '  ' + params.slice(1)].join('\n')
								}
							}
						},
					data: yData
				},
				geo: {
					// roam: true,
					map: 'china',
					left: 'left',
					right: '300',
					// layoutSize: '80%',
					label: {
						emphasis: {
							show: false
						}
					},
					itemStyle: {
						emphasis: {
							areaColor: '#fff464'
						}
					}
				},
				series: [
				{
					name: 'mapSer',
					type: 'map',
					roam: false,
					geoIndex: 0,
					label: {
						show: false,
					},
					data: data
				}, 
				{
					name: 'barSer',
					type: 'bar',
					roam: false,
					visualMap: false,
					zlevel: 2,
					barMaxWidth: 8,
					barGap: 0,
					itemStyle: {
						normal: {
							color: function(params) {
								// build a color map as your need.
								var colorList = [{
									colorStops: [{
										offset: 0,
										color: '#FFD119' // 0% 处的颜色
									}, {
										offset: 1,
										color: '#FFAC4C' // 100% 处的颜色
									}]
									},
									{
										colorStops: [{
											offset: 0,
											color: '#00C0FA' // 0% 处的颜色
										}, {
											offset: 1,
											color: '#2F95FA' // 100% 处的颜色
										}]
									}
								];
								if (params.dataIndex < 3) {
									return colorList[0]
								} else {
									return colorList[1]
								}
							},
							barBorderRadius: 15
						}
					},
					data: barData
				}]
				};
			myChartChina.setOption(option);
			},
	},
}
</script>

<style scoped>
.ranking_list{
	width: 96%;
	margin: 10px auto;
	background-color: #fff;
	overflow: visible;
	position: relative;
}
.ranking_list span{
	font-size: 16px;
	font-weight: bold;
	line-height: 70px;
	margin-left: 20px;
}
.ranking_list .help{
	font-weight: normal;
	color: rgb(230,232,235);
	margin-left: 10px;
	cursor: pointer;
	line-height: 0px;
}
.ranking_list .help:hover{
	color: rgb(84,192,110);
}
.ranking_list hr{
	margin-top: -5px;
}
.ranking_list img{
	margin: 30px 145px;
}
.introduce{
	position: absolute;
	left: 32px;
	top: 58px;
	z-index:99;
}
.triangle{
	position: absolute;
	margin: -20px 32px;
}
.triangle:before,.triangle:after{
	position: absolute;
	content: '';
	border-top:10px transparent dashed;
	border-left:10px transparent dashed;
	border-right:10px transparent dashed;
}
.triangle:before{
	border-bottom: 10px #eee solid;
}
.triangle:after{
	top: 1px;
	border-bottom: 10px #fff solid;
}
.con{
	width: 270px;
	height: 148px;
	background-color: #fff;
	border: 1px solid #eee;
	box-shadow: 0px 2px 10px 2px #ada4a4e6;
}
.con span{
	font-size: 14px;
	font-weight: normal;
	line-height: 35px;
	margin-left: 20px;
	padding: 0;
}
.con p{
	color: #675e5ead;
	font-size: 12px;
	text-indent: 24px;
	margin-top: -8px;
	padding: 10px
}
.refresh{
	position: absolute;
    top: 26px;
    right: 50px;
    font-size: 25px;
    color: rgb(84,192,110);
    cursor: pointer;
}
.show{
	background-color: #fff;
	margin: -10px 23px 0;
}
.show span{
	line-height:20px;
	font-size:15px;
	font-weight:normal;
}
.show span a{
	text-decoration:none;
	cursor: pointer;
	font-size:14px
}
</style>