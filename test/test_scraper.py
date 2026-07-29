from scraping.web_scraper import scrape_webpage


url = input("Enter URL to scrape: ")

result = scrape_webpage(url)


if result["success"]:

    print("\nScraping successful!\n")

    print(
        result["text"][:3000]
    )

else:

    print("\nScraping failed.")
    print("Type:", result["type"])
    print("Error:", result["error"])