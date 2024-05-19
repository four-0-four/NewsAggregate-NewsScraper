import argparse
import asyncio

from main import parallel_main, parallel_one_news_source, scrape_article_given_url, scrape_urls_one_category_given_news_source


def main():
    parser = argparse.ArgumentParser(description="Run scraping functions with provided arguments.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("parallel_main", help="Run the parallel main function to scrape all sources.")

    parser_one_news = subparsers.add_parser("parallel_one_news_source", help="Scrape a single news source.")
    parser_one_news.add_argument("newsSource", help="The news source to scrape.")

    parser_one_category = subparsers.add_parser("scrape_urls_one_category_given_news_source", help="Scrape URLs of one category given a news source.")
    parser_one_category.add_argument("newsSource", help="The news source to scrape.")

    parser_article_url = subparsers.add_parser("scrape_article_given_url", help="Scrape an article given its URL.")
    parser_article_url.add_argument("newsSource", help="The news source of the article.")
    parser_article_url.add_argument("articleURL", help="The URL of the article to scrape.")

    args = parser.parse_args()

    if args.command == "parallel_main":
        asyncio.run(parallel_main())
    elif args.command == "parallel_one_news_source":
        asyncio.run(parallel_one_news_source(args.newsSource))
    elif args.command == "scrape_urls_one_category_given_news_source":
        scrape_urls_one_category_given_news_source(args.newsSource)
    elif args.command == "scrape_article_given_url":
        asyncio.run(scrape_article_given_url(args.newsSource, args.articleURL))

if __name__ == "__main__":
    main()