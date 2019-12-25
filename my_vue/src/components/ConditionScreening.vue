<template>
	<div>
		<div class="condition_screen">
			<span>粉丝数量：</span>
			<ul @click="change_bc($event),get_num($event)">
				<li class="active" value="0">小于10万</li>
				<li value="1">10万～50万</li>
				<li value="2">50万～100万</li>
				<li value="3">大于100万</li>
			</ul>
			<br />
			<span>用户标签：</span>
			<ul id="user_tags">
				<li @click="set_condition($event,ind)" v-for="(cls,ind) in classification" :key="ind">{{cls}}</li>
			</ul>
			<br />
			<div class="small_condition" v-if="seen" >
				<ul @click='change_bc($event),get_category($event)'>
					<li v-for="(val,index) in small_cond[li_index[0]]" :key="index">{{val}}</li>
				</ul>

				<br>			
			</div>
			

			<span>时间筛选：</span>
			<ul @click="change_bc($event),get_date($event)">
				<li class="active" value="3">近3日</li>
				<li value="7">近7日</li>
				<li value="10">近10日</li>
				<li value="30">近30日</li>
			</ul>


			<button @click="screen()">筛 选</button>
		</div>

		<div class="content">
			<div class="result">
				<span> 根据您的条件，为您筛选出<span class="num">{{user_list.length}}</span>个相关用户</span>
				<input type="text" placeholder="请输入关键字">
				<button class="glyphicon glyphicon-search search"></button>
				<span ></span>
			</div>
			<ul class="select">
				<li><a @click="show_user() ">用户列表</a></li>
				<li>|</li>
				<li><a @click="show_weibo()">微博列表</a></li>
			</ul>
			<div class="user_li" v-if="user_seen">
				<table>
					<tr>
						<th>序号</th>
						<th>微博名称</th>
						<th>简介</th>
						<th>地址</th>
						<th>粉丝数量</th>
						<th>标签</th>
						<th>微博数量</th>
					</tr>
					<span ></span>
					<tr v-if="user_list.length==0">
						<td></td>
						<td></td>
						<td></td>
						<td>暂无数据，请先筛选！</td>
						<td></td>
						<td></td>
						<td></td>
					</tr>
					<tr v-for='(user,index) in show_list' :key="index">
						<td>{{index}}</td>
						<td>{{user.name}}</td>
						<td>{{user.profile}}</td>
						<td>{{user.address}}</td>
						<td>{{user.fans_num}}</td>
						<td>{{user.label}}</td>
						<td>{{user.micro_blog_num}}</td>
					</tr>
				</table>

				<div class="pagination">
					<el-pagination
					background
					:hide-on-single-page='true'
					:page-size="pagesize"
					@current-change="handleCurrentChange"
					:current-page="currentPage"
					layout="total,prev, pager, next, jumper"
					:total="user_list.length">
				</el-pagination>
			</div>
		</div>

			<div class="weibo_li" v-if="weibo_seen">
				<table>
					<tr>
						<th>序号</th>
						<th>微博名称</th>
						<th>微博详情</th>
						<th>时间</th>
					</tr>
					<tr v-for='(con,index) in show_con' :key="index">
						<td>{{index}}</td>
						<td>{{con.user_name}}</td>
						<td>{{con.content.slice(0,20)}}</td>
						<td>{{con.time}}</td>
						<td><a href="#" @click="view_details(con.fields.content)">详情</a></td>
					</tr>
				</table>

				<div class="pagination">
					<el-pagination
					background
					:hide-on-single-page='true'
					:page-size="pagesize"
					@current-change="handleCurrentChange2"
					:current-page="currentPage"
					layout="total,prev, pager, next, jumper"
					:total="con_list.length">
				</el-pagination>
				</div>
			</div>

		</div>
	</div>
</template>

