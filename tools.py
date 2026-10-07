import os, re
from crewai.tools import tool

from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key=os.getenv("FIRE_CRAWL_API_KEY"))

@tool
def web_search_tool(query: str):
    """
    Web search tool that uses the Firecrawl API to search the web and return the results.

    Args:
        query: The query to search the web for.

    Returns:
        A list of dictionaries containing the title, url, and markdown of the search results.
    """
    response =firecrawl.search(
        query=query,
        limit=2,
        scrape_options={
            "formats": ["markdown"]
        }
    )
    
    cleaned_chunks = []

    # if not response.success:
    #     return "Error in web search"

    if hasattr(response, 'web'):
        for result in response.web:
            title = getattr(result.metadata,"title","")
            url = getattr(result.metadata,"url","")

            markdown = getattr(result,"markdown", "")
            cleaned = re.sub(r'\\+|\n+',"",markdown).strip()
            cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

            cleaned_result = {
                "title": title,
                "url": url,
                "markdown": cleaned
            }

            cleaned_chunks.append(cleaned_result)
    return cleaned_chunks
       


    
    

    

