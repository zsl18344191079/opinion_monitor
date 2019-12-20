<template>
	<div class="show_user_list">
		<div class="user_show_li">
			<ul>
				<li v-for="(name,index) in userli.name" :key="name" @click="change_con(name)">
					<img :src="userli.personal_head[index]">
					<span >{{name}}</span>
				</li>
			</ul>
		</div>
		<div class="con_show">
			<ul>
				<li v-for="(con,index) in conli[user_name]" :key="index">
				<p>{{con.content}}</p>
				<span>时间：{{con.time}}</span>
				<span> 点赞数：{{con.like_num}}</span>
				<span> 评论量：{{con.comment_num}}</span>
				<span> 转发量：{{con.forward_num}}</span>
				<hr>
				</li>
			</ul>

		</div>
	</div>
</template>

<script >

export default {
	data(){
		return{
			user_name:"",
		}
	},
	props:{
		userli:Object,
		conli:Object	
	},
	components: {

  },
	methods:{
		change_con(name){
			this.user_name = name
		}
  }
}
</script>

<style scopen>
	ul{
		list-style: none;
	}
	.show_user_list{
		margin: 20px auto;
		width: 950px;
		height: 622px;
		border: 1px solid #000;
	}
	.user_show_li{
		width: 30%;
		height: 100%;
		float: left;
		margin: 0;
	}
	.user_show_li ul{
		margin: 0;
		padding:0;
		border-right: 1px solid #eee
	}
	.user_show_li li{
		padding: 10px;
		cursor: pointer;
	}
	.user_show_li li:hover{
		background-color: rgb(178,184,197);
	}		
	.user_show_li img{
		width: 42px;
		border-radius: 50%
	}
	.con_show{
		width: 70%;
		height: 100%;
		overflow-y: scroll;
		float: right;
	}
	.con_show ul{
		margin: 10px 20px;
		padding: 0;
		
	}
	.con_show li{
		margin-bottom:20px;
	}
	.con_show span{
		margin-right:20px
	}

</style>