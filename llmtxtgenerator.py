# Import necessary libraries
import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import re
import unicodedata
import html
import requests
import json

# Function to crawl a sitemap and extract URLs
async def crawl_sitemap(crawler, sitemap_url, level=0):
    print("Step 1: Starting to crawl sitemap:", sitemap_url)  # Log step
    try:
        result = await crawler.arun(sitemap_url)  # Crawl the sitemap
        print("Step 2: Crawled sitemap successfully.")  # Log step
        if not result.markdown:  # Check if markdown is present
            print("Step 3: No markdown found in result.")  # Log step
            return []
        
        all_results = []  # Initialize list to store results
        # Extract URLs from the sitemap
        urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', result.markdown, re.DOTALL)
        table_urls = re.findall(r'<(https?://[^>]+)>', result.markdown)
        urls.extend(table_urls)  # Combine extracted URLs
        
        xml_urls = []  # List for XML URLs
        page_urls = []  # List for page URLs
        
        # Classify URLs into XML and page URLs
        for url in urls:
            if url.lower().endswith('.xml'):
                xml_urls.append(url)  # Add to XML URLs
            else:
                page_urls.append(url)  # Add to page URLs
        
        # Add current sitemap's direct page URLs
        if page_urls:
            all_results.append({
                'source': sitemap_url,
                'urls': page_urls
            })
        
        # Recursively process nested sitemaps
        for xml_url in xml_urls:
            nested_results = await crawl_sitemap(crawler, xml_url, level + 1)
            all_results.extend(nested_results)  # Combine nested results
        
        print("Step 4: Finished processing sitemap:", sitemap_url)  # Log step
        return all_results  # Return all results
    except Exception as e:
        print(f"Error crawling {sitemap_url}: {str(e)}")
        return []

# Function to clean text by removing HTML and unwanted elements
def clean_text(text):
    # Convert HTML entities
    text = html.unescape(text)
    
    # Remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    
    # Remove all links
    for link in soup.find_all('a'):
        link.decompose()
    
    text = soup.get_text()  # Get text without HTML tags
    
    # Remove URLs that might be in plain text
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Basic cleaning
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single
    text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with single
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
    text = text = unicodedata.normalize('NFKD', text)  # Normalize unicode
    
    # Remove common web elements
    text = re.sub(r'cookie[s]?\spolicy', '', text, flags=re.IGNORECASE)
    text = re.sub(r'privacy\spolicy', '', text, flags=re.IGNORECASE)
    text = re.sub(r'terms\sof\sservice', '', text, flags=re.IGNORECASE)
    
    return text.strip()  # Return cleaned text

# Function to get AI-generated summary for a given URL and text
async def get_ai_summary(url, text):
    try:
        # Get API key from user input (stored temporarily for the session)
        api_key = getattr(get_ai_summary, 'api_key', None)
        if not api_key:
            api_key = input("Enter your OpenRouter API key (get it from openrouter.ai): ")
            get_ai_summary.api_key = api_key  # Store for subsequent calls

        # Send a POST request to the AI API
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "qwen/qwen-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI that creates webpage summaries in a specific link format. Provide a concise title of 4 to 5 words that accurately conveys the main context and purpose of the webpage."
                    },
                    {
                        "role": "user",
                        "content": f"""Create a single-sentence webpage summary in this exact format:
[Title] ({url}): A concise sentence that captures the essence of the page.

Input content:
{text}"""
                    }
                ],
            })
        )

        # Log the response content for debugging
        print(f"Response for {url}: {response.text}")

        if response.status_code == 200:  # Check if the request was successful
            response_json = response.json()
            if 'choices' in response_json:
                return response_json['choices'][0]['message']['content']  # Return the summary
            else:
                # Log the error message if 'choices' is not present
                error_message = response_json.get('error', {}).get('message', 'Unknown error')
                error_code = response_json.get('error', {}).get('code', 'Unknown code')
                return f"Error processing {url}: {error_code} - {error_message}"
        else:
            return f"Error processing {url}: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error processing {url}: {str(e)}"

