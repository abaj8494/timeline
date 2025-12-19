<script lang="ts">
  import { onMount } from 'svelte';
  
  export let items: {
    id: string;
    title: string;
    subtitle?: string;
    kind: 'point' | 'range';
    start: number;
    end: number;
    approx?: boolean;
    labelTime?: string;
    tags?: string[];
    region?: string;
  }[];
  
  export let scaleType: 'log' | 'linear' = 'linear';

  // Constants for visualization
  const PADDING = 60;
  const TIMELINE_Y = 500;
  const BAR_HEIGHT = 12;
  const BAR_GAP = 35;
  const BAR_OFFSET = 60;
  const NAME_OFFSET = 8;
  const MAX_BARS_PER_SIDE = 20;
  
  // Calculate time range
  $: minTime = Math.min(...items.map(i => i.start));
  $: maxTime = Math.max(...items.map(i => i.end));
  
  // For logarithmic scale, we need to handle negative (BC) years specially
  // We'll use a shifted log scale where we add an offset to make all values positive
  $: timeOffset = minTime < 0 ? Math.abs(minTime) + 1 : 0;
  
  // Width calculations
  const BASE_LINEAR_WIDTH = 3000;
  const BASE_LOG_WIDTH = 2500;
  
  $: calculatedWidth = scaleType === 'log' 
    ? BASE_LOG_WIDTH 
    : Math.max(BASE_LINEAR_WIDTH, (maxTime - minTime) * 0.15);
  
  let containerWidth = 0;
  $: effectiveWidth = Math.max(calculatedWidth, containerWidth / 0.5) + (PADDING * 2);
  
  // Height calculation
  $: height = TIMELINE_Y + (PADDING * 3) + (MAX_BARS_PER_SIDE * 2) * (BAR_HEIGHT + BAR_GAP);
  
  // Sort by start time
  $: sorted = [...items].sort((a, b) => a.start - b.start);
  
  // Convert time to x position
  function timeToX(time: number): number {
    const usableWidth = effectiveWidth - (PADDING * 2);
    
    if (scaleType === 'log') {
      // Logarithmic scale with offset for negative values
      const logMin = Math.log10(minTime + timeOffset + 1);
      const logMax = Math.log10(maxTime + timeOffset + 1);
      const logTime = Math.log10(time + timeOffset + 1);
      
      const ratio = (logTime - logMin) / (logMax - logMin);
      return PADDING + (ratio * usableWidth);
    } else {
      // Linear scale
      const ratio = (time - minTime) / (maxTime - minTime);
      return PADDING + (ratio * usableWidth);
    }
  }
  
  // Generate time markers
  $: timeMarkers = generateTimeMarkers();
  
  function generateTimeMarkers() {
    const markers = [];
    const range = maxTime - minTime;
    
    if (scaleType === 'log') {
      // For logarithmic scale, use powers of 10
      const powers = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0];
      for (const p of powers) {
        const value = Math.pow(10, Math.abs(p)) * (p < 0 ? -1 : 1);
        if (value >= minTime && value <= maxTime) {
          markers.push(value);
        }
      }
      // Add some key dates
      const keyDates = [-13800000000, -4500000000, -1000000000, -100000000, -10000000, -1000000, -100000, -10000, -1000, 0, 1000, 2000];
      for (const d of keyDates) {
        if (d >= minTime && d <= maxTime && !markers.includes(d)) {
          markers.push(d);
        }
      }
    } else {
      // For linear scale, calculate appropriate intervals
      let interval;
      if (range > 10000) interval = 2000;
      else if (range > 5000) interval = 1000;
      else if (range > 1000) interval = 500;
      else if (range > 500) interval = 100;
      else interval = 50;
      
      const startMarker = Math.ceil(minTime / interval) * interval;
      for (let m = startMarker; m <= maxTime; m += interval) {
        markers.push(m);
      }
    }
    
    return markers.sort((a, b) => a - b);
  }
  
  // Format time for display
  function formatTime(time: number): string {
    const absTime = Math.abs(time);
    
    if (absTime >= 1000000000) {
      return `${(time / 1000000000).toFixed(1)} Ga`;
    } else if (absTime >= 1000000) {
      return `${(time / 1000000).toFixed(1)} Ma`;
    } else if (absTime >= 1000) {
      if (time < 0) {
        return `${Math.abs(time)} BC`;
      }
      return `${time} AD`;
    } else {
      if (time < 0) {
        return `${Math.abs(time)} BC`;
      }
      return `${time} AD`;
    }
  }
  
  // Distribute bars with no overlap
  $: {
    const topItems = [];
    const bottomItems = [];
    
    for (let i = 0; i < sorted.length; i++) {
      if (i % 2 === 0) {
        topItems.push(sorted[i]);
        sorted[i].placement = 'top';
      } else {
        bottomItems.push(sorted[i]);
        sorted[i].placement = 'bottom';
      }
    }
    
    function assignRows(itemList) {
      itemList.sort((a, b) => a.start - b.start);
      
      for (let i = 0; i < itemList.length; i++) {
        const item = itemList[i];
        const itemStartX = timeToX(item.start);
        const itemEndX = timeToX(item.end);
        
        let rowAssigned = false;
        let currentRow = 1;
        
        while (!rowAssigned && currentRow <= MAX_BARS_PER_SIDE) {
          const hasOverlap = itemList.some((other, idx) => {
            if (idx >= i || other.row !== currentRow) return false;
            
            const otherStartX = timeToX(other.start);
            const otherEndX = timeToX(other.end);
            const buffer = 50;
            
            return (itemStartX <= otherEndX + buffer) && (itemEndX >= otherStartX - buffer);
          });
          
          if (!hasOverlap) {
            item.row = currentRow;
            rowAssigned = true;
          } else {
            currentRow++;
          }
        }
        
        if (!rowAssigned) {
          item.row = MAX_BARS_PER_SIDE;
        }
      }
    }
    
    assignRows(topItems);
    assignRows(bottomItems);
  }
  
  let selectedItem = null;
  let tooltipX = 0;
  let tooltipY = 0;
  
  // Panning state
  let isPanning = false;
  let startX = 0;
  let startY = 0;
  let scrollLeft = 0;
  let scrollTop = 0;
  let container;
  
  // Touch/zoom state
  let touchStartDistance = 0;
  let initialScale = 1;
  let currentScale = 1;
  
  onMount(() => {
    container = document.querySelector('.event-timeline-container');
    if (container) {
      containerWidth = container.clientWidth;
      
      const content = container.querySelector('.timeline-content');
      if (content) {
        const scaleX = container.clientWidth / effectiveWidth;
        const scaleY = container.clientHeight / height;
        const fitScale = Math.min(scaleX, scaleY) * 0.95;
        
        currentScale = Math.max(0.1, Math.min(50, fitScale));
        content.style.transform = `scale(${currentScale})`;
        content.style.transformOrigin = 'top left';
        
        const scaledWidth = effectiveWidth * currentScale;
        const scaledHeight = height * currentScale;
        container.scrollLeft = Math.max(0, (scaledWidth - container.clientWidth) / 2);
        container.scrollTop = Math.max(0, (scaledHeight - container.clientHeight) / 2);
      }
    }
  });
  
  function handleMouseDown(e) {
    if (e.target.closest('.event-bar, .event-label, .event-popup')) return;
    if (selectedItem) selectedItem = null;
    
    isPanning = true;
    startX = e.pageX - container.offsetLeft;
    startY = e.pageY - container.offsetTop;
    scrollLeft = container.scrollLeft;
    scrollTop = container.scrollTop;
    container.style.cursor = 'grabbing';
  }
  
  function handleMouseMove(e) {
    if (!isPanning) return;
    e.preventDefault();
    
    const x = e.pageX - container.offsetLeft;
    const y = e.pageY - container.offsetTop;
    const walkX = (x - startX) * 1.5;
    const walkY = (y - startY) * 1.5;
    
    container.scrollLeft = scrollLeft - walkX;
    container.scrollTop = scrollTop - walkY;
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
  
  function handleWheel(e) {
    e.preventDefault();
    
    const zoomSpeed = 0.001;
    const delta = -e.deltaY;
    const scaleChange = 1 + (delta * zoomSpeed);
    const newScale = Math.max(0.1, Math.min(50, currentScale * scaleChange));
    
    if (newScale === currentScale) return;
    
    const rect = container.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    const scrollX = container.scrollLeft;
    const scrollY = container.scrollTop;
    const contentX = (scrollX + mouseX) / currentScale;
    const contentY = (scrollY + mouseY) / currentScale;
    
    currentScale = newScale;
    
    const content = container?.querySelector('.timeline-content');
    if (content) {
      content.style.transform = `scale(${currentScale})`;
      content.style.transformOrigin = 'top left';
    }
    
    container.scrollLeft = (contentX * newScale) - mouseX;
    container.scrollTop = (contentY * newScale) - mouseY;
  }
  
  function getTouchDistance(touches) {
    const dx = touches[0].clientX - touches[1].clientX;
    const dy = touches[0].clientY - touches[1].clientY;
    return Math.sqrt(dx * dx + dy * dy);
  }
  
  function handleTouchStart(e) {
    if (e.touches.length === 2) {
      e.preventDefault();
      touchStartDistance = getTouchDistance(e.touches);
      initialScale = currentScale;
    }
  }
  
  function handleTouchMove(e) {
    if (e.touches.length === 2 && touchStartDistance > 0) {
      e.preventDefault();
      const currentDistance = getTouchDistance(e.touches);
      const scaleChange = currentDistance / touchStartDistance;
      currentScale = Math.max(0.1, Math.min(50, initialScale * scaleChange));
      
      const content = container?.querySelector('.timeline-content');
      if (content) {
        content.style.transform = `scale(${currentScale})`;
        content.style.transformOrigin = 'top left';
      }
    }
  }
  
  function handleTouchEnd(e) {
    if (e.touches.length < 2) touchStartDistance = 0;
  }
  
  function handleItemClick(item, e) {
    selectedItem = item;
    const constrainedPos = constrainPopupPosition(e.clientX, e.clientY);
    tooltipX = constrainedPos.x;
    tooltipY = constrainedPos.y;
    e.stopPropagation();
  }
  
  function handleItemKeydown(item, e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      selectedItem = item;
      const rect = e.target.getBoundingClientRect();
      const constrainedPos = constrainPopupPosition(rect.left + rect.width / 2, rect.top + rect.height / 2);
      tooltipX = constrainedPos.x;
      tooltipY = constrainedPos.y;
    }
  }
  
  function constrainPopupPosition(clientX, clientY) {
    const popup = { width: 300, height: 200 };
    const margin = 20;
    
    let x = clientX;
    let y = clientY;
    
    if (x + popup.width/2 > window.innerWidth - margin) {
      x = window.innerWidth - popup.width/2 - margin;
    }
    if (x - popup.width/2 < margin) {
      x = popup.width/2 + margin;
    }
    if (y + popup.height/2 > window.innerHeight - margin) {
      y = window.innerHeight - popup.height/2 - margin;
    }
    if (y - popup.height/2 < margin) {
      y = popup.height/2 + margin;
    }
    
    return { x, y };
  }
  
  // Get color based on tags
  function getEventColor(item) {
    const tags = item.tags || [];
    if (tags.includes('extinction')) return '#EF4444';
    if (tags.includes('war')) return '#DC2626';
    if (tags.includes('biology')) return '#22C55E';
    if (tags.includes('humanity')) return '#F59E0B';
    if (tags.includes('politics')) return '#6366F1';
    if (tags.includes('religion') || tags.includes('philosophy')) return '#8B5CF6';
    if (tags.includes('science') || tags.includes('technology')) return '#3B82F6';
    if (tags.includes('culture') || tags.includes('art')) return '#EC4899';
    if (tags.includes('economy')) return '#14B8A6';
    if (tags.includes('cosmology') || tags.includes('astronomy') || tags.includes('physics')) return '#06B6D4';
    if (tags.includes('earth') || tags.includes('chemistry')) return '#84CC16';
    return '#FA6742';
  }
