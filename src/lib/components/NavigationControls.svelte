<!-- src/lib/components/NavigationControls.svelte -->
<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/stores';

	// Determine current page to highlight active nav
	$: currentPath = $page.url.pathname;
</script>

<div class="navigation-controls">
	<a
		href="{base}/cosmic"
		class="navigation-icon"
		class:active={currentPath.includes('/cosmic')}
		title="Cosmic Timeline (C)">🌌</a
	>
	<a
		href="{base}/humanity"
		class="navigation-icon"
		class:active={currentPath.includes('/humanity')}
		title="Humanity Timeline (H)">🌍</a
	>
	<a
		href="{base}/people"
		class="navigation-icon"
		class:active={currentPath.includes('/people')}
		title="People Timeline (P)">👤</a
	>
	<a
		href="{base}/books"
		class="navigation-icon"
		class:active={currentPath.includes('/books')}
		title="Books Timeline (B)">📚</a
	>
	<a
		href="{base}/artworks"
		class="navigation-icon"
		class:active={currentPath.includes('/artworks')}
		title="Artworks Timeline (A)">🎨</a
	>
	<a
		href="{base}/list"
		class="navigation-icon"
		class:active={currentPath.includes('/list')}
		title="List View (L)">📋</a
	>
	<a
		href="{base}/search"
		class="navigation-icon"
		class:active={currentPath.includes('/search')}
		title="Search (S)">🔍</a
	>
</div>

<style>
	.navigation-controls {
		position: fixed;
		top: 20px;
		left: 20px;
		z-index: 100;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.navigation-icon {
		background-color: rgba(0, 0, 0, 0.85);
		backdrop-filter: blur(10px);
		border-radius: 50%;
		width: 56px;
		height: 56px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		text-decoration: none;
		font-size: 26px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
		transition:
			transform 0.2s,
			background-color 0.2s,
			box-shadow 0.2s;
		border: 1px solid rgba(255, 255, 255, 0.1);
		cursor: pointer;
	}

	.navigation-icon:hover {
		transform: scale(1.1);
		background-color: rgba(0, 0, 0, 0.95);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
	}

	.navigation-icon.active {
		background-color: rgba(250, 103, 66, 0.3);
		border-color: rgba(250, 103, 66, 0.5);
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.navigation-controls {
			gap: 10px;
			top: 16px;
			left: 16px;
		}

		.navigation-icon {
			width: 48px;
			height: 48px;
			font-size: 22px;
		}
	}

	@media (max-width: 480px) {
		.navigation-controls {
			gap: 8px;
			top: 12px;
			left: 12px;
		}

		.navigation-icon {
			width: 44px;
			height: 44px;
			font-size: 20px;
		}
	}
</style>
