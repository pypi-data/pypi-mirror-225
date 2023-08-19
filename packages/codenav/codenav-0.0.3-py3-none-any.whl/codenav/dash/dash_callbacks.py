# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""

# from psutil import pid_exists

from os import path, access, W_OK, getcwd
from typing import Union
from textwrap import wrap
from subprocess import Popen
from datetime import datetime
import psutil
from dash import ctx, html, ALL
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from snipsearch import search_all_pyfiles
from . import dash_sweet_components as sweet
from .file_system_node import create_fs_nodes
from .dash_trees import file_sys_tree
from .shell_server import get_from_queue


# CONSTANTS
scriptdir = path.split(path.realpath(__file__))[0]
QUEUE_NAME = "dash_testing"
ACTIVATE_CMD = "C:/ProgramData/Anaconda3/Scripts/activate.bat && conda activate py39"
SHELL_SERVER_PATH = path.join(scriptdir, "shell_server.py")
SERVER_CMD = f'{ACTIVATE_CMD} && python "{SHELL_SERVER_PATH}" "{QUEUE_NAME}" "'
READY_STR = "#%# Command Window Ready #%#"
# PORT = 1000

SCROLLDOWN = """
    function(prismchildren) {
        botright = document.getElementById('botright')
        if (typeof botright === "undefined") {
            return "placeholder"
        }
        child1 = botright.children[0];
        if (typeof child1 === "undefined") {
            return "placeholder"
        }
        child2 = child1.children[1];
        if (typeof child2 === "undefined") {
            return "placeholder"
        }
        viewport = child2.children[1];
        if (typeof viewport === "undefined") {
            return "placeholder"
        }
        viewport.scrollTo({top:viewport.scrollHeight, behavior: 'smooth'});
        return "placeholder"
    }
    """


# Callbacks below
def dirpath_up(app, dirpath_id: str, upbutton_id: str, valname: str):
    """
    dirpath_up
    """
    outputs = _puts("d", dirpath_id, [valname])
    inputs = _puts("i", upbutton_id, ["n_clicks"])
    states = _puts("s", dirpath_id, [valname])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)  #
    def up_dirpath(_nclicks, dirpath):
        """up_dirpath.

        Parameters
        ----------
        _nclicks :
            _nclicks
        dirpath :
            dirpath
        """
        _none_check(_nclicks)
        _none_zerolen_check(dirpath)
        return [path.dirname(dirpath.rstrip("/").rstrip("\\"))]


def dirpath_store(app, storepath_id: str, dirpath_id: str):
    """
    dirpath_update
    """
    outputs = _puts("o", [dirpath_id, storepath_id], ["value", "data"])
    inputs = _puts("i", dirpath_id, ["value"])
    states = _puts("s", storepath_id, ["data"])

    @app.callback(outputs, inputs, states)  #
    def update_dirpath(dirpath, storepath):
        """update_dirpath.

        Parameters
        ----------
        dirpath :
            dirpath
        storepath :
            storepath
        """
        # print(f"\ndirpath: {dirpath}\nstorepath: {storepath}")
        if dirpath is not None:
            if path.isdir(dirpath):
                return dirpath, dirpath
            raise PreventUpdate
        if _not_none_haslen(storepath):
            return storepath, storepath
        return getcwd(), getcwd()


def tree_create(app, tree_loader_id: str, dirpath_id: str, tree_id: str):
    """
    create_tree
    """
    outputs = _puts("o", [tree_loader_id, dirpath_id], ["children", "status"])
    inputs = _puts("i", dirpath_id, ["value"])

    @app.callback(outputs, inputs)  # , prevent_initial_call=True
    def create_tree(dirpath):
        """create_tree.

        Parameters
        ----------
        dirpath :
            dirpath
        """
        _none_check(dirpath)
        if not path.isdir(dirpath):
            return sweet.dark_text("Directory Does Not Exist"), "error"
        nodes = create_fs_nodes(dirpath, ext=[".py"])
        tree = file_sys_tree(nodes, tree_id, persistence=True, selectedKeys=[])
        return tree, None


