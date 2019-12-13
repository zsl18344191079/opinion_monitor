<template>
	<!-- 排行榜 -->
		<div class="ranking_list">
			<span>{{title}}</span>
			<span class="glyphicon glyphicon-question-sign help" @mouseenter="onMouseOver" @mouseleave="onMouseOut"></span>		
			<div class="introduce">
				<i class="triangle" v-if="seen"></i>
				<div class="con" v-if="seen">
					<span>{{title}}</span>
					<p>{{introduce}}</p>
				</div>
			</div>				
			<hr>			
		</div> 
</template>

<script>

export default {
	data(){
		return{
			seen:false
		}
	},
	props:{
		title:String,
		introduce:String
	},
	methods:{
		onMouseOver(){
			this.seen = true
		},
		onMouseOut(){
			this.seen = false
		}
	},
	components: {
  }
}
</script>

<style >
/*排行榜*/
.ranking_list{
	width: 96%;
	height: 96%;
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
.echarts{
	margin:-10px 23px 10px;
	background-color: #fff;
	padding-left:125px;
	padding-bottom:20px;
}
</style>