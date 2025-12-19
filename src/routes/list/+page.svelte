<!-- src/routes/list/+page.svelte -->
<script lang="ts">
	import { base } from '$app/paths';
	import people from '$lib/data/people.json';
	import { resolveBasePath } from '$lib/utils/paths';
	import NavigationControls from '$lib/components/NavigationControls.svelte';
	let genderFilter: string = 'all'; // 'all', 'male', 'female'
	let selectedPerson = null;

	// Sort people by birth-date
	$: sortedPeople = [...people].sort((a, b) => (a.born || 0) - (b.born || 0));

	// Filter by gender
	$: filteredPeople = sortedPeople.filter((person) => {
		if (genderFilter === 'all') return true;
		if (genderFilter === 'male') return person.gender === 1;
		if (genderFilter === 'female') return person.gender === 0;
		return true;
	});

	// Format year with BC/AD
	function formatYear(year: number): string {
		if (year === 0) return '0';
		return year < 0 ? `${Math.abs(year)} BC` : `${year} AD`;
	}

	// Navigate to timeline
	function viewInTimeline() {
		window.location.href = `${base}/people`;
	}
</script>

<svelte:head>
	<title>List - People Timeline</title>
	<meta name="description" content="Browse all historical figures sorted by birth date" />
</svelte:head>

<NavigationControls />

