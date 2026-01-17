# sitemap.py
from usp.tree import sitemap_tree_for_homepage

def fetch_sitemap_urls(domain: str) -> list[str]:
    """
    Input: https://example.com
    Output: List of all sitemap URLs discovered
    """
    tree = sitemap_tree_for_homepage(domain)

    urls = []
    for page in tree.all_pages():
        urls.append(page.url)

    print(len(urls))
    return urls
