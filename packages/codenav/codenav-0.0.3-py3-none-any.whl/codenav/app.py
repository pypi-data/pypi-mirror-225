# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris

"""

from os import getcwd
import webbrowser
import socket
from threading import Timer
from waitress import serve
from dash import Dash, html, dcc, clientside_callback
from dash.dependencies import Input, Output
from dash_bootstrap_components import themes
import cleandoc  # pylint: disable=W0611,E0401
from . import dash_sweet_components as sweet
from . import dash_trees as trees
from . import dash_callbacks as call
from .file_system_node import create_fs_nodes


# CONSTANTS
PERSIST = True
TREE_ID = "tree"
TREE_LOADER_ID = "treeloader"
PATH_INPUT_ID = "pathinput"
ENV_CMD_ID = "envcmd"
FILE_TABS_ID = "filetabs"
STORE_PATH_ID = "storepath"
STORE_ITEMS_ID = "storeitems"
STORE_ENV_ID = "storeenv"
STORE_CMD_ID = "storestdout"
NEW_TAB_ID = "newtab"
EDIT_TAB_ID = "edittab"
RUN_TAB_ID = "runtab"
RUN_TAB_CMD = "python "
SAVE_TAB_ID = "savefile"
UP_BUTTON_ID = "updir"
STDOUT_ID = "stdout_text"
INTERVAL_ID = "stdout_int"
CLEAN_FILE_ID = "File"
CLEAN_ALL_ID = "All"
CLEAN_DOC_ID = "Doc"
CLEAN_FILE_CMD = "cleandoc -f "  #  -w
CLEAN_ALL_CMD = "cleandoc -nodoc -d "  #  -w
CLEAN_DOC_CMD = "cleandoc -d "
TAG_SEARCH_ID = "tagsearch"
LOAD_SEARCH_ID = "searchloader"
RESULT_ID = "searchresults"
NOTIFY_ID = "notifydiv"


def codenav_app():
    """
    create the dash app object
    """

    # Stores
    storepath = dcc.Store(id=STORE_PATH_ID, storage_type="session")
    storeitems = dcc.Store(id=STORE_ITEMS_ID, storage_type="session")
    storeenv = dcc.Store(id=STORE_ENV_ID, storage_type="session")
    storecmd = dcc.Store(id=STORE_CMD_ID, storage_type="local")

    # Cleandoc Buttons Group
    cleanfile_icons = ["carbon:clean", "ant-design:file-twotone"]
    fc_button, fc_icons = sweet.icon_button(
        CLEAN_FILE_ID, cleanfile_icons, "Clean Current File"
    )
    cleanall_hint = "Clean All Files in Current Directory"
    cleanall_icons = ["carbon:clean", "ant-design:folder-twotone"]
    ac_button, ac_icons = sweet.icon_button(CLEAN_ALL_ID, cleanall_icons, cleanall_hint)
    cleandoc_hint = "Clean All Files and Create HTML Docs"
    cleandoc_icons = ["carbon:clean", "tabler:file-type-html"]
    cd_button, cd_icons = sweet.icon_button(CLEAN_DOC_ID, cleandoc_icons, cleandoc_hint)
    clean_buttons = sweet.dmc_group([fc_button, ac_button, cd_button])

    # Folder Selection Bar
    upbut = sweet.action_icon("lucide:folder-up", "Up One Folder", UP_BUTTON_ID)
    textdiv = sweet.ant_input("📁 Folder Path", id=PATH_INPUT_ID, persistence=PERSIST)
    # , style={"display": "none"}
    treeselectdiv = html.Div(
        [], id="pathdiv", style={"width": "100%", "minWidth": "0", "display": "none"}
    )
    treepathbar = html.Div(
        [upbut, treeselectdiv, textdiv],
        style={"display": "flex", "width": "100%", "padding": "5px 5px"},
    )
    fs_nodes = create_fs_nodes(getcwd(), ext=[".py"])
    treediv = trees.file_sys_tree(fs_nodes, TREE_ID, persistence=PERSIST)
    treeloader = sweet.spin_loader([treediv], TREE_LOADER_ID)
    middle = sweet.spin_loader([html.Div(id=RESULT_ID)], LOAD_SEARCH_ID)
    searchdiv = sweet.tag_search(
        "Search Code Content",
        TAG_SEARCH_ID,
        style={"padding": "0 5px"},
        persistence=PERSIST,
    )
    botleft = sweet.flex_row([treeloader], style={"border": ""})
    left = sweet.flex_container(
        [clean_buttons, searchdiv, treepathbar, botleft], flexcol=True
    )

    topright = [
        sweet.file_tabs(
            [], FILE_TABS_ID, NEW_TAB_ID, EDIT_TAB_ID, RUN_TAB_ID, SAVE_TAB_ID
        )
    ]  #  persistence=False
    interval = dcc.Interval(id=INTERVAL_ID, interval=500)
    prismdiv = sweet.pyprism("Loading...", id=STDOUT_ID, linenums=False)
    headerdiv = sweet.ant_input("Conda Activate and Python Command Here", id=ENV_CMD_ID)
    botright = sweet.add_header_div(headerdiv, [interval, prismdiv])

    quadlayout = sweet.quad_layout(left, middle, topright, botright, splits=[20, 0, 60])
    run_icon = sweet.iconify("ph:play-fill", "#2AB047")

    # Dash App Creation
    app = Dash(
        __name__,
        update_title=None,
        external_stylesheets=[themes.BOOTSTRAP],
    )
    app.index_string = sweet.dash_index_string()
    app.title = "CodeNav 🧭"
    app.layout = html.Main(
        [
            storepath,
            storeitems,
            storeenv,
            storecmd,
            html.Div(children=[], id="hiddendiv", style={"display": "none"}),
            sweet.notify_container([quadlayout, html.Div(id=NOTIFY_ID)]),
        ]
    )

    # Callbacks
    call.envcmd_store(app, STORE_ENV_ID, ENV_CMD_ID, NOTIFY_ID)
    call.dirpath_store(app, STORE_PATH_ID, PATH_INPUT_ID)
    call.dirpath_up(app, PATH_INPUT_ID, UP_BUTTON_ID, "value")
    call.tree_expand(app, TREE_ID)
    call.tree_create(app, TREE_LOADER_ID, PATH_INPUT_ID, TREE_ID)
    call.tree_open_file(app, STORE_ITEMS_ID, TREE_ID)
    call.tab_store(app, FILE_TABS_ID, STORE_ITEMS_ID)
    call.tab_new(app, STORE_ITEMS_ID, NEW_TAB_ID)
    call.tab_delete(app, FILE_TABS_ID, STORE_ITEMS_ID)
    call.tab_edit(app, STORE_ITEMS_ID, EDIT_TAB_ID)
    call.tab_save(app, STORE_ITEMS_ID, SAVE_TAB_ID, NOTIFY_ID)
    call.button_start_cmd(
        app,
        RUN_TAB_CMD,
        STORE_ENV_ID,
        STORE_CMD_ID,
        STORE_ITEMS_ID,
        call.read_storetabs_file,
        RUN_TAB_ID,
        run_icon,
        "children",
        first=True,
    )
    call.button_start_cmd(
        app,
        CLEAN_FILE_CMD,
        STORE_ENV_ID,
        STORE_CMD_ID,
        STORE_ITEMS_ID,
        call.read_storetabs_file,
        CLEAN_FILE_ID,
        fc_icons,
        "leftIcon",
    )
    call.button_start_cmd(
        app,
        CLEAN_ALL_CMD,
        STORE_ENV_ID,
        STORE_CMD_ID,
        STORE_PATH_ID,
        call.read_storepath,
        CLEAN_ALL_ID,
        ac_icons,
        "leftIcon",
    )
    call.button_start_cmd(
        app,
        CLEAN_DOC_CMD,
        STORE_ENV_ID,
        STORE_CMD_ID,
        STORE_PATH_ID,
        call.read_storepath,
        CLEAN_DOC_ID,
        cd_icons,
        "leftIcon",
    )
    call.stdout_update(app, STORE_CMD_ID, STDOUT_ID)
    call.stdstore_update(app, STORE_CMD_ID, INTERVAL_ID)
    call.show_hide_search(app, TAG_SEARCH_ID, RESULT_ID)
    call.run_search(app, TAG_SEARCH_ID, LOAD_SEARCH_ID, STORE_PATH_ID, RESULT_ID)
    call.open_search(app, STORE_ITEMS_ID)

    # Clientside Callback
    clientside_callback(
        call.SCROLLDOWN,
        Output("hiddendiv", "children"),
        Input(STDOUT_ID, "children"),
    )
    return app


def open_app():
    """
    Open dash app upon running script
    """
    webbrowser.open(f"http://{HOST}:{PORT}")  # type: ignore


def serve_app(port, remote, debug):
    """
    serve codenav app
    """
    global HOST, PORT  # pylint: disable=W0601
    PORT = port
    if remote:
        # host = "pycodenav"
        HOST = socket.gethostbyname(socket.gethostname())
    else:
        HOST = "localhost"
    app = codenav_app()
    if debug:
        app.run_server(debug=True, port=PORT)
    else:
        Timer(1, open_app).start()
        print(f"    Hosting CodéNav App at http://{HOST}:{PORT}")
        serve(app.server, host=HOST, port=PORT, threads=10)


if __name__ == "__main__":
    serve_app(8050, False, False)
