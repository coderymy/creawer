import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url="https://t66y.com/htm_data/2409/7/6521080.html")

        # Print the extracted content
        print(result.markdown)
        writeContent(result.markdown)

def writeContent(content):
    f = open('content1.md', 'a', encoding='utf-8')
    f.write(content)
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.close()

# Run the async main function


if __name__ == '__main__':
    asyncio.run(main())
