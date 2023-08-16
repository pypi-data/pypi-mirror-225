<template>
	<router-view v-slot="{ Component }">
		<keep-alive>
			<component :is="Component"></component>
		</keep-alive>
	</router-view>
</template>

<script setup>
import { watch } from "vue"
import { useRoute } from "vue-router"

let route = useRoute();

watch(route, async () => {
	criscostack.router.current_route = await criscostack.router.parse();
	criscostack.breadcrumbs.update();
	criscostack.recorder.route = route;
});
</script>