<script ></script>
<script>
	import VueEvent from "../model/VueEvent.js" // 引入广播实例
	import storage from "../model/storage.js" 

	export default {
	data(){
		return{
			currentPage:1,  //初始页
			pagesize:10,  //每页的数据
			show_list:[],
			user_list:[],
			con_list:[],
			show_con:[],
			classification:["名人","专家","兴趣","机构"],
			small_cond:[
				["明星","商界","媒体精英","作家","政府官员"],
				["医疗","育儿","IT互联网","电台","财经","教育","法律","美妆","艺术","设计","房产家装","汽车","交通","职业招聘","婚庆","宗教"],
				["时尚","美女","电影","电视剧","音乐","动漫","游戏","星座","搞笑","情感两性","运动健身","体育","萌宠","美食","旅游","摄影","历史军事","科学","数码"],
				["政务","媒体"]
			],
			li_index:[],
			seen:false,

			condition:{
				sel_num: "0",
				sel_time:"3",
				category:"明星"
			},
			user_seen:true,
			weibo_seen:false,
			if_screened:false,  // 判断是否进行了筛选
		}
	},
	mounted(){
		var user_list = storage.get('user_list');
		if(user_list){
			this.user_list = user_list;
			this.show_list=this.user_list.slice(0,this.pagesize);					
		};

		var con_list = storage.get('con_list');
		if(con_list){
			this.con_list = con_list;
			this.show_con=this.con_list.slice(0,this.pagesize);
		};
	},
	methods: {
		set_condition(e,n){
			this.li_index=[];
			var li_list = document.getElementById('user_tags').childNodes;
			for(var i=0;i<li_list.length;i++){
				li_list[i].style.color = "#000";
				li_list[i].style.backgroundColor = "#fff";
			}
			e.target.style.color = "#fff";
			e.target.style.backgroundColor = "rgb(84,192,110)";
			this.li_index.push(n);
			this.seen = true;
		},
		change_bc(e){
			var li_list = e.currentTarget.getElementsByTagName('li');
			for(var i=0;i<li_list.length;i++){
				li_list[i].style.color = "#000";
				li_list[i].style.backgroundColor = "#fff";
			}
			e.target.style.color = "#fff";
			e.target.style.backgroundColor = "rgb(84,192,110)";
		},
		get_num(e){
			this.condition.sel_num=e.target.getAttribute("value")
		},
		get_category(e){
			this.condition.category=e.target.getAttribute("value")
		},	
		get_date(e){
			this.condition.sel_time=e.target.getAttribute("value")
		},
		show_user(){
			this.weibo_seen=false;
			this.user_seen=true;
		},
		show_weibo(){
			this.user_seen=false;
			this.weibo_seen=true
		},
		screen(){
			alert("您选择的条件为："+this.condition.sel_num+","+this.condition.category+","+this.condition.sel_time+"\n正在为您筛选，请稍等......");
			
			this.$axios.get("api/data",
				{params: {
					num: this.condition.sel_num,
					category: this.condition.category,
					time:this.condition.sel_time}
				})
				.then(response => {
					// this.user_list = JSON.parse(response.data.message);
					this.user_list = (response.data.user);
					this.show_list=this.user_list.slice(0,this.pagesize);

					this.con_list = (response.data.con);	
					this.show_con=this.con_list.slice(0,this.pagesize);
					this.if_screened=true; // 请求成功后将if_scrrened设置为True

					//将数据持久化保存
					storage.set('user_list', this.user_list);
					storage.set('con_list', this.con_list);
					storage.set('if_screened', this.if_screened);  
				}).catch(err => {                 //请求失败后的处理函数
					console.log(err)
				});
		},
		handleCurrentChange(val) {
			// 跳转页数
			//获取当前页
			let index = this.pagesize * (val -1);
			//获取总数
			let allData = this.pagesize * val;
			
			let tablist=[];
			for(let i = index;i<allData;i++) {
				if (this.user_list[i]) {
					tablist.push(this.user_list[i])
				}
				this.show_list = tablist
			}
		},

		handleCurrentChange2(val) {
			// 跳转页数
			//获取当前页
			let index = this.pagesize * (val -1);
			//获取总数
			let allData = this.pagesize * val;
			
			let tablist=[];
			for(let i = index;i<allData;i++) {
				if (this.con_list[i]) {
					tablist.push(this.con_list[i])
				}
				this.show_con = tablist
			}
		},
		view_details(val){
			alert(val)
		}
	},
	// 在组件销毁前发送广播
	beforeDestroy(){
		if(this.if_screened==true){
			VueEvent.$emit('if_screened',true);
		}
	}
}
</script>

