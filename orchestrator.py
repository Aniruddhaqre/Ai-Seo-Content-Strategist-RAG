from sitemap import fetch_sitemap_urls
from filter import filter_urls, advanced_filter, limit_per_folder
from crawler import crawl_batch
import asyncio
from utils import write_to_csv, write_to_word, write_to_word_clean
from chunker import TrafilaturaChunkingPipeline
from vector_store import upload_to_local_db
import json

# urls = fetch_sitemap_urls("https://theayurvedaco.us/")
# clean_urls = filter_urls(urls)

# urls = advanced_filter(clean_urls)
# urls = limit_per_folder(urls, limit=120)

# print(len(urls))
# print(len(clean_urls))
# print(urls[:10])

# test_urls = ['https://www.clubmahindra.com/blog/experience/celebrate-rann-utsav-with-club-mahindra' , 'https://www.clubmahindra.com/blog/places-to-visit/4-summer-destinations-to-beat-the-heat']

# result = asyncio.run(crawl_batch(
#         urls=clean_urls, 
#         batch_size=50, 
#         max_concurrency=5
#     ))

# for x in result:
#     print(x.keys())

# with open("data.json", "w", encoding="utf-8") as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)


# pipeline = TrafilaturaChunkingPipeline()
# pipeline.process_file("the_ayurvedaco_us_data.json", "the_ayurvedaco_us_data_chunks.json", "Comp1")
# pipeline.process_file("kamaayurveda_data.json", "kamaayurveda_data_chunks.json", "Comp2")
# pipeline.process_file("banyan_botanicals_data.json", "banyan_botanicals_data_chunks.json", "Comp2")

upload_to_local_db("./chunks/banyan_botanicals_data_chunks.json", "Comp3")
upload_to_local_db("./chunks/kamaayurveda_data_chunks.json", "Comp2")
upload_to_local_db("./chunks/the_ayurvedaco_us_data_chunks.json", "Comp1")