<script lang="ts">
	import { resolveBasePath } from '$lib/utils/paths';
	import { onMount } from 'svelte';

	export let items: {
		id: string;
		name?: string; // for people
		title?: string; // for books and artworks
		born?: number; // for people
		died?: number; // for people
		published?: number; // for books
		created?: number; // for artworks
		image: string;
		gender?: number; // for people
		author?: string; // for books
		artist?: string; // for artworks
	}[];

	// Constants for visualization
	const PADDING = 60;
	const TIMELINE_Y = 800; // Increased from 400 to shift the timeline lower
	const BAR_HEIGHT = 8; // Thinner bars
	const BAR_GAP = 40; // Increased gap between bars (was 25)
	const BAR_OFFSET = 90; // Distance between bars and main timeline (was 70)
	const NAME_OFFSET = 10; // Distance between bar and name (reduced from 20)
	const DATE_OFFSET = 36; // Distance between bar and date (was not explicitly defined)
	const YEAR_PIXEL_RATIO = 1.2; // pixels per year - significantly increased for more horizontal space
	const MAX_BARS_PER_SIDE = 25; // Increased from 20 to allow more rows
	const DOT_RADIUS = 6; // New constant for book dots

	// Helper to determine if an item is a book, artwork, or person
	function isBook(item) {
		return item.title !== undefined && item.published !== undefined;
	}

	function isArtwork(item) {
		return item.title !== undefined && item.created !== undefined;
	}

	function isDot(item) {
		return isBook(item) || isArtwork(item);
	}

	// Calculate the earliest and latest years in the dataset
	$: earliestYear =
		Math.floor(Math.min(...items.map((p) => p.born || p.published || p.created || 0)) / 100) * 100 -
		100;
	$: latestYear =
		Math.ceil(
			Math.max(
				...items.map((p) => p.died || p.created || p.published || new Date().getFullYear() || 0)
			) / 100
		) * 100;

	// Calculate total width based on year span
	$: width = (latestYear - earliestYear) * YEAR_PIXEL_RATIO + PADDING * 2;

	// Calculate total height with additional padding
	$: height = TIMELINE_Y + PADDING * 3 + MAX_BARS_PER_SIDE * 2 * (BAR_HEIGHT + BAR_GAP);

	// Sort by birth/publication/creation year
	$: sorted = [...items].sort(
		(a, b) => (a.born || a.published || a.created || 0) - (b.born || b.published || b.created || 0)
	);

	// Function to convert year to x position
	function yearToX(year: number): number {
		return (year - earliestYear) * YEAR_PIXEL_RATIO + PADDING;
	}

	// Generate major time markers (centuries)
	$: timeMarkers = Array.from(
		{ length: Math.ceil((latestYear - earliestYear) / 100) + 1 },
		(_, i) => Math.floor(earliestYear / 100) * 100 + i * 100
	);

	// Format year with BC/AD
	function formatYear(year: number): string {
		if (year === 0) return '0';
		return year < 0 ? `${Math.abs(year)}BC` : `${year}`;
	}

	// Distribute bars with guaranteed no overlap
	$: {
		// Group people by which side of the timeline they'll appear on
		const topPeople = [];
		const bottomPeople = [];

		// Assign people to top or bottom based on alternating pattern
		for (let i = 0; i < sorted.length; i++) {
			if (i % 2 === 0) {
				topPeople.push(sorted[i]);
				sorted[i].placement = 'top';
			} else {
				bottomPeople.push(sorted[i]);
				sorted[i].placement = 'bottom';
			}
		}

		// Function to sort people by row assignment
		function assignRows(peopleList) {
			// Sort by birth year first
			peopleList.sort(
				(a, b) =>
					(a.born || a.published || a.created || 0) - (b.born || b.published || b.created || 0)
			);

			// For each person, find the first available row that doesn't overlap
			for (let i = 0; i < peopleList.length; i++) {
				const person = peopleList[i];
				const personStart = person.born || person.published || person.created || 0;
				const personEnd =
					person.died || person.created || person.published || new Date().getFullYear();

				// Start checking from row 1
				let rowAssigned = false;
				let currentRow = 1;

				while (!rowAssigned && currentRow <= MAX_BARS_PER_SIDE) {
					// Check if this row has any overlapping people
					const hasOverlap = peopleList.some((p, idx) => {
						if (idx >= i || p.row !== currentRow) return false; // Only check people already assigned to this row

						const pStart = p.born || p.published || p.created || 0;
						const pEnd = p.died || p.created || p.published || new Date().getFullYear();

						// For books and artworks (dots), we check both time proximity and title length
						if (isDot(person) && isDot(p)) {
							// Estimate text width: roughly 6 pixels per character for font-size 11px
							const personTitleWidth = (person.title?.length || 0) * 6;
							const pTitleWidth = (p.title?.length || 0) * 6;
							const maxTitleWidth = Math.max(personTitleWidth, pTitleWidth);

							// Calculate required year distance based on title width
							// More pixels needed = more years of separation needed
							const requiredYearDistance = Math.max(50, maxTitleWidth / YEAR_PIXEL_RATIO);

							return Math.abs(personStart - pStart) < requiredYearDistance;
						}

						// For people (bars), or book-person combinations
						return personStart <= pEnd + 70 && personEnd >= pStart - 70; // Increased buffer (was 50)
					});

					if (!hasOverlap) {
						person.row = currentRow;
						rowAssigned = true;
					} else {
						currentRow++;
					}
				}

				// If we couldn't find a non-overlapping row, just use the highest one
				if (!rowAssigned) {
					person.row = MAX_BARS_PER_SIDE;
				}
			}
		}

		// Assign rows to both groups
		assignRows(topPeople);
		assignRows(bottomPeople);
	}

	let selectedPerson = null;
	let tooltipX = 0;
	let tooltipY = 0;

	// Panning state - using transform instead of scroll
	let isPanning = false;
	let startX = 0;
	let startY = 0;
	let panX = 0;
	let panY = 0;
	let lastPanX = 0;
	let lastPanY = 0;
	let container: HTMLElement | null = null;

	// Zoom state
	let touchStartDistance = 0;
	let initialScale = 1;
	let currentScale = 1;
	let containerWidth = 0;
	let containerHeight = 0;

	// Calculate minimum width to fill viewport
	$: effectiveWidth = Math.max(width, containerWidth / 0.5);

	// Initialize when mounted
	onMount(() => {
		container = document.querySelector('.timeline-container');
		if (container) {
			containerWidth = container.clientWidth;
			containerHeight = container.clientHeight;

			// Calculate initial zoom to fit the entire timeline on screen
			const scaleX = container.clientWidth / effectiveWidth;
			const scaleY = container.clientHeight / height;
			const fitScale = Math.min(scaleX, scaleY) * 0.9;

			currentScale = Math.max(0.3, Math.min(10, fitScale));

			// Center the content
			const scaledWidth = effectiveWidth * currentScale;
			const scaledHeight = height * currentScale;
			panX = (container.clientWidth - scaledWidth) / 2;
			panY = (container.clientHeight - scaledHeight) / 2;
		}
	});

	// Panning handlers
	function handleMouseDown(e: MouseEvent) {
		// Don't start panning if clicking on interactive elements
		if (
			(e.target as HTMLElement).closest(
				'.person-bar, .book-dot, .person-name, .book-title, .image-popup'
			)
		) {
			return;
		}

		// Close popup when clicking on background to start panning
		if (selectedPerson) {
			selectedPerson = null;
		}

		isPanning = true;
		startX = e.clientX;
		startY = e.clientY;
		lastPanX = panX;
		lastPanY = panY;
		if (container) container.style.cursor = 'grabbing';
	}

	function handleMouseMove(e: MouseEvent) {
		if (!isPanning) return;
		e.preventDefault();

		const dx = e.clientX - startX;
		const dy = e.clientY - startY;
		panX = lastPanX + dx;
		panY = lastPanY + dy;
	}

	function handleMouseUp() {
		isPanning = false;
		if (container) container.style.cursor = 'grab';
	}

	function handleMouseLeave() {
		if (isPanning) {
			isPanning = false;
			if (container) container.style.cursor = 'grab';
		}
	}

	// Mouse wheel zoom handler
	function handleWheel(e: WheelEvent) {
		e.preventDefault();

		const zoomSpeed = 0.002;
		const delta = -e.deltaY;
		const scaleChange = 1 + delta * zoomSpeed;
		const newScale = Math.max(0.1, Math.min(20, currentScale * scaleChange));

		if (newScale === currentScale) return;

		// Zoom towards mouse position
		if (container) {
			const rect = container.getBoundingClientRect();
			const mouseX = e.clientX - rect.left;
			const mouseY = e.clientY - rect.top;

			// Calculate the point in content coordinates before zoom
			const contentX = (mouseX - panX) / currentScale;
			const contentY = (mouseY - panY) / currentScale;

			// Update scale
			currentScale = newScale;

			// Adjust pan so the point under the mouse stays in place
			panX = mouseX - contentX * currentScale;
			panY = mouseY - contentY * currentScale;
		} else {
			currentScale = newScale;
		}
	}

	// Touch event handlers for mobile pinch-to-zoom
	function getTouchDistance(touches: TouchList) {
		const dx = touches[0].clientX - touches[1].clientX;
		const dy = touches[0].clientY - touches[1].clientY;
		return Math.sqrt(dx * dx + dy * dy);
	}

	function handleTouchStart(e: TouchEvent) {
		if (e.touches.length === 2) {
			e.preventDefault();
			touchStartDistance = getTouchDistance(e.touches);
			initialScale = currentScale;
		}
	}

	function handleTouchMove(e: TouchEvent) {
		if (e.touches.length === 2 && touchStartDistance > 0) {
			e.preventDefault();
			const currentDistance = getTouchDistance(e.touches);
			const scaleChange = currentDistance / touchStartDistance;
			currentScale = Math.max(0.1, Math.min(20, initialScale * scaleChange));
		}
	}

	function handleTouchEnd(e: TouchEvent) {
		if (e.touches.length < 2) {
			touchStartDistance = 0;
		}
	}

	// Item click handler for keyboard accessibility
	function handleItemClick(item, e) {
		selectedPerson = item;
		const constrainedPos = constrainPopupPosition(e.clientX, e.clientY);
		tooltipX = constrainedPos.x;
		tooltipY = constrainedPos.y;
		e.stopPropagation();
	}

	// Keyboard handler for accessibility
	function handleItemKeydown(item, e) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			selectedPerson = item;
			const rect = e.target.getBoundingClientRect();
			const constrainedPos = constrainPopupPosition(
				rect.left + rect.width / 2,
				rect.top + rect.height / 2
			);
			tooltipX = constrainedPos.x;
			tooltipY = constrainedPos.y;
		}
	}

	// Function to constrain popup position within viewport
	function constrainPopupPosition(clientX, clientY) {
		const popup = { width: 220, height: 300 }; // Approximate popup dimensions
		const margin = 20; // Margin from viewport edges

		let x = clientX;
		let y = clientY;

		// Constrain horizontally
		if (x + popup.width / 2 > window.innerWidth - margin) {
			x = window.innerWidth - popup.width / 2 - margin;
		}
		if (x - popup.width / 2 < margin) {
			x = popup.width / 2 + margin;
		}

		// Constrain vertically
		if (y + popup.height / 2 > window.innerHeight - margin) {
			y = window.innerHeight - popup.height / 2 - margin;
		}
		if (y - popup.height / 2 < margin) {
			y = popup.height / 2 + margin;
		}

		return { x, y };
	}
