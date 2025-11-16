<!-- src/routes/people/+page.svelte -->
<script lang="ts">
  import TimelineChart from '$lib/components/TimelineChart.svelte';
  import people from '$lib/data/people.json';
  import { base } from '$app/paths';

  export let data;
</script>

<svelte:head>
  <title>{data.title}</title>
  <meta name="description" content={data.description} />
  <meta property="og:title" content={data.title} />
  <meta property="og:description" content={data.description} />
  <meta property="og:image" content={data.ogImage} />
  <meta property="og:url" content="https://yourdomain.com/shrine/people" />
  <meta name="twitter:title" content={data.title} />
  <meta name="twitter:description" content={data.description} />
  <meta name="twitter:image" content={data.ogImage} />
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
    gap: 10px;
  }
  
  .navigation-icon {
    background-color: rgba(0, 0, 0, 0.6);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    text-decoration: none;
    font-size: 24px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s, background-color 0.2s;
    border: none;
    cursor: pointer;
  }
  
  .navigation-icon:hover {
    transform: scale(1.1);
    background-color: rgba(0, 0, 0, 0.8);
  }


</style>

<div class="timeline-wrapper">
  <TimelineChart items={people} />
</div>

<div class="navigation-controls">
  <a href="{base}/books" class="navigation-icon" title="Go to Books Timeline">📚</a>
  <a href="{base}/list" class="navigation-icon" title="List View">📋</a>
  <a href="{base}/search" class="navigation-icon" title="Search Timeline">🔍</a>
</div>

