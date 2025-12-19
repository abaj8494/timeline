<!-- src/routes/cosmic/+page.svelte -->
<script lang="ts">
	import EventTimeline from '$lib/components/EventTimeline.svelte';
	import NavigationControls from '$lib/components/NavigationControls.svelte';
	import cosmic from '$lib/data/cosmic.json';

	export let data;
</script>

<svelte:head>
	<title>{data.title}</title>
	<meta name="description" content={data.description} />
	<meta property="og:title" content={data.title} />
	<meta property="og:description" content={data.description} />
	<meta property="og:url" content="https://yourdomain.com/timeline/cosmic" />
</svelte:head>

<div class="timeline-wrapper">
	<EventTimeline items={cosmic} scaleType="log" />
</div>

<NavigationControls />

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
		height: 100vh;
		width: 100vw;
		background-color: #1c1e21;
	}

	:global(html) {
		overflow: hidden;
	}

	.timeline-wrapper {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		width: 100vw;
		height: 100vh;
		overflow: hidden;
	}
</style>
