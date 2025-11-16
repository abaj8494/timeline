<script>
	import '../app.css';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { base } from '$app/paths';
	import { onMount } from 'svelte';
	
	let { children } = $props();
	
	// Keyboard shortcuts
	onMount(() => {
		function handleKeyPress(e) {
			// Ignore if user is typing in an input field
			if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
				return;
			}
			
			const currentPath = $page.url.pathname;
			
			switch (e.key.toLowerCase()) {
				case 's':
					goto(`${base}/search`);
					break;
				case 'b':
					// Only navigate to books if not already on books page
					if (!currentPath.includes('/books')) {
						goto(`${base}/books`);
					}
					break;
				case 'l':
					goto(`${base}/list`);
					break;
				case 'p':
					// Only navigate to people if not already on people page
					if (!currentPath.includes('/people')) {
						goto(`${base}/people`);
					}
					break;
			}
		}
		
		window.addEventListener('keydown', handleKeyPress);
		
		return () => {
			window.removeEventListener('keydown', handleKeyPress);
		};
	});
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