<style>
	.condition_screen{
		width: 100%;
		height: 28%;
		padding-top: 20px;
		background-color: #fff;
	}
	.condition_screen ul{
		list-style: none;
		font-size: 0;
		padding: 0;
		display: inline-block;
		border: 1px solid rgb(238,239,241);
	}
	.condition_screen span{
		font-size: 12px;
		margin-left: 30px;
	}
	.condition_screen li{
		width: 105px;
		height: 30px;
		display: inline-block;
		border-left: 1px solid rgb(238,239,241);
		line-height: 30px;
		font-size: 12px;
		text-align: center;
		cursor: pointer;
	}
	.condition_screen ul li:nth-child(1){
		border-left: 0px solid rgb(238,239,241);
	}
	.condition_screen li:hover{
		color: #fff !important;
		background-color: rgb(84,192,110) !important;;
	}	
	.condition_screen .active{
		color: #fff;
		font-weight: bold;
		background-color: rgb(84,192,110);
	}
	.condition_screen button{
		width: 100px;
		height: 30px;
		background-color: rgb(84,192,110);
		color: #fff;
		float: right;
		margin-right: 50px;
		border-radius: 10%
	}
	#user_tags li:hover{
		background-color: rgb(84,192,110);
	}
	.small_condition{
		width:485px;
		margin:-11px 90px 10px;

	}
	.small_condition ul{
		margin:0px;
	}

	.small_condition li{
		width:60px;
		border:0;
	}
	.content{
		width: 97%;
		height: 69%;
		margin: 10px auto 0;
		background-color: #fff;
		overflow: hidden;
	}
	.result{
		height: 20%;
		line-height: 80px;
		border-bottom: 1px solid #ddd;
	}
	.result span{
		font-size: 12px;
		color: rgb(80,90,101);
		letter-spacing: 1px;
		margin-left: 25px;
	}
	.result .num{
		color: rgb(84,192,110);
		letter-spacing: 0px;
		margin:0 5px 0;
	}
	.result input{
		width: 150px;
		height: 25px;
		margin: 32px 40px;
		float: right;
	}
	.search{
		height: 25px;
		margin: 31px -190px;
		float: right;
	}
	.select{
		padding: 0;
		margin-left: 20px;
		list-style: none;
		font-size: 0px;
	}
	.select li{
		width: 65px;
		font-size: 14px;
		line-height: 50px;
		display: inline-block;
		text-align: center;
		
	}
	.select a{
		cursor: pointer;
	}
	.select a:hover{
		color: red;
		text-decoration: none;
	}
	.user_li{
		margin-top: 20px;
	}
	.user_li table{
		color: rgb(80,90,101);
		font-size: 14px;
		text-align: center;
		line-height: 30px;
		margin-top: -28px;
	}
	.user_li table th{
		text-align: center;
		line-height: 38px;
		width: 4%;
	}
	.weibo_li{
		margin-top:-20px
	}
	.weibo_li table{
		color: rgb(80,90,101);
		font-size: 14px;
		text-align: center;
		line-height: 30px;
	}
	.weibo_li table th{
		text-align: center;
		line-height: 38px;
		width: 20%;
	}
	.weibo_li table td{
		text-align: center;
	}
	.pagination{
		margin:20px 300px 10px;
	}
</style>