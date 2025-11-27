<!-- src/routes/search/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import people from '$lib/data/people.json';
  import books from '$lib/data/books.json';
  import { resolveBasePath } from '$lib/utils/paths';

  let searchTerm = '';
  let searchResults = [];
  let selectedItem = null;

  // Combined search function
  $: if (searchTerm.trim()) {
    const term = searchTerm.toLowerCase();
    
    // Search people
    const foundPeople = people
      .filter(person => 
        person.name.toLowerCase().includes(term) ||
        (person.born && person.born.toString().includes(term)) ||
        (person.died && person.died.toString().includes(term))
      )
      .map(person => ({
        ...person,
        type: 'person',
        displayName: person.name,
        dateRange: `${person.born || '?'} - ${person.died || 'present'}`
      }));

    // Search books
    const foundBooks = books
      .filter(book => 
        book.title.toLowerCase().includes(term) ||
        book.author.toLowerCase().includes(term) ||
        (book.published && book.published.toString().includes(term))
      )
      .map(book => ({
        ...book,
        type: 'book',
        displayName: book.title,
        dateRange: `${book.published} • ${book.author}`
      }));

    // Combine and sort by relevance (name matches first, then date matches)
    searchResults = [...foundPeople, ...foundBooks].sort((a, b) => {
      const aNameMatch = a.displayName.toLowerCase().includes(term);
      const bNameMatch = b.displayName.toLowerCase().includes(term);
      
      if (aNameMatch && !bNameMatch) return -1;
      if (!aNameMatch && bNameMatch) return 1;
      
      // If both match name or both don't, sort by date
      const aDate = a.born || a.published || 0;
      const bDate = b.born || b.published || 0;
      return aDate - bDate;
    });
  } else {
    searchResults = [];
  }

  function selectItem(item) {
    selectedItem = item;
  }

  function goToTimeline(type) {
    if (type === 'person') {
      window.location.href = `${base}/people`;
    } else {
      window.location.href = `${base}/books`;
    }
  }

  onMount(() => {
    // Focus search input on mount
    const input = document.querySelector('.search-input');
    if (input) {
      input.focus();
    }
  });
</script>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    background-color: #1C1E21;
    color: white;
    font-family: system-ui, -apple-system, sans-serif;
  }
  
  .search-page {
    min-height: 100vh;
    padding: 40px 20px;
    max-width: 1000px;
    margin: 0 auto;
  }

  .header {
    text-align: center;
    margin-bottom: 40px;
  }

  .title {
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 10px;
    color: #FA6742;
  }

  .subtitle {
    color: #999;
    font-size: 1.1rem;
  }

  .search-container {
    max-width: 600px;
    margin: 0 auto 40px;
  }

  .search-input {
    width: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    border: 2px solid #333;
    border-radius: 30px;
    padding: 15px 25px;
    color: white;
    font-size: 18px;
    outline: none;
    transition: border-color 0.3s;
  }

  .search-input:focus {
    border-color: #FA6742;
  }

  .search-input::placeholder {
    color: #666;
  }

  .results-container {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 40px;
    align-items: start;
  }

  @media (max-width: 768px) {
    .results-container {
      grid-template-columns: 1fr;
    }
  }

  .results-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .result-item {
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 12px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid transparent;
  }

  .result-item:hover {
    background-color: rgba(0, 0, 0, 0.6);
    transform: translateY(-2px);
  }

  .result-item.selected {
    border-color: #FA6742;
    background-color: rgba(250, 103, 66, 0.1);
  }

  .result-header {
    display: flex;
    justify-content: between;
    align-items: center;
    margin-bottom: 8px;
  }

  .result-name {
    font-size: 1.2rem;
    font-weight: 600;
    color: white;
  }

  .result-type {
    background-color: #FA6742;
    color: white;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.8rem;
    text-transform: uppercase;
    margin-left: auto;
  }

  .result-type.book {
    background-color: #58B5F3;
  }

  .result-date {
    color: #999;
    font-size: 0.9rem;
  }

  .detail-panel {
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 12px;
    padding: 20px;
    position: sticky;
    top: 20px;
  }

  .detail-image {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 15px;
  }

  .detail-name {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: white;
  }

  .detail-info {
    color: #999;
    margin-bottom: 15px;
  }

  .view-timeline-btn {
    width: 100%;
    background-color: #FA6742;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .view-timeline-btn:hover {
    background-color: #e55a35;
  }

  .no-results {
    text-align: center;
    color: #666;
    font-size: 1.1rem;
    margin-top: 40px;
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

  .navigation-link {
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
    transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .navigation-link:hover {
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
    
    .navigation-link {
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
    
    .navigation-link {
      width: 44px;
      height: 44px;
      font-size: 20px;
    }
  }
</style>

<div class="navigation-controls">
  <a href="{base}/people" class="navigation-link" title="People Timeline">👤</a>
  <a href="{base}/books" class="navigation-link" title="Books Timeline">📚</a>
  <a href="{base}/artworks" class="navigation-link" title="Artworks Timeline">🎨</a>
  <a href="{base}/list" class="navigation-link" title="List View">📋</a>
</div>

<div class="search-page">
  <div class="header">
    <h1 class="title">Search Timeline</h1>
    <p class="subtitle">Find people and books across history</p>
  </div>

  <div class="search-container">
    <input 
      type="text" 
      class="search-input"
      placeholder="Search for people, books, years..."
      bind:value={searchTerm}
    />
  </div>

  {#if searchTerm.trim()}
    {#if searchResults.length > 0}
      <div class="results-container">
        <div class="results-list">
          {#each searchResults as item (item.id)}
            <div 
              class="result-item"
              class:selected={selectedItem?.id === item.id}
              role="button"
              tabindex="0"
              aria-label="View details for {item.displayName}"
              on:click={() => selectItem(item)}
              on:keydown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  selectItem(item);
                }
              }}
            >
              <div class="result-header">
                <div class="result-name">{item.displayName}</div>
                <div class="result-type" class:book={item.type === 'book'}>
                  {item.type}
                </div>
              </div>
              <div class="result-date">{item.dateRange}</div>
            </div>
          {/each}
        </div>

        <div class="detail-panel">
          {#if selectedItem}
            <img 
              src={resolveBasePath(selectedItem.image)} 
              alt={selectedItem.displayName}
              class="detail-image"
            />
            <div class="detail-name">{selectedItem.displayName}</div>
            <div class="detail-info">
              {#if selectedItem.type === 'person'}
                {selectedItem.born || '?'} - {selectedItem.died || 'present'}
                {#if selectedItem.died && selectedItem.born}
                  <br/>({selectedItem.died - selectedItem.born} years old)
                {/if}
              {:else}
                Published: {selectedItem.published}<br/>
                Author: {selectedItem.author}
              {/if}
            </div>
            <button 
              class="view-timeline-btn"
              on:click={() => goToTimeline(selectedItem.type)}
            >
              View in Timeline
            </button>
          {:else}
            <div style="text-align: center; color: #666;">
              Click on a result to see details
            </div>
          {/if}
        </div>
      </div>
    {:else}
      <div class="no-results">
        No results found for "{searchTerm}"
      </div>
    {/if}
  {:else}
    <div class="no-results">
      Start typing to search people and books...
    </div>
  {/if}
</div> 