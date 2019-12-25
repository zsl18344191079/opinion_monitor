<template>
	<!-- 词云 -->
		<div class="ranking_list">
			<span>每日词云</span>
			<span class="glyphicon glyphicon-question-sign help" @mouseenter="onMouseOver" @mouseleave="onMouseOut"></span>		
			<div class="introduce" v-if="seen">
				<i class="triangle" v-if="seen"></i>
				<div class="con" >
					<span>每日词云</span>
					<p>首先将得到的用户被关注度取代当前存在虚假的用户粉丝数,通过较为合理的用户被关注度计算得到微博用户的用户活跃度与微博影响力,最后将用户活跃度与微博影响力作为用户影响力的影响因子合成微博用户的用户影响力</p>
				</div>
			</div>
			<i class="el-icon-refresh refresh" title="点击刷新页面" v-if="ref1" @click="refresh"></i>
			<i class="el-icon-loading refresh" title="刷新ing...." v-if="ref2"></i>
			<hr>

			<div class="show">
		
				<span v-if="data.length==0" style="margin-left:410px">暂未完成</span>
				<div class="tagBall" v-if="data.length==0">
					<span class="tag"></span>
				</div>		
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
			data :[],
		}
	},
	props:{
		screen:String
	},
	created(){
		VueEvent.$on('if_screened',(value)=>{
			this.if_screened = value
		})
		
	},
	mounted(){
		// 只有进行筛选后才会请求数据并渲染图像
		// this.drawPicture()
		var if_screened = storage.get('if_screened');
		if(if_screened){
			// this.getData()
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
			await this.$axios.get(this.url,{params: {screen: this.screen,}})
				.then(response => {
					this.data = (response.data.con_rank);			
				}).catch(err => {                 //请求失败后的处理函数
					console.log(err)
				});
		},
		// 词云绘制
		drawPicture(){
			var tagEle = "querySelectorAll" in document ? document.querySelectorAll(".tag") : getClass("tag"),
			paper = "querySelectorAll" in document ? document.querySelector(".tagBall") : getClass("tagBall")[0];
			function getClass(className) {
				var ele = document.getElementsByTagName("*");
				var classEle = [];
				for (var i = 0; i < ele.length; i++) {
					var cn = ele[i].className;
					if (cn === className) {
						classEle.push(ele[i]);
					}
				}
				return classEle;
			}
			var RADIUS = 220,
			tags = [],
			fallLength = 500,
			angleX = Math.PI / 500,
			angleY = Math.PI / 500,
			CX = paper.offsetWidth / 2,
			CY = paper.offsetHeight / 2,
			EX = paper.offsetLeft + document.body.scrollLeft + document.documentElement.scrollLeft,
			EY = paper.offsetTop + document.body.scrollTop + document.documentElement.scrollTop;
			function innit() {
				for (var i = 0; i < tagEle.length; i++) {
					var a, b;
					var k = -1 + (2 * (i + 1) - 1) / tagEle.length;
					a = Math.acos(k);
					b = a * Math.sqrt(tagEle.length * Math.PI);
					var x = RADIUS * Math.sin(a) * Math.cos(b);
					var y = RADIUS * Math.sin(a) * Math.sin(b);
					var z = RADIUS * Math.cos(a);
					var t = new tag(tagEle[i], x, y, z);
					tagEle[i].style.color = "rgb(" + parseInt(Math.random() * 255) + "," + parseInt(Math.random() * 255) + "," + parseInt(Math.random() * 255) + ")";
					tags.push(t);
					t.move();
				}
			}
				function animate() {
					rotateX(tags,angleX);
					rotateY(tags,angleY);
					tags.forEach(function() {
						this.move();
					});
					requestAnimationFrame(animate);
				}
				function rotateX() {
					var cos = Math.cos(angleX);
					var sin = Math.sin(angleX);
					tags.forEach(function() {
						var y1 = this.y * cos - this.z * sin;
						var z1 = this.z * cos + this.y * sin;
						this.y = y1;
						this.z = z1;
					})
				}
				function rotateY(){
					var cos = Math.cos(angleY);
					var sin = Math.sin(angleY);
					tags.forEach(function() {
						var x1 = this.x * cos - this.z * sin;
						var z1 = this.z * cos + this.x * sin;
						this.x = x1;
						this.z = z1;
					})
				}
			Array.prototype.forEach = function(callback) {
				for (var i = 0; i < this.length; i++) {
					callback.call(this[i]);
				}
			}

		if ("addEventListener" in window) {
			paper.addEventListener("mousemove", function(event) {
				var x = event.clientX - EX - CX;
				var y = event.clientY - EY - CY;
				angleY = x * 0.0001;
				angleX = y * 0.0001;
			});
		}
		else {
			paper.attachEvent("onmousemove", function(event) {
				var x = event.clientX - EX - CX;
				var y = event.clientY - EY - CY;
				angleY = x * 0.0001;
				angleX = y * 0.0001;
			});
		}

		var tag = function(ele, x, y, z) {
			this.ele = ele;
			this.x = x;
			this.y = y;
			this.z = z;
		}
		tag.prototype = {
			move: function() {
				var scale = fallLength / (fallLength - this.z);
				var alpha = (this.z + RADIUS) / (2 * RADIUS);
				var left = this.x + CX - this.ele.offsetWidth / 2 + "px";
				var top = this.y + CY - this.ele.offsetHeight / 2 + "px";
				var transform = 'translate(' + left + ', ' + top + ') scale(' + scale + ')';
				this.ele.style.opacity = alpha + 0.5;
				this.ele.style.zIndex = parseInt(scale * 100);
				this.ele.style.transform = transform;
				this.ele.style.webkitTransform = transform;
			}
		}

		innit();
		animate();
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


	.tagBall {
		position: relative;
		margin:160px 120px 0 0;
	}
	.tag {
		display: block;
		position: absolute;
		left: 0px;
		top: 0px;
		color: #000;
		text-decoration: none;
		font-size: 15px;
		font-family: "微软雅黑";
		font-weight: bold;
		will-change: transform;
	}
	.tag:hover {
		border: 1px solid #666;
	}
</style>