<div class="list-page">
	<div class="header">
		<h1 class="title">People ({filteredPeople.length})</h1>

		<div class="filter-controls">
			<span class="filter-label">Filter by Gender:</span>
			<div class="filter-buttons">
				<button
					class="filter-btn"
					class:active={genderFilter === 'all'}
					on:click={() => (genderFilter = 'all')}
				>
					All
				</button>
				<button
					class="filter-btn"
					class:active={genderFilter === 'male'}
					on:click={() => (genderFilter = 'male')}
				>
					Male
				</button>
				<button
					class="filter-btn"
					class:active={genderFilter === 'female'}
					on:click={() => (genderFilter = 'female')}
				>
					Female
				</button>
			</div>
		</div>
	</div>

	<div class="people-list">
		{#each filteredPeople as person (person.id)}
			<div
				class="person-card"
				role="button"
				tabindex="0"
				on:click={() => (selectedPerson = person)}
				on:keydown={(e) => {
					if (e.key === 'Enter' || e.key === ' ') {
						e.preventDefault();
						selectedPerson = person;
					}
				}}
			>
				<img src={resolveBasePath(person.image)} alt={person.name} class="person-image" />
				<div class="person-info">
					<h3 class="person-name">{person.name}</h3>
					<p class="person-dates">
						{person.born ? formatYear(person.born) : '?'} -
						{person.died ? formatYear(person.died) : 'present'}
					</p>
					{#if person.died && person.born}
						<p class="person-lifespan">
							({Math.abs(person.died - person.born)} years)
						</p>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</div>

{#if selectedPerson}
	<div class="detail-panel" role="dialog" aria-modal="true" aria-labelledby="person-name">
		<button class="close-detail" on:click={() => (selectedPerson = null)}> ✕ </button>
		<img src={resolveBasePath(selectedPerson.image)} alt={selectedPerson.name} />
		<h3 id="person-name">{selectedPerson.name}</h3>
		<div class="dates">
			{#if selectedPerson.born || selectedPerson.died}
				{selectedPerson.born ? formatYear(selectedPerson.born) : '?'} -
				{selectedPerson.died ? formatYear(selectedPerson.died) : 'present'}
				{#if selectedPerson.died && selectedPerson.born}
					<br />({Math.abs(selectedPerson.died - selectedPerson.born)} years old)
				{/if}
			{/if}
		</div>
		<button class="view-timeline-btn" on:click={viewInTimeline}> View in Timeline </button>
	</div>
{/if}

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		background-color: #1c1e21;
		color: white;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
		overflow-y: auto;
	}

	:global(html) {
		overflow-y: auto;
	}

	.list-page {
		min-height: 100vh;
		padding: 40px 20px;
	}

	.header {
		max-width: 1200px;
		margin: 0 auto 40px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 20px;
		padding-bottom: 20px;
		border-bottom: 2px solid rgba(250, 103, 66, 0.5);
	}

	.title {
		font-size: 2.5rem;
		font-weight: 300;
		margin: 0;
		color: #fa6742;
	}

	.filter-controls {
		display: flex;
		align-items: center;
		gap: 15px;
	}

	.filter-label {
		color: #aaa;
		font-size: 0.9rem;
	}

	.filter-buttons {
		display: flex;
		gap: 10px;
	}

	.filter-btn {
		padding: 8px 16px;
		border-radius: 8px;
		border: 1px solid rgba(250, 103, 66, 0.5);
		background: rgba(0, 0, 0, 0.4);
		color: #fff;
		font-size: 0.9rem;
		cursor: pointer;
		transition: all 0.2s;
	}

	.filter-btn:hover {
		border-color: rgba(250, 103, 66, 0.8);
		background: rgba(250, 103, 66, 0.2);
	}

	.filter-btn.active {
		background: #fa6742;
		border-color: #fa6742;
	}

	.people-list {
		max-width: 1200px;
		margin: 0 auto;
		display: grid;
		gap: 20px;
	}

	.person-card {
		background: rgba(0, 0, 0, 0.4);
		border-radius: 12px;
		padding: 20px;
		cursor: pointer;
		transition: all 0.3s;
		border: 1px solid transparent;
		display: flex;
		gap: 20px;
		align-items: center;
	}

	.person-card:hover {
		background: rgba(0, 0, 0, 0.6);
		transform: translateX(8px);
		border-color: #fa6742;
	}

	.person-image {
		width: 80px;
		height: 80px;
		border-radius: 50%;
		object-fit: cover;
		border: 2px solid #fa6742;
		flex-shrink: 0;
	}

	.person-info {
		flex: 1;
	}

	.person-name {
		font-size: 1.4rem;
		font-weight: 600;
		margin: 0 0 8px 0;
		color: #fff;
	}

	.person-dates {
		color: #999;
		font-size: 1rem;
		margin: 0;
	}

	.person-lifespan {
		color: #fa6742;
		font-size: 0.9rem;
		margin: 4px 0 0 0;
	}

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

	.detail-panel {
		position: fixed;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		background: rgba(26, 26, 46, 0.98);
		border-radius: 16px;
		border: 2px solid rgba(250, 103, 66, 0.6);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
		z-index: 2000;
		min-width: 300px;
		max-width: 400px;
		text-align: center;
		padding: 30px;
	}

	.detail-panel img {
		width: 150px;
		height: 150px;
		border-radius: 50%;
		object-fit: cover;
		margin: 0 auto 20px;
		border: 3px solid #fa6742;
	}

	.detail-panel h3 {
		color: #fff;
		margin: 0 0 10px 0;
		font-size: 1.8rem;
	}

	.detail-panel .dates {
		color: #aaa;
		font-size: 1.1rem;
		line-height: 1.6;
		margin: 0 0 20px 0;
	}

	.close-detail {
		position: absolute;
		top: 15px;
		right: 15px;
		background: rgba(239, 68, 68, 0.3);
		border: 1px solid rgba(239, 68, 68, 0.5);
		border-radius: 50%;
		color: white;
		font-size: 1.5rem;
		cursor: pointer;
		padding: 8px;
		line-height: 1;
		width: 35px;
		height: 35px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s;
	}

	.close-detail:hover {
		background: rgba(239, 68, 68, 0.6);
		transform: scale(1.1);
	}

	.view-timeline-btn {
		width: 100%;
		background-color: #fa6742;
		color: white;
		border: none;
		border-radius: 8px;
		padding: 12px;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.3s;
		margin-top: 10px;
	}

	.view-timeline-btn:hover {
		background-color: #e55a35;
	}

	@media (max-width: 768px) {
		.header {
			flex-direction: column;
			align-items: flex-start;
		}

		.person-card {
			flex-direction: column;
			text-align: center;
		}

		.person-image {
			width: 100px;
			height: 100px;
		}

		.detail-panel {
			max-width: calc(100% - 40px);
		}
	}
</style>
