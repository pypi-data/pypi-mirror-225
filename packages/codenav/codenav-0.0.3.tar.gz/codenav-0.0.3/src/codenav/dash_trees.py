# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""

from os import path
import feffery_antd_components as fac

BG_COLOR_1_DARK = "#181818"
BG_COLOR_2_DARK = "#5C5F66"
BG_COLOR_3_DARK = "#373A40"
BG_COLOR_4_DARK = "#25262B"  # darkest one?
BG_COLOR_BLUE_POP = "#094F9C"
FG_COLOR_1_DARK = "white"


def create_tree_list(file_objs: list, parent_icon: str = None, child_icon: str = None):
    """
    create_tree_list

    objects must have name, ftype, ind, path
    """
    treelist = []
    for obj in file_objs:
        objpath = obj.directory + "/" + obj.name
        leafdict = {
            "title": obj.name,
            "key": str(obj.ind),
            "type": obj.ftype,
            "value": objpath,
        }
        if parent_icon and (path.isdir(objpath)):
            leafdict = {
                **leafdict,
                **{"icon": parent_icon},  # , "switcherIcon": "antd-file"
            }
        else:
            leafdict = {
                **leafdict,
                **{"icon": child_icon},
            }
        if obj.parent:
            leafdict = {**leafdict, **{"parent": str(obj.parent.ind)}}
        treelist.append(leafdict)
    return treelist


def create_tree_select_list(file_objs: list):
    """
    create_tree_select_list
    """
    treelist = []
    for obj in file_objs:
        if not obj.parent:
            continue
        if obj.ftype == "file":
            continue
        leafdict = {
            "title": obj.name,
            "value": obj.directory + "/" + obj.name,
            "key": str(obj.ind),
        }
        if obj.parent:
            if obj.parent.parent:
                leafdict = {**leafdict, **{"parent": str(obj.parent.ind)}}
        treelist.append(leafdict)
    return treelist


def tree_list_to_dict(treelist: list):
    """
    tree_list_to_dict
    """
    treedict = [
        {
            **{key: value for key, value in item.items()},
        }
        for item in treelist
    ]
    return treedict


def ant_tree(treelist: list, call_id: str, **kwargs):
    """
    ant_tree
    """
    treedict = tree_list_to_dict(treelist)
    div = fac.AntdTree(
        id=call_id,
        treeData=treedict,
        treeDataMode="flat",
        defaultExpandAll=False,
        showIcon=True,
        showLine=False,
        style={
            "background": BG_COLOR_1_DARK,
            "color": FG_COLOR_1_DARK,  # "#B3B3B3",
            "width": "100%",
            "height": "100%",
            "flex": "1",
        },
        expandedKeys=["0"],
        **kwargs,
    )
    return div


def ant_tree_select(treelist: list, call_id: str, searchpath: str, **kwargs):
    """
    ant_tree
    """
    treedict = tree_list_to_dict(treelist)
    div = fac.AntdTreeSelect(
        id=call_id,
        locale="en-us",
        treeData=treedict,
        treeDataMode="flat",
        placeholder="📁 Folder Path",
        defaultValue=searchpath,
        value=searchpath,
        # persistence_type="session",
        # autoClearSearchValue=False,
        # treeNodeFilterProp="title",
        # status="error",
        style={
            "width": "100%",
            "minWidth": "0",
        },
        **kwargs,
    )
    return div


def file_sys_tree(nodes, tree_id: str, **kwargs):
    """
    file_sys_tree
    """
    treelist = create_tree_list(
        nodes,
        parent_icon="antd-folder",
        child_icon="antd-file",
    )
    treediv = ant_tree(treelist, tree_id, **kwargs)
    return treediv


def file_sys_tree_select(nodes, select_id: str, searchpath: str, **kwargs):
    """
    file_sys_tree
    """
    treeselectlist = create_tree_select_list(nodes)
    treeselectdiv = ant_tree_select(treeselectlist, select_id, searchpath, **kwargs)
    return treeselectdiv
