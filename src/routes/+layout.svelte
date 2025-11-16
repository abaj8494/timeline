<script>
	import '../app.css';
	import { page } from '$app/stores';
	
	let { children } = $props();
</script>

<svelte:head>
	<title>Shrine - Interactive Historical Timeline</title>
	<meta name="description" content="Explore history through an interactive timeline of influential people and books" />
	
	<!-- Structured Data -->
	{@html `<script type="application/ld+json">
	{
		"@context": "https://schema.org",
		"@type": "WebSite",
		"name": "Shrine Timeline",
		"description": "An interactive timeline visualization of historical figures and influential books throughout history",
		"url": "https://yourdomain.com/shrine/",
		"potentialAction": {
			"@type": "SearchAction",
			"target": "https://yourdomain.com/shrine/search?q={search_term_string}",
			"query-input": "required name=search_term_string"
		}
	}
	<\/script>`}
</svelte:head>

{@render children()}