def tree_expand(app, tree_id: str):
    """
    tree_expand
    """
    outputs = _puts("o", tree_id, ["expandedKeys", "selectedKeys"])
    inputs = _puts("i", tree_id, ["selectedKeys"])
    states = _puts("s", tree_id, ["expandedKeys", "treeData"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def expand_tree(selected, expanded, treedata):
        """expand_tree.

        Parameters
        ----------
        selected :
            selected
        expanded :
            expanded
        treedata :
            treedata
        """
        selectdata = _selectdata_check(selected, treedata)
        if selectdata["type"] == "file":
            raise PreventUpdate
        if not expanded:
            expanded = [selectdata["key"]]
            return expanded, []
        if selectdata["key"] in expanded:
            expanded.remove(selectdata["key"])
        else:
            expanded.append(selectdata["key"])
        return expanded, []


def tab_store(app, tabs_id: str, storetabs_id: str):
    """
    tree_open_file
    """
    output1 = _puts("o", tabs_id, ["items", "activeKey"])
    output2 = _puts("o", storetabs_id, ["data"])
    inputs = _puts("i", [storetabs_id, tabs_id], ["data", "activeKey"])
    states = _puts("s", tabs_id, ["items"])

    @app.callback(output1, output2, inputs, states)
    def store_tab(storetabs, activekey, tabitems):
        """store_tab.

        Parameters
        ----------
        storetabs :
            storetabs
        activekey :
            activekey
        tabitems :
            tabitems
        """
        _none_check(storetabs)
        if activekey and ctx.triggered_id == tabs_id:
            storetabs["_active"] = activekey
        if ctx.triggered_id == storetabs_id:
            tabitems, activekey = _tabitems_from_dict(storetabs, tabitems)
        return tabitems, activekey, storetabs


def tree_open_file(app, storetabs_id: str, tree_id: str):
    """
    tree_open_file
    """
    outputs = _puts("d", [storetabs_id, tree_id], ["data", "selectedKeys"])
    inputs = _puts("i", tree_id, ["selectedKeys"])
    states = _puts("s", [tree_id, storetabs_id], ["treeData", "data"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def open_file(selected, treedata, storetabs):
        """open_file.

        Parameters
        ----------
        selected :
            selected
        treedata :
            treedata
        storetabs :
            storetabs
        """
        selectdata = _selectdata_check(selected, treedata)
        if not selectdata["type"] == "file":
            raise PreventUpdate
        filepath = selectdata["value"]
        _filedir, filename = path.split(filepath)
        storetabs = _storetabs_append(
            storetabs, filepath, None, filename, ctype="prism"
        )
        # print("\n" + storetabs["_active"] + "\n" + str(storetabs))
        return storetabs, None


def tab_new(app, storetabs_id: str, newtab_id: str):
    """
    tab_new
    """
    outputs = _puts("d", storetabs_id, ["data"])
    inputs = _puts("i", newtab_id, ["n_clicks"])
    states = _puts("s", storetabs_id, ["data"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def new_tab(_nclicks, storetabs):
        """new_tab.

        Parameters
        ----------
        _nclicks :
            _nclicks
        storetabs :
            storetabs
        """
        storetabs = _storetabs_append(
            storetabs, None, "# New Tab Contents\n\n", "New Tab", ctype="ace"
        )
        return [storetabs]


def tab_delete(app, tabs_id: str, storetabs_id: str):
    """
    tab_delete
    """
    outputs = _puts("d", storetabs_id, ["data"])
    inputs = _puts("i", tabs_id, ["latestDeletePane"])
    state1 = _puts("s", tabs_id, ["items", "activeKey"])
    state2 = _puts("s", storetabs_id, ["data"])

    @app.callback(outputs, inputs, state1, state2, prevent_initial_call=True)
    def delete_tab(delkey, tabitems, activekey, storetabs):
        """delete_tab.

        Parameters
        ----------
        delkey :
            delkey
        tabitems :
            tabitems
        activekey :
            activekey
        storetabs :
            storetabs
        """
        _none_check(delkey)
        ind = [i for i, item in enumerate(tabitems) if item["key"] == delkey]
        tabitems = [item for item in tabitems if item["key"] != delkey]
        _deleted = storetabs.pop(delkey)
        if activekey != delkey:
            return [storetabs]
        if not _not_none_haslen(tabitems):
            activekey = "0"
        elif ind[0] == 0:
            activekey = tabitems[0]["key"]
        else:
            activekey = tabitems[ind[0] - 1]["key"]
        storetabs["_active"] = activekey
        return [storetabs]


def tab_edit(app, storetabs_id: str, edittab_id: str):
    """
    tab_edit
    """
    outputs = _puts("d", storetabs_id, ["data"])
    inputs = _puts("i", edittab_id, ["n_clicks"])
    states = _puts("s", storetabs_id, ["data"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def edit_tab(_nclicks, storetabs):
        """edit_tab.

        Parameters
        ----------
        _nclicks :
            _nclicks
        storetabs :
            storetabs
        """
        _none_check(storetabs)
        activekey = storetabs["_active"]
        if activekey not in storetabs:
            raise PreventUpdate
        _none_check(storetabs[activekey]["path"])
        if storetabs[activekey]["type"] == "ace":
            raise PreventUpdate
        # filepath = storetabs[activekey]["path"]
        # if not access(filepath, W_OK):
        #    raise PreventUpdate
        storetabs[activekey]["type"] = "ace"
        return [storetabs]


def tab_save(app, storetabs_id: str, savetab_id: str, notify_id: str):
    """
    tab_save
    """
    outputs = _puts(["o", "d"], [notify_id, storetabs_id], ["children", "data"])
    inputs = _puts("i", savetab_id, ["n_clicks"])
    states1 = _puts("s", [storetabs_id], ["data"])
    tabinput_id = {"type": "tabinput", "index": ALL}
    tabace_id = {"type": "tabace", "index": ALL}
    states2 = _puts("s", tabinput_id, ["value", "id"])
    states3 = _puts("s", tabace_id, ["value", "id"])

    @app.callback(outputs, inputs, states1, states2, states3, prevent_initial_call=True)
    def save_tab(_nclicks, storetabs, tabpaths, pathids, tabaces, aceids):
        """save_tab.

        Parameters
        ----------
        _nclicks :
            _nclicks
        storetabs :
            storetabs
        tabpaths :
            tabpaths
        pathids :
            pathids
        tabaces :
            tabaces
        aceids :
            aceids
        """
        _none_check(storetabs)
        activekey = storetabs["_active"]
        if activekey not in storetabs:
            raise PreventUpdate
        if storetabs[activekey]["type"] != "ace":
            message = "You must edit the file before saving"
            notify_error = sweet.notify("Save Error", message, "carbon:unsaved", "red")
            return notify_error, storetabs
        savepath = tabpaths[
            [i for i, id in enumerate(pathids) if id["index"] == activekey][0]
        ]
        savetext = tabaces[
            [i for i, id in enumerate(aceids) if id["index"] == activekey][0]
        ]
        _none_check(savepath)
        savedir, savename = path.split(savepath)
        message = None
        if not path.exists(savedir):
            message = "Directory does not exist"
        elif not access(savedir, W_OK):
            message = "You do not have write access to this directory"
        elif path.exists(savepath) and not access(savepath, W_OK):
            message = "You do not have write access to this file"
        if message:
            notify_error = sweet.notify("Save Error", message, "carbon:unsaved", "red")
            return notify_error, storetabs
        storetabs[activekey]["type"] = "prism"
        with open(savepath, "w", encoding="utf-8") as savefile:
            savefile.write(savetext)
        storetabs[activekey]["name"] = savename
        storetabs[activekey]["path"] = savepath
        storetabs[activekey]["text"] = None
        notify = sweet.notify(
            "Saved Successfully", savename, "mingcute:save-line", "green"
        )
        return notify, storetabs


def button_start_cmd(
    app,
    command: str,
    stdstore_id: str,
    storeval_id: str,
    state_fxn,
    button_id: str,
    button_icon,
    button_property: str,
    first: bool = False,
):
    """
    button_start_cmd
    """
    outputs = _puts("d", stdstore_id, ["data"])
    if first:
        outputs = _puts("o", stdstore_id, ["data"])
    inputs = _puts("i", button_id, ["n_clicks"])
    states = _puts("s", [stdstore_id, storeval_id], ["data", "data"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def start_command(_nclicks, stdstore, storeval):
        """start_command.

        Parameters
        ----------
        _nclicks :
            _nclicks
        stdstore :
            stdstore
        storeval :
            storeval
        """
        _none_check(storeval)
        _none_check(_nclicks)
        _none_check(stdstore)
        text_in = stdstore["text"]
        now = datetime.now()
        nowstr = now.strftime("%d-%m-%y %H:%M:%S")
        if READY_STR in text_in:
            scriptpath = state_fxn(storeval)
            runcmd = SERVER_CMD + command + '""' + scriptpath + '"""'
            parent_proc = Popen(runcmd)  # , shell=True
            runtext = "\n".join(wrap(runcmd, 150))
            text_out = (
                f"\n#%# PROCESS ID: {parent_proc.pid} #%#"
                + f'\n>> [{nowstr}] Running Command:\n    {runtext}\n""" "\n'
            )
            stdstore["text"] = text_out
            stdstore["stop"] = button_id
            stdstore["proc_id"] = parent_proc.pid
            return [stdstore]
        server_proc_id = int(stdstore["proc_id"])
        curbutton_id = stdstore["stop"]
        if curbutton_id != button_id:
            raise PreventUpdate
        if psutil.pid_exists(server_proc_id):
            _n1, _s1 = get_from_queue(server_proc_id, QUEUE_NAME, stop="user stop")
            print(f"status: {_s1}\nnewlines: {_n1}\n")
            stopstr = f"\n#%# [{nowstr}] Process Stopped #%#\n{READY_STR}\n"
        else:
            # stopstr = f"{READY_STR}\n"
            raise PreventUpdate
        stdstore["text"] = text_in + stopstr
        stdstore["stop"] = None
        return [stdstore]

    stop_icon = sweet.iconify("fe:stop", "red")
    outputs = _puts("o", button_id, [button_property])
    inputs = _puts("i", stdstore_id, ["data"])
    states = _puts("s", storeval_id, ["data"])

    @app.callback(outputs, inputs, states)
    def stop_button(stdstore, storeval):
        """stop_button.

        Parameters
        ----------
        stdstore :
            stdstore
        storeval :
            storeval
        """
        _none_check(storeval)
        _none_check(stdstore)
        text_in = stdstore["text"]
        curbutton_id = stdstore["stop"]
        if READY_STR in text_in:
            return [button_icon]
        if curbutton_id != button_id:
            raise PreventUpdate
        return [stop_icon]


def stdstore_update(app, stdstore_id: str, interval_id: str):
    """
    stdout_update
    """
    outputs = _puts("d", [stdstore_id], ["data"])
    inputs = _puts("i", [interval_id], ["n_intervals"])
    states = _puts("s", [stdstore_id], ["data"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def update_stdstore(_intervals, stdstore):
        """update_stdstore.

        Parameters
        ----------
        _intervals :
            _intervals
        stdstore :
            stdstore
        """
        if not stdstore:
            stdstore = {"proc_id": None, "stop": None}
            stdstore["text"] = f"{READY_STR}\n"
            return [stdstore]
        text_in = stdstore["text"]
        server_proc_id = stdstore["proc_id"]
        _none_check(server_proc_id)
        try:
            newlines, status = get_from_queue(int(server_proc_id), QUEUE_NAME)
        except ConnectionResetError as err:
            newlines = [str(err)]
        if (not psutil.pid_exists(server_proc_id)) and (READY_STR not in text_in):
            now = datetime.now()
            nowstr = now.strftime("%d-%m-%y %H:%M:%S")
            donestr = f"\n#%# [{nowstr}] Process Complete #%#\n{READY_STR}\n"
            stdstore["text"] = text_in + donestr
            return [stdstore]
        if not newlines:
            raise PreventUpdate
        if not status and len(newlines) > 0:
            print(f"status: {status}    newlines: {newlines}")
            _n1, _s1 = get_from_queue(
                int(server_proc_id), QUEUE_NAME, stop="completion"
            )
            print(f"status: {_s1}\nnewlines: {_n1}\n")
            raise PreventUpdate
        if len("".join(newlines)) == 0:
            raise PreventUpdate
        text_out = text_in + "".join(newlines)
        stdstore["text"] = text_out
        return [stdstore]


def stdout_update(app, stdstore_id: str, stdout_id: str):
    """
    stdout_store
    """
    outputs = _puts("o", [stdout_id], ["children"])
    inputs = _puts("i", [stdstore_id], ["data"])

    @app.callback(outputs, inputs)
    def update_stdout(stdstore):
        """update_stdout.

        Parameters
        ----------
        stdstore :
            stdstore
        """
        _none_check(stdstore)
        storetext = stdstore["text"]
        return [storetext]


def show_hide_search(app, search_id: str, result_id: str):
    """
    show_hide_search
    """
    outputs = _puts("o", ["middle", result_id], ["style", "style"])
    inputs = _puts("i", [search_id], ["value"])

    @app.callback(outputs, inputs)
    def showhidesearch(search):
        """showhidesearch.

        Parameters
        ----------
        search :
            search
        """
        if not search:
            width = "0vw"
            minwidth = "0"
        else:
            width = "12vw"
            minwidth = "5vw"
        style = {
            "height": "100vh",
            "width": width,
            "minWidth": minwidth,
            "display": "inline-block",
            "overflow": "auto",
            "resize": "horizontal",
            "background": "#181818",
            "border": "1px solid #5C5F66",
        }
        return style, {"display": "none"}


def run_search(app, search_id: str, loader_id: str, storepath_id: str, result_id: str):
    """
    show_hide_search
    """
    outputs = _puts("o", loader_id, ["children"])
    inputs = _puts("i", "middle", ["style"])
    states = _puts("s", [storepath_id, search_id], ["data", "value"])

    @app.callback(outputs, inputs, states)
    def runsearch(_style, searchdir, searchval):
        """runsearch.

        Parameters
        ----------
        _style :
            _style
        searchdir :
            searchdir
        searchval :
            searchval
        """
        _none_check(searchval)
        _none_check(searchdir)
        if not path.exists(searchdir):
            raise PreventUpdate
        results = search_all_pyfiles(searchdir, searchval)
        if len(results) > 10:
            results = results[0:10]
        # Parse the results myself and turn into Divs with text and 2 buttons each
        # resultstr = crs.get_result_str(results, number=10)
        # resultcode = [codetext(resultstr, "searchtext")]
        # return resultcode
        alldivs = sweet.create_search_results(results)
        return [html.Div(alldivs, id=result_id)]


def open_search(app, storetabs_id: str):
    """
    tab_edit
    """
    filebutton_ids = {"type": "filebutton", "index": ALL}
    respath_ids = {"type": "respath", "index": ALL}
    outputs = _puts(["d"], storetabs_id, ["data"])
    inputs = _puts("i", filebutton_ids, ["n_clicks"])
    states = _puts("s", [storetabs_id, respath_ids], ["data", "children"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def opensearchfile(_nclicks, storetabs, respaths):
        """opensearchfile.

        Parameters
        ----------
        _nclicks :
            _nclicks
        storetabs :
            storetabs
        respaths :
            respaths
        """
        if not any(_nclicks):
            raise PreventUpdate
        # print(f"\n{_nclicks}\n{ctx.triggered_prop_ids}")
        ind = int(ctx.triggered_id["index"]) - 1
        respath = respaths[ind]
        _filedir, filename = path.split(respath)
        storetabs = _storetabs_append(storetabs, respath, None, filename, ctype="prism")
        return [storetabs]

    snipbutton_id = {"type": "snipbutton", "index": ALL}
    restext_id = {"type": "restext", "index": ALL}
    outputs = _puts(["d"], storetabs_id, ["data"])
    inputs = _puts("i", snipbutton_id, ["n_clicks"])
    states = _puts("s", [storetabs_id, restext_id], ["data", "children"])

    @app.callback(outputs, inputs, states, prevent_initial_call=True)
    def opensearchsnip(_nclicks, storetabs, restexts):
        """opensearchsnip.

        Parameters
        ----------
        _nclicks :
            _nclicks
        storetabs :
            storetabs
        restexts :
            restexts
        """
        if not any(_nclicks):
            raise PreventUpdate
        ind = int(ctx.triggered_id["index"]) - 1
        restext = restexts[ind]
        storetabs = _storetabs_append(
            storetabs, None, restext, "Snip #" + str(ind + 1), ctype="prism"
        )
        return [storetabs]


# Pre Checks Below
def _selectdata_check(selected, treedata):
    """_selectdata_check.

    Parameters
    ----------
    selected :
        selected
    treedata :
        treedata
    """
    if not selected:
        raise PreventUpdate
    selectdata = [data for data in treedata if data["key"] == selected[0]]
    if len(selectdata) == 0:
        raise PreventUpdate
    return selectdata[0]


def _none_check(value):
    """_none_check.

    Parameters
    ----------
    value :
        value
    """
    if not value:
        raise PreventUpdate


def _not_none_haslen(value):
    """_not_none_haslen.

    Parameters
    ----------
    value :
        value
    """
    if not value:
        return False
    if len(value) == 0:
        return False
    return True


def _none_zerolen_check(value):
    """_none_zerolen_check.

    Parameters
    ----------
    value :
        value
    """
    if not value:
        raise PreventUpdate
    if len(value) == 0:
        raise PreventUpdate


# Helpers Below
def read_storetabs_file(storetabs):
    """
    read_storetabs_file
    """
    activekey = storetabs["_active"]
    if activekey not in storetabs:
        raise PreventUpdate
    if not storetabs[activekey]["path"]:
        raise PreventUpdate
    return storetabs[activekey]["path"]


def read_storepath(storepath):
    """
    read_storepath
    """
    return storepath


def _puts(
    ptypes: Union[list[str], str], call_ids: Union[list[str], str], names: list[str]
):
    """_puts.

    Parameters
    ----------
    ptypes : Union[list[str], str]
        ptypes
    call_ids : Union[list[str], str]
        call_ids
    names : list[str]
        names
    """
    if not isinstance(call_ids, list):
        call_ids = [call_ids] * len(names)
    if not isinstance(ptypes, list):
        ptypes = [ptypes] * len(names)
    outlist = []
    for i, ptype in enumerate(ptypes):
        if ptype == "o":
            outlist.append(Output(call_ids[i], names[i]))
        elif ptype == "d":
            outlist.append(Output(call_ids[i], names[i], allow_duplicate=True))
        elif ptype == "i":
            outlist.append(Input(call_ids[i], names[i]))
        elif ptype == "s":
            outlist.append(State(call_ids[i], names[i]))
        else:
            raise TypeError(f"!! ptype '{ptype}' is not support by 'puts' function !!")
    return outlist


def _tabdict(children, label: str, key: str) -> dict:
    """_tabdict.

    Parameters
    ----------
    children :
        children
    label : str
        label
    key : str
        key

    Returns
    -------
    dict

    """
    return {"label": label, "key": key, "children": children, "closable": True}


def _storetabs_append(storetabs, itempath: str, text: str, name: str, ctype="prism"):
    """_storetabs_append.

    Parameters
    ----------
    storetabs :
        storetabs
    itempath : str
        itempath
    text : str
        text
    name : str
        name
    ctype :
        ctype
    """
    if not storetabs:
        storetabs = {}
    storekeys = [key for key in storetabs.keys() if key.isdigit()]
    if len(storekeys) == 0:
        curkey = "0"
    else:
        curkey = str(int(storekeys[-1]) + 1)
    storetabs["_active"] = curkey
    storetabs[curkey] = {}
    storetabs[curkey]["path"] = itempath
    if itempath:
        if not access(itempath, W_OK):
            name = name + " (Read Only)"
    storetabs[curkey]["name"] = name
    storetabs[curkey]["text"] = text
    storetabs[curkey]["key"] = curkey
    storetabs[curkey]["type"] = ctype
    # print(f"\nactivekey in append: {curkey}")
    return storetabs


def _tabitems_from_dict(storetabs: dict, tabitems: list):
    """_tabitems_from_dict.

    Parameters
    ----------
    storetabs : dict
        storetabs
    tabitems : list
        tabitems
    """
    storetabs_cp = dict(storetabs)
    if not tabitems:
        tabitems = []
    new_tabitems = []
    new_keys = []
    curkey = storetabs_cp.pop("_active")
    for tabitem in tabitems:
        if not tabitem["key"] in storetabs_cp.keys():
            continue
        if tabitem["key"] == curkey:
            storeitem = storetabs_cp[curkey]
            tabdiv = _make_tabdiv(storeitem)
            new_tabitems.append(_tabdict(tabdiv, storeitem["name"], storeitem["key"]))
        else:
            new_tabitems.append(tabitem)
        new_keys.append(tabitem["key"])
    new_storekeys = [key for key in storetabs_cp.keys() if key not in new_keys]
    for storekey in new_storekeys:
        storeitem = storetabs_cp[storekey]
        tabdiv = _make_tabdiv(storeitem)
        new_tabitems.append(_tabdict(tabdiv, storeitem["name"], storeitem["key"]))
    return new_tabitems, curkey


def _make_tabdiv(storeitem: dict):
    """_make_tabdiv.

    Parameters
    ----------
    storeitem : dict
        storeitem
    """
    isfile = False
    text = storeitem["text"]
    header_id = {"type": "tabinput", "index": storeitem["key"]}
    headerdiv = sweet.ant_input("🗎 File Path", id=header_id)
    if storeitem["path"]:
        isfile = True
        text = storeitem["path"]
        headerdiv = sweet.ant_input(
            "🗎 File Path", id=header_id, value=storeitem["path"]
        )
    if storeitem["type"] == "edit":
        codediv = sweet.pyeditor(text, isfile=isfile)
    elif storeitem["type"] == "ace":
        ace_id = {"type": "tabace", "index": storeitem["key"]}
        codediv = sweet.ace_pyeditor(text, isfile=isfile, id=ace_id)
    else:
        codediv = sweet.pyprism(text, isfile=isfile)
    tabdiv = sweet.add_header_div(headerdiv, codediv)
    return tabdiv
