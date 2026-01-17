import json
import hashlib
import trafilatura
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

class TrafilaturaChunkingPipeline:
    def __init__(self, chunk_size=1200, chunk_overlap=200):
        # 1. Structural Splitter
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "H1"), ("##", "H2"), ("###", "H3")],
            strip_headers=False
        )
        
        # 2. Recursive Fallback
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def extract_main_content(self, markdown_text):
        """
        Uses Trafilatura logic to identify the main body.
        If Trafilatura fails, it returns the original text.
        """
        # Trafilatura's extract function is very good at identifying 'main' text
        # We set include_links=True to keep our internal URLs for the AI
        clean_content = trafilatura.extract(
            markdown_text, 
            include_links=True,
            include_images=False, # We usually want text for chunking
            output_format='markdown'
        )
        
        return clean_content if clean_content else markdown_text

    def generate_page_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def process_file(self, input_path: str, output_path: str, business_label: str):
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_chunks = []

        for item in data:
            url = item.get('url')
            page_id = self.generate_page_id(url)
            
            # --- THE CLEANING STEP ---
            # We take the markdown and let Trafilatura decide what is the 'Body'
            raw_md = item.get('cleaned_markdown', '') # Using the full markdown field
            body_content = self.extract_main_content(raw_md)
            
            # --- CHUNKING ---
            header_splits = self.header_splitter.split_text(body_content)
            docs = self.recursive_splitter.split_documents(header_splits)
            
            for i, doc in enumerate(docs):
                all_chunks.append({
                    "chunk_id": f"{page_id}_{i}",
                    "page_id": page_id,
                    "business_source": business_label,
                    "url": url,
                    "chunk_content": doc.page_content,
                    "metadata": doc.metadata
                })

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=4)
        
        print(f"Finished {business_label}: Generated {len(all_chunks)} clean chunks.")

# Execution