</script>

<style>
  .event-timeline-container {
    width: 100%;
    height: 100vh;
    background-color: #17191C;
    position: relative;
    overflow: auto;
    cursor: grab;
    user-select: none;
  }
  
  .event-timeline-container:active {
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
    font-size: 11px;
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
  
  .event-bar {
    opacity: 0.85;
    transition: opacity 0.2s;
    pointer-events: all;
    cursor: pointer;
  }
  
  .event-bar:hover {
    opacity: 1;
  }
  
  .event-label {
    fill: #fff;
    font-size: 10px;
    dominant-baseline: middle;
    pointer-events: all;
    cursor: pointer;
  }
  
  .event-label:hover {
    fill: #FA6742;
  }
  
  g:focus {
    outline: none;
  }
  
  .event-popup {
    position: fixed;
    background-color: #23272F;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    z-index: 100;
    border: 1px solid #444;
    max-width: 280px;
    transform: translate(-50%, -50%);
  }
  
  .event-popup h4 {
    margin: 0 0 8px;
    color: #fff;
    font-size: 1.1rem;
    padding-right: 24px;
  }
  
  .event-popup .subtitle {
    margin: 0 0 12px;
    font-size: 0.9rem;
    color: #ccc;
    line-height: 1.4;
  }
  
  .event-popup .time-label {
    font-size: 0.85rem;
    color: #999;
    margin-bottom: 10px;
  }
  
  .event-popup .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  
  .event-popup .tag {
    background: rgba(250, 103, 66, 0.2);
    color: #FA6742;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    text-transform: uppercase;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    font-size: 18px;
    padding: 4px;
    line-height: 1;
  }
  
  .close-btn:hover {
    color: #fff;
  }
</style>

<div 
  class="event-timeline-container"
  role="application"
  aria-label="Interactive event timeline - click and drag to pan, scroll to zoom"
  on:mousedown={handleMouseDown}
  on:mousemove={handleMouseMove}
  on:mouseup={handleMouseUp}
  on:mouseleave={handleMouseLeave}
  on:wheel={handleWheel}
  on:touchstart={handleTouchStart}
  on:touchmove={handleTouchMove}
  on:touchend={handleTouchEnd}
>
  <div class="timeline-content" style="width: {effectiveWidth * currentScale}px; height: {height * currentScale}px;">
    <svg width={effectiveWidth} height={height}>
      <!-- Background -->
      <rect x="0" y="0" width={effectiveWidth} height={height} fill="#17191C" />
      
      <!-- Time markers -->
      {#each timeMarkers as marker}
        {@const xPos = timeToX(marker)}
        {#if xPos >= PADDING && xPos <= effectiveWidth - PADDING}
          <line 
            x1={xPos} 
            y1={0} 
            x2={xPos} 
            y2={height} 
            class="time-marker-line" 
          />
          <text 
            x={xPos} 
            y={TIMELINE_Y - 15} 
            text-anchor="middle" 
            class="time-marker"
          >
            {formatTime(marker)}
          </text>
        {/if}
      {/each}
      
      <!-- Main timeline -->
      <line 
        x1={PADDING} 
        y1={TIMELINE_Y} 
        x2={effectiveWidth - PADDING} 
        y2={TIMELINE_Y} 
        class="main-timeline" 
      />
      
      <!-- Events -->
      {#each sorted as item}
        {@const xStart = timeToX(item.start)}
        {@const xEnd = timeToX(item.end)}
        {@const barWidth = Math.max(xEnd - xStart, 8)}
        {@const isTop = item.placement === 'top'}
        {@const rowOffset = (item.row - 1) * (BAR_HEIGHT + BAR_GAP)}
        {@const yPos = isTop 
          ? TIMELINE_Y - BAR_OFFSET - rowOffset - BAR_HEIGHT
          : TIMELINE_Y + BAR_OFFSET + rowOffset}
        {@const color = getEventColor(item)}
        
        <g 
          role="button"
          tabindex="0"
          aria-label="{item.title}"
          on:click={(e) => handleItemClick(item, e)}
          on:keydown={(e) => handleItemKeydown(item, e)}
        >
          <!-- Event title -->
          <text 
            x={xStart + barWidth/2} 
            y={yPos + (isTop ? -NAME_OFFSET : BAR_HEIGHT + NAME_OFFSET + 4)} 
            text-anchor="middle" 
            class="event-label"
          >
            {item.title}
          </text>
          
          <!-- Event bar -->
          <rect 
            x={xStart} 
            y={yPos} 
            width={barWidth} 
            height={BAR_HEIGHT} 
            rx="3"
            ry="3"
            class="event-bar"
            style="fill: {color}"
          />
          
          <!-- Connecting line to timeline -->
          <line 
            x1={xStart + barWidth/2} 
            y1={yPos + (isTop ? BAR_HEIGHT : 0)} 
            x2={xStart + barWidth/2} 
            y2={TIMELINE_Y + (isTop ? -3 : 3)} 
            stroke="#555" 
            stroke-width="0.5" 
            stroke-dasharray="2 2" 
          />
        </g>
      {/each}
    </svg>
  </div>
  
  {#if selectedItem}
    <div 
      class="event-popup" 
      style="left: {tooltipX}px; top: {tooltipY}px;"
    >
      <button class="close-btn" on:click={() => selectedItem = null}>×</button>
      <h4>{selectedItem.title}</h4>
      {#if selectedItem.subtitle}
        <p class="subtitle">{selectedItem.subtitle}</p>
      {/if}
      <div class="time-label">
        {selectedItem.labelTime || formatTime(selectedItem.start)}
        {#if selectedItem.region}
          <br/>{selectedItem.region}
        {/if}
      </div>
      {#if selectedItem.tags && selectedItem.tags.length > 0}
        <div class="tags">
          {#each selectedItem.tags as tag}
            <span class="tag">{tag}</span>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>
