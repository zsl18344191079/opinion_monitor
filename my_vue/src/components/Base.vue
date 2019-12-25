<template>
	<div>
		<div class="top">
			<div class="top_le">
				<a href="#"><span class="glyphicon glyphicon-fire"></span>微博舆情监控平台</a>
			</div>
			
			<div class="top_ri">
				<ul>
					<li><a href="#">登录</a></li>
					<li>|</li>
					<li><a href="#">注册</a></li>
					<li>|</li>
					<li><a href="#">帮助</a></li>
					<li>|</li>
					<li><a href="#">联系</a></li>
				</ul>
			</div>
		</div>

		<div class="control_list">
			<ul @click='change_color($event)'>
				<li><router-link to="/home"><span class="glyphicon glyphicon-home  s_active"></span> 首  页</router-link></li>
				<li><router-link to="/screen"><span class="glyphicon glyphicon-screenshot"></span> 条件筛选</router-link></li>
				<li><router-link to="/daywc"><span class="glyphicon glyphicon-cloud"></span> 每日词云</router-link></li>
				<li><router-link to="/weekwc"><span class="glyphicon glyphicon-cloud"></span> 每周词云</router-link></li>
				<li><router-link to="/wctrend"><span class="glyphicon glyphicon-globe"></span> 人员分布</router-link></li>
				<li><router-link to="/influence"><span class="glyphicon glyphicon-stats"></span> 影响力排行榜</router-link></li>
				<li><router-link to="/activity"><span class="glyphicon glyphicon-stats"></span> 活跃度排行榜</router-link></li>
				<li><router-link to="/pointpraise"><span class="glyphicon glyphicon-stats"></span> 点赞数排行榜</router-link></li>
				<li><router-link to="/comment"><span class="glyphicon glyphicon-stats"></span> 评论量排行榜</router-link></li>
				<li><router-link to="/forward"><span class="glyphicon glyphicon-stats"></span> 转发数排行榜</router-link></li>
			</ul>
		</div>
		<div class="show_content">
			<router-view></router-view>
		</div>
	</div>
</template>

<script>

export default {
	data(){
		return{
		}
	},
	methods: {
		change_color(e) {
			var span_li = e.currentTarget.getElementsByTagName('span')
			for (var i=0;i<span_li.length;i++){ 
				span_li[i].style.color="rgb(178,184,197)";
			}

			e.target.getElementsByTagName('span')[0].style.color="rgb(84,192,110)";
		}
	}
}
</script>

<style>
	.top{
			width: 100%;
			height:62px;
			background-color:#000;
			color: #fff;
			position: relative;
		}
		.top_le{
			float: left;
			margin:18px;
			font-weight: bold;
		}
		.top_le span{
			font-size: 19px;
		}
		.top_le a{
			text-decoration: none;
			font-size: 16px;

		}
		.top_ri{
			float: right;
			margin: 18px;
		}
		.top_ri ul{
			list-style: none;
		}
		.top_ri li{
			font-size: 14px;
			margin-left:15px;	
			display: inline-block;	
		}
		.top_ri li a{
			text-decoration: none;
			color: #fff;
		}

		.control_list{
			width: 15%;
			background-color:rgb(51,65,79);
			position:absolute;
			top:62px;
			left:0;
			bottom:0;
		}
		.control_list ul{
			list-style: none;
			margin:0;
			padding:0;
		}
		.control_list li{
			height: 40px;
			color: rgb(178,184,197);
			text-indent: 12px;
			border-bottom: 0.5px solid rgb(47,60,73);
		}
		.control_list li:hover{
			background-color: #3c4e5e;
			cursor: pointer;
			margin-left: 2px;
		}
		.s_active{
			color: rgb(84,192,110)
		}
		.control_list li a{
			font-family: 'PingFang SC,helvetica neue,arial,microsoft yahei,sans-serif';
			color: rgb(178,184,197);
			display:inline-block;
			width:186px;
			letter-spacing:2px;
			font-size: 15px;
			line-height: 40px;
			text-decoration: none;
		}
		.show_content{
			width: 85%;
			background-color: rgb(238,239,241);
			position:absolute;
			top:62px;
			left:203px;
			bottom:0;
			overflow:auto;
		}


</style>