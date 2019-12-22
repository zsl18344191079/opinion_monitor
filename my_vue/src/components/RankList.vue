<template>
	<!-- 排行榜 -->
		<div class="ranking_list">
			<span>{{title}}</span>
			<span class="glyphicon glyphicon-question-sign help" @mouseenter="onMouseOver" @mouseleave="onMouseOut"></span>		
			<div class="introduce" v-if="seen">
				<i class="triangle" v-if="seen"></i>
				<div class="con" >
					<span>{{title}}</span>
					<p>{{introduce}}</p>
				</div>
			</div>
			<i class="el-icon-refresh refresh" title="点击刷新页面" v-if="ref1" @click="refresh"></i>
			<i class="el-icon-loading refresh" title="刷新ing...." v-if="ref2"></i>
			<hr>

			<div class="show">
				<span><a @click="show_e()">图像展示</a></span>
				<span>|</span>
				<span><a @click="show_u()">相关用户</a></span>
				<br>	

				<span v-if="user_list.length==0" style="margin-left:410px">暂无数据，请先筛选数据！</span>
				<div id="myChart" style="width:850px;height:450px;margin-left:50px" v-show="user_list.length!=0 &&show_echar"></div>
				<user-list v-show="show_use && user_list.length!=0"
					:condata="con_data"
				></user-list>		
			</div>	 			
		</div> 
</template>

<script>
import userlist from "./UserShow.vue" 
import VueEvent from "../model/VueEvent.js" // 引入广播实例
import storage from "../model/storage.js" 

export default {
	data(){
		return{
			seen:false,
			ref1:true,
			ref2:false,
			show_echar:true,
			show_use:false,
			user_list:[], //用户
			data_list:[], //用户相关数据（eg:影响力、活跃度）
			con_data:{}, //用户微博
		}
	},
	props:{
		title:String,
		introduce:String,
		url:String,
		drawPicture:Function,
		screen:String
	},
	components: {
		'user-list':userlist
  },
	created(){
		VueEvent.$on('if_screened',(value)=>{
			this.if_screened = value
		})
		
	},
	mounted(){
		// var user_list = storage.get('rank_user');
		// if(user_list){
		// 	this.user_list = user_list;			
		// }
		// var data_list = storage.get('rank_data');
		// if(data_list){
		// 	this.data_list = data_list
		// }
		// var con_list = storage.get('rank_con');
		// if(con_list){
		// 	this.con_list = con_list;
		// }

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
		show_e(){
			this.show_use=false;
			this.show_echar=true;
		},
		show_u(){
			this.show_echar=false;
			this.show_use=true;
		},
		async getData(){
			await this.$axios.get(this.url,{params: {screen: this.screen,}})
				.then(response => {
					var con_rank = (response.data.con_rank);
					// 处理内容过长的情况
					for(var i=0;i<con_rank.length;i++){
						if(con_rank[i].length>20){
							this.user_list.push(con_rank[i].replace(/\s+/g,"").slice(0, 10)+"....")
						}else{
							this.user_list.push(con_rank[i])
						}
					}
					
					// this.user_list = (response.data.con_rank);
					this.data_list = (response.data.data_rank);
					this.con_data = (response.data.con_data);
					
					// storage.set('rank_user', this.user_list);
					// storage.set('rank_data', this.data_list);
					// storage.set('rank_con', this.con_list);
				}).catch(err => {                 //请求失败后的处理函数
					console.log(err)
				});

			this.drawPicture(this.user_list, this.data_list)
		},
	},
}
</script>

<style scoped>
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