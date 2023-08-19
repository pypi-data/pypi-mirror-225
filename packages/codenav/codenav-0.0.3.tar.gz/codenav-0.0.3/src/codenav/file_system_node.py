# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""

from os import listdir, path
from typing import Any


class FileSystemNode:
    """
    FileSystemNode
    """

    def __init__(
        self,
        name: str,
        directory: str,
        parent: "FileSystemNode",
        children: list["FileSystemNode"],
        ftype: str,
        ind: int,
    ):
        """__init__.

        Parameters
        ----------
        name : str
            name
        directory : str
            directory
        parent : "FileSystemNode"
            parent
        children : list["FileSystemNode"]
            children
        ftype : str
            ftype
        ind : int
            ind
        """
        self.name = name
        self.directory = directory.replace("\\", "/")
        self.parent = parent
        self.children = children
        self.ftype = ftype
        self.ind = ind

    def get_all_children(self):
        """
        get_all_children
        """
        childlist = []
        for child in self.children:
            subchildren = child.get_all_children()
            if len(subchildren) > 0:
                childlist.extend(subchildren)
        childlist.extend(self.children)
        return childlist

    def print_children(self):
        """
        print_children
        """
        objlist = self.get_all_children()
        for obj in objlist:
            if isinstance(obj, list):
                obj.print_nested()
            else:
                # Change this later for printparams as args
                print(f"\n{obj.name}\n    {obj.ind}\n    {obj.directory}")
                if obj.parent:
                    print(f"    {obj.parent.name}")
                childnamelist = [child.name for child in obj.children]
                if len(childnamelist) > 0:
                    print(f"    {childnamelist}")


def create_fs_nodes(
    searchpath: str,
    parent: FileSystemNode = None,
    ind: int = 0,
    ext: list[str] = None,
    skip: list[str] = None,
):
    """
    create_fs_nodes
    """
    ext = set_default(ext, [])
    skip = set_default(skip, [".", "_"])
    nodes = []
    searchpath = path.normpath(searchpath)
    basepath, searchname = path.split(searchpath)
    if parent:
        rootnode = FileSystemNode(searchname, basepath, parent, [], "directory", ind)
    else:
        rootnode = FileSystemNode(searchname, basepath, None, [], "root", ind)
    ind += 1
    try:
        listdir(searchpath)
    except PermissionError:
        return [rootnode]
    for item in listdir(searchpath):
        itempath = path.join(searchpath, item)
        if path.isdir(itempath):
            if any(item.startswith(char) for char in skip):
                continue
            dirnodes = create_fs_nodes(
                itempath, parent=rootnode, ind=ind, ext=ext, skip=skip
            )
            dirnodes = [
                node
                for node in dirnodes
                if (node.ftype == "directory" and len(node.children) > 0)
                or (node.ftype == "file")
            ]
            if len(dirnodes) > 0:
                ind += len(dirnodes)
                nodes.extend(dirnodes)
                rootnode.children.append(dirnodes[-1])
        else:
            _none, itemext = path.splitext(item)
            if (len(ext) > 0) and (itemext not in ext):
                continue
            filenode = FileSystemNode(item, searchpath, rootnode, [], "file", ind)
            ind += 1
            nodes.append(filenode)
            rootnode.children.append(filenode)
    nodes.append(rootnode)
    return nodes


def set_default(variable: Any, default: Any):
    """
    set_default
    """
    if not variable:
        return default
    return variable


if __name__ == "__main__":
    SEARCH = R"C:\Users\jkris\OneDrive\2022_onward\2023\optibox"
    onodes = create_fs_nodes(SEARCH, ext=[".py"])
    spnode = onodes[-1]
    import time

    time.sleep(3)
    cnodes = spnode.get_all_children()
    spnode.print_children()
    # for node in cnodes:
    #    print(node.name)
