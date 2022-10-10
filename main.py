import argparse
from link_checker import LinkChecker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web crawling')
    parser.add_argument('--page', type=str, required=True, help='Website link')
    parser.add_argument('--format', type=str, required=True, choices=['CSV', 'JSON'], help='Select CSV or JSON format')
    parser.add_argument('--output', type=str, required=True, help='Path to file')
    args = parser.parse_args()

    # scrapper = Scrapper(args.page, args.format, args.output)
    # scrapper.start_crawl()

    scrapper = LinkChecker(args.format, args.output)
    scrapper.check_link(args.page)
