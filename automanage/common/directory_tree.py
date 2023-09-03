#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import fire
from loguru import logger

from treelib import Tree
from anytree import Node, RenderTree

class DirectoryTree(object):
    """
    A class that represents a directory tree structure
    
    Example:
        python3 directory_tree.py main
        
        # python3 directory_tree.py --root_dir /tmp --save_dir /tmp
    """
    def __init__(self, root_dir = None, save_dir = None, depth = None):
        self.root_dir = root_dir
        self.save_dir = save_dir
        self.depth = depth
        self.root = None
    
    def config_treelib(self, root_dir, save_dir, depth):
        self.root_dir = root_dir
        self.save_dir = save_dir
        self.root = self.create_treelib(self.root_dir, Tree(), None)
        return Tree()
    
    def config_anytree(self, root_dir, save_dir, depth):
        self.root_dir = root_dir
        self.save_dir = save_dir
        self.root = self.create_anytree(self.root_dir, None)
        return Tree()

    def create_anytree(self, path, parent):
        """
        Recursively create a tree structure of the given path using anytree
        """
        name = os.path.basename(path)
        node = Node(name, parent = parent)
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        self.create_anytree(entry.path, node)
        except OSError as e:
            logger.error(f"Error: {e}")
        return node

    def create_depth_anytree(self, depth, path, parent):
        if depth == 0:
            return
        self.create_depth_anytree(depth - 1, path, parent)
        return
    
    def create_treelib(self, path, tree, parent):
        """
        Recursively create a tree structure of the given path using treelib
        """
        name = os.path.basename(path)
        node = tree.create_node(name, parent = parent)
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        self.create_treelib(entry.path, tree, node.identifier)
        except OSError as e:
            logger.error(f"Error: {e}")
        return node

    def print_anytree(self):
        """
        Print the directory structure of the given path using anytree
        """
        for pre, _, node in RenderTree(self.root):
            print(f"{pre}{node.name}")

    def save_anytree(self, filename):
        """
        Save the directory structure of the given path using anytree
        """
        with open(filename, "w") as f:
            for pre, _, node in RenderTree(self.root):
                f.write(f"{pre}{node.name}\n")

    def save_treelib(self, tree, filename):
        """
        Save the directory structure of the given path using treelib
        """
        if os.path.exists(filename):
            os.remove(filename)
        tree.save2file(filename)
    
    def main(self):
        """
        Main function
        """
        root_dir = '..\\'
        save_dir = '..\\data\\'
        tree = self.config_treelib(root_dir, save_dir, None)
        logger.info("Printing directory structure using treelib:")
        tree.show(self.root.identifier)
        logger.info("Saving directory structure using treelib:")
        self.save_treelib(tree, f"{save_dir}treelib.txt")
        logger.info("Finished!")

        # tree = self.config_anytree(root_dir, save_dir, None)
        # logger.info("Printing directory structure using anytree:")
        # self.print_anytree()
        # logger.info("Saving directory structure using anytree:")
        # self.save_anytree(f"{save_dir}anytree.txt")
        # logger.info("Finished!")

if __name__ == "__main__":
    fire.Fire(DirectoryTree)
    