# Function to process a URL and generate a summary
async def process_url(crawler, url):
    print(f"Step 5: Processing URL: {url}")  # Log step
    try:
        result = await crawler.arun(url)  # Crawl the URL
        print("Step 6: URL processed successfully.")  # Log step
        cleaned_text = clean_text(result.markdown)  # Clean the text
        print("Step 7: Cleaned text from URL.")  # Log step
        
        # Print the URL and the cleaned text
        print(f"Web Link: {url}")  # Print the URL
        print("Text Content:")
        print(cleaned_text)  # Print the cleaned text
        
        summary = await get_ai_summary(url, cleaned_text)  # Get the summary
        print("Step 8: Summary generated for URL.")  # Log step
        return summary  # Return the summary
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return f"Error processing {url}: {str(e)}"

# Main function to orchestrate the crawling and summarization process
async def main():
    print("Step 9: Starting main function.")  # Log step
    async with AsyncWebCrawler(verbose=False) as crawler:
        website = input("Enter website URL: ")  # Get website URL from user
        if not website.startswith(('http://', 'https://')):
            website = f'https://{website}'  # Ensure URL starts with http(s)
        
        # Try common sitemap paths
        sitemap_paths = [
            f"{website}/sitemap.xml",
            f"{website}/sitemap_index.xml",
            f"{website}/sitemap-index.xml",
            f"{website}/sitemaps.xml"
        ]
        
        found_sitemap = False  # Flag to check if sitemap is found
        for sitemap_url in sitemap_paths:
            try:
                print(f"Step 10: Trying sitemap URL: {sitemap_url}")  # Log step
                result = await crawler.arun(sitemap_url)  # Crawl the sitemap URL
                if result.markdown:  # Check if markdown is present
                    print(f"Step 11: Found sitemap at: {sitemap_url}")  # Log step
                    
                    # Print plain text first
                    print("\nSitemap Content:")
                    print(result.markdown)
                    
                    # Get all URLs recursively
                    results = await crawl_sitemap(crawler, sitemap_url)
                    
                    if results:
                        all_summaries = []  # List to store all summaries
                        
                        # Process each URL and get summary
                        for result_group in results:
                            print("\n" + "="*80)
                            print(f"Processing source: {result_group['source']}")
                            print("="*80 + "\n")
                            
                            for url in result_group['urls']:
                                print(f"Step 12: Processing URL from sitemap: {url}")  # Log step
                                summary = await process_url(crawler, url)  # Process the URL
                                all_summaries.append(summary)  # Add summary to list
                        
                        # Print all summaries
                        print("\n\n" + "="*80)
                        print(f"LLMS.txt Page for {website}")  # Stylish header
                        print("="*80 + "\n")
                        print("Links can be found below:\n")  # Message about links
                        
                        for summary in all_summaries:
                            print(summary)  # Print each summary
                            print()  # Add a line space between links
                        print("-"*40)
                    
                    found_sitemap = True  # Set flag to true if sitemap is found
                    break
            except Exception as e:
                print(f"Error with sitemap {sitemap_url}: {str(e)}")
                continue
        
        if not found_sitemap:
            print("No sitemap found. Please check the website URL or try a different website.")
            return

        # Format the final output
        output = []
        output.append("="*80)
        output.append(f"LLMS.txt Page for {website}")
        output.append("="*80 + "\n")
        output.append("Links can be found below:\n")

        for summary in all_summaries:
            output.append(summary)
            output.append("")  # Empty line between summaries
        
        output.append("-"*40)
        
        # Join all lines with newlines
        final_output = "\n".join(output)
        
        # Print to terminal
        print("\n" + final_output)
        
        # Save to file
        with open("llms.txt", "w", encoding="utf-8") as f:
            f.write(final_output)
        
        print("\nOutput has been saved to llms.txt")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())  # Run the main function 