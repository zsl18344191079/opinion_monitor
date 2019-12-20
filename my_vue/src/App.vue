<template>
	<div id="app">
		<v-base></v-base>
	</div>
</template>

<script>
import base from './components/Base.vue'

export default {
	name: 'app',
	components: {
		'v-base':base

	},
	mounted(){
		// 刷新浏览器窗口的时候清空浏览器缓存在localStorage的数据
            window.onbeforeunload = function () {
                var storage = window.localStorage;
                storage.clear()
            }

	}


}
</script>

<style>

</style>
