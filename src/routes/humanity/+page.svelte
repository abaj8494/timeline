<!-- src/routes/humanity/+page.svelte -->
<script lang="ts">
  import EventTimeline from '$lib/components/EventTimeline.svelte';
  import humanity from '$lib/data/humanity.json';
  import { base } from '$app/paths';

  export let data;
</script>

<svelte:head>
  <title>{data.title}</title>
  <meta name="description" content={data.description} />
  <meta property="og:title" content={data.title} />
  <meta property="og:description" content={data.description} />
  <meta property="og:url" content="https://yourdomain.com/timeline/humanity" />
</svelte:head>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    background-color: #1C1E21;
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
    transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
    border: 1px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
  }
  
  .navigation-icon:hover {
    transform: scale(1.1);
    background-color: rgba(0, 0, 0, 0.95);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
  }
  
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

<div class="timeline-wrapper">
  <EventTimeline items={humanity} scaleType="linear" />
</div>

<div class="navigation-controls">
  <a href="{base}/cosmic" class="navigation-icon" title="Cosmic Timeline">🌌</a>
  <a href="{base}/people" class="navigation-icon" title="People Timeline">👤</a>
  <a href="{base}/books" class="navigation-icon" title="Books Timeline">📚</a>
  <a href="{base}/artworks" class="navigation-icon" title="Artworks Timeline">🎨</a>
  <a href="{base}/search" class="navigation-icon" title="Search Timeline">🔍</a>
</div>