</script>

<div
	class="timeline-container"
	role="application"
	aria-label="Interactive timeline visualization - click and drag to pan, scroll to zoom, pinch to zoom on mobile"
	on:mousedown={handleMouseDown}
	on:mousemove={handleMouseMove}
	on:mouseup={handleMouseUp}
	on:mouseleave={handleMouseLeave}
	on:wheel={handleWheel}
	on:touchstart={handleTouchStart}
	on:touchmove={handleTouchMove}
	on:touchend={handleTouchEnd}
>
	<div
		class="timeline-content"
		style="transform: translate({panX}px, {panY}px) scale({currentScale}); transform-origin: 0 0;"
	>
		<svg width={effectiveWidth} {height}>
			<!-- Background -->
			<rect x="0" y="0" width={effectiveWidth} {height} fill="#17191C" />

			<!-- Time markers -->
			{#each timeMarkers as year}
				<line x1={yearToX(year)} y1={0} x2={yearToX(year)} y2={height} class="time-marker-line" />
				<text x={yearToX(year)} y={TIMELINE_Y - 20} text-anchor="middle" class="time-marker">
					{formatYear(year)}
				</text>
			{/each}

			<!-- Main timeline -->
			<line
				x1={PADDING}
				y1={TIMELINE_Y}
				x2={width - PADDING}
				y2={TIMELINE_Y}
				class="main-timeline"
			/>

			<!-- Person timelines -->
			{#each sorted as item, index}
				<!-- Calculate positions -->
				{@const yearValue = item.born || item.published || item.created || 0}
				{@const isItemBook = isBook(item)}
				{@const isItemArtwork = isArtwork(item)}
				{@const isItemDot = isItemBook || isItemArtwork}
				{@const displayName = isItemDot ? item.title : item.name}

				{#if isItemDot}
					<!-- Book/Artwork representation (dot) -->
					{@const xPos = yearToX(yearValue)}

					<!-- Calculate Y position based on placement and row -->
					{@const isTop = item.placement === 'top'}
					{@const rowOffset = (item.row - 1) * (BAR_HEIGHT + BAR_GAP)}
					{@const yPos = isTop
						? TIMELINE_Y - BAR_OFFSET - rowOffset - BAR_HEIGHT / 2
						: TIMELINE_Y + BAR_OFFSET + rowOffset + BAR_HEIGHT / 2}

					{@const dotColor = isItemArtwork ? '#FF6B9D' : '#4A9EFF'}
					{@const itemDescription = isItemArtwork
						? `{displayName} by {item.artist}, created {formatYear(yearValue)}`
						: `{displayName} by {item.author}, published {formatYear(yearValue)}`}

					<!-- Dot group with pointer events -->
					<g
						role="button"
						tabindex="0"
						aria-label={itemDescription}
						on:click={(e) => handleItemClick(item, e)}
						on:keydown={(e) => handleItemKeydown(item, e)}
					>
						<!-- Title -->
						<text
							x={xPos}
							y={yPos + (isTop ? -NAME_OFFSET - 6 : NAME_OFFSET + 6)}
							text-anchor="middle"
							class="book-title"
							style="fill: {isItemArtwork ? '#FF6B9D' : '#4A9EFF'}"
						>
							{displayName}
						</text>

						<!-- Dot -->
						<circle
							cx={xPos}
							cy={yPos}
							r={DOT_RADIUS}
							class="book-dot"
							style="fill: {dotColor}; stroke: {dotColor}"
						/>

						<!-- Connecting line to timeline -->
						<line
							x1={xPos}
							y1={yPos + (isTop ? DOT_RADIUS : -DOT_RADIUS)}
							x2={xPos}
							y2={TIMELINE_Y + (isTop ? -3 : 3)}
							stroke="#555"
							stroke-width="0.5"
							stroke-dasharray="2 2"
						/>
					</g>
				{:else}
					<!-- Person representation (lifespan bar) -->
					{@const deathYear = item.died || new Date().getFullYear()}
					{@const xStart = yearToX(yearValue)}
					{@const xEnd = yearToX(deathYear)}
					{@const barWidth = Math.max(xEnd - xStart, 5)}
					<!-- Ensure minimum visibility -->

					<!-- Calculate Y position based on placement and row -->
					{@const isTop = item.placement === 'top'}
					{@const rowOffset = (item.row - 1) * (BAR_HEIGHT + BAR_GAP)}
					{@const yPos = isTop
						? TIMELINE_Y - BAR_OFFSET - rowOffset - BAR_HEIGHT
						: TIMELINE_Y + BAR_OFFSET + rowOffset}

					<!-- Person bar group with pointer events -->
					<g
						role="button"
						tabindex="0"
						aria-label="{displayName}, {selectedPerson?.born
							? formatYear(item.born)
							: ''} to {item.died ? formatYear(item.died) : 'present'}"
						on:click={(e) => handleItemClick(item, e)}
						on:keydown={(e) => handleItemKeydown(item, e)}
					>
						<!-- Person name -->
						<text
							x={xStart + barWidth / 2}
							y={yPos + (isTop ? -NAME_OFFSET : BAR_HEIGHT + NAME_OFFSET)}
							text-anchor="middle"
							class="person-name"
						>
							{displayName}
						</text>

						<!-- Person lifespan bar -->
						<rect x={xStart} y={yPos} width={barWidth} height={BAR_HEIGHT} class="person-bar" />

						<!-- Connecting line to timeline -->
						<line
							x1={xStart + barWidth / 2}
							y1={yPos + (isTop ? BAR_HEIGHT : 0)}
							x2={xStart + barWidth / 2}
							y2={TIMELINE_Y + (isTop ? -3 : 3)}
							stroke="#555"
							stroke-width="0.5"
							stroke-dasharray="2 2"
						/>
					</g>
				{/if}
			{/each}
		</svg>
	</div>

	{#if selectedPerson}
		<div class="image-popup" style="left: {tooltipX}px; top: {tooltipY}px;">
			<img
				src={resolveBasePath(selectedPerson.image)}
				alt={selectedPerson.name || selectedPerson.title}
			/>
			<h4>{selectedPerson.name || selectedPerson.title}</h4>
			<p>
				{#if selectedPerson.created}
					{selectedPerson.artist}<br />
					{formatYear(selectedPerson.created)}
				{:else if selectedPerson.published}
					{selectedPerson.author}<br />
					{formatYear(selectedPerson.published)}
				{:else}
					{selectedPerson.born ? formatYear(selectedPerson.born) : ''} -
					{selectedPerson.died ? formatYear(selectedPerson.died) : 'present'}
					({selectedPerson.died
						? Math.abs(selectedPerson.died - selectedPerson.born)
						: Math.abs(new Date().getFullYear() - selectedPerson.born)} years)
				{/if}
			</p>
			<button
				style="position: absolute; top: 5px; right: 5px; background: none; border: none; color: white; cursor: pointer; font-size: 16px;"
				on:click={() => (selectedPerson = null)}
			>
				×
			</button>
		</div>
	{/if}
</div>

<style>
	.timeline-container {
		width: 100%;
		height: 100vh;
		background-color: #17191c; /* Match SVG background to hide border */
		position: relative;
		overflow: hidden;
		cursor: grab;
		user-select: none; /* Prevent text selection while dragging */
	}

	.timeline-container:active {
		cursor: grabbing;
	}

	.timeline-content {
		position: relative;
		transition: transform 0.1s ease-out;
	}

	svg {
		display: block;
	}

	.time-marker {
		fill: #999;
		font-size: 12px;
	}

	.time-marker-line {
		stroke: #333;
		stroke-width: 1;
		stroke-dasharray: 2 4;
	}

	.main-timeline {
		stroke: #555;
		stroke-width: 3;
	}

	.person-name,
	.book-title {
		fill: #fff;
		font-size: 11px;
		dominant-baseline: middle;
		pointer-events: all;
		cursor: pointer;
	}

	.person-name:hover,
	.book-title:hover {
		fill: #fa6742;
	}

	.book-title {
		fill: #58b5f3;
	}

	.person-bar {
		fill: #fa6742;
		rx: 2;
		ry: 2;
		opacity: 0.75;
		transition: opacity 0.2s;
		pointer-events: all;
		cursor: pointer;
	}

	.person-bar:hover {
		opacity: 1;
	}

	.book-dot {
		fill: #58b5f3;
		opacity: 0.9;
		transition:
			opacity 0.2s,
			r 0.2s;
		pointer-events: all;
		cursor: pointer;
	}

	.book-dot:hover {
		opacity: 1;
		r: 8;
	}

	/* Remove focus outline on click */
	g:focus {
		outline: none;
	}

	.image-popup {
		position: fixed;
		background-color: #23272f;
		padding: 15px;
		border-radius: 12px;
		box-shadow: 0 6px 25px rgba(0, 0, 0, 0.6);
		z-index: 100;
		border: 1px solid #333;
		max-width: 300px;
		transform: translate(-50%, -50%);
		cursor: auto;
		user-select: text;
	}

	.image-popup img {
		width: 100%;
		max-height: 375px;
		object-fit: cover;
		border-radius: 6px;
	}

	.image-popup h4 {
		margin: 12px 0 6px;
		color: #fff;
		text-align: center;
		font-size: 1.2rem;
		user-select: text;
	}

	.image-popup p {
		margin: 0;
		font-size: 1rem;
		color: #aaa;
		text-align: center;
		user-select: text;
	}
</style>
