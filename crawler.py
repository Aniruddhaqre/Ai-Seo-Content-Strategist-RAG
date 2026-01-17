import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, PruningContentFilter, DefaultMarkdownGenerator
from utils import remove_links_from_markdown

async def crawl_batch(urls, batch_size=50, max_concurrency=5):
    """
    urls: List of 1000 URLs
    batch_size: Saves results to disk every 50 URLs
    max_concurrency: Only processes 5 URLs at a time to save RAM
    """
    
    # 1. Setup Filters (Keep these outside the loop to save memory)
    pruning_filter = PruningContentFilter(
        threshold=0.45, 
        threshold_type="fixed", 
        min_word_threshold=50
    )
    md_generator = DefaultMarkdownGenerator(content_filter=pruning_filter)

    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        excluded_tags=['nav', 'footer', 'header', 'aside', 'form', 'noscript'],
        exclude_external_links=True,
        exclude_social_media_links=True
    )

    # 2. Concurrency Control
    semaphore = asyncio.Semaphore(max_concurrency)

    async def throttled_crawl(url, crawler):
        async with semaphore:
            try:
                # We use a session_id to reuse browser tabs effectively
                res = await crawler.arun(url=url, config=config, session_id="my_session")
                if res.success:
                    return {
                        "url": url,
                        "title": res.metadata.get("title"),
                        "metadata": res.metadata,
                        "description": res.metadata.get("description"),
                        "language": res.metadata.get("language"),
                        "cleaned_markdown": remove_links_from_markdown(res.markdown),
                        "markdown": res.markdown,
                    }
            except Exception as e:
                return {"url": url, "error": str(e)}
            return None

    final_results = []

    # 3. Process in chunks to protect 8GB RAM
    async with AsyncWebCrawler() as crawler:
        for i in range(0, len(urls), batch_size):
            chunk = urls[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1} ({i} to {i+batch_size})...")
            
            tasks = [throttled_crawl(url, crawler) for url in chunk]
            batch_results = await asyncio.gather(*tasks)
            
            # Filter out None results and append
            valid_results = [r for r in batch_results if r]
            final_results.extend(valid_results)
            
            # 4. Immediate Disk Write (Safety Net)
            with open(f"crawl_checkpoint_{i}.json", "w") as f:
                json.dump(valid_results, f)

    return final_results