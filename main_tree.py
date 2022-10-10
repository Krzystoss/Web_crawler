import argparse
from tree_printer import Tree
from link_checker import LinkChecker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Links tree')
    parser.add_argument('--page', type=str, required=True, help='Website link')
    args = parser.parse_args()

    line_checker = LinkChecker(file_format=None, output=None)
    urls_dictionary = line_checker.check_link(args.page)
    Tree.build_tree_from_dict(urls_dictionary).print()
