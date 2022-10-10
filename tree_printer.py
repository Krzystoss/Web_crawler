import pandas as pd

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, node):
        if self.root is None:
            self.root = node
        else:
            self.root.add_node(node)

    def print(self):
        self.root.print(0)

    @staticmethod
    def build_tree_from_dict(urls_dictionary):
        tree = Tree()
        sorted_keys = sorted(list(urls_dictionary.keys()), key=lambda x: x.count("/"))
        for url in sorted_keys:
            tree.add_node(TreeNode(url, urls_dictionary[url]["internal links count"]))
        return tree

    @staticmethod
    def build_tree_from_file(path, format="CSV"):
        df = pd.read_csv(path) if format == "CSV" else pd.read_json(path)
        urls_dictionary = {row[1]['url']: {"internal links count": row[1]['internal links count']} for row in df.iterrows()}
        return Tree.build_tree_from_dict(urls_dictionary)

class TreeNode:

    def __init__(self, url, n_internal_pages):
        self.url = url
        self.n_internal_pages = n_internal_pages
        self.children = []

    def add_node(self, node):
        for child in self.children:
            if node.url.startswith(child.url):
                return child.add_node(node)
        self.children.append(node)

    def print(self, level):
        print("  "*level + f"{self.url} ({self.n_internal_pages})")
        for child in self.children:
            child.print(level+1)

# tree = Tree.build_tree_from_file("crawler-test.com.csv").print() - reading from file