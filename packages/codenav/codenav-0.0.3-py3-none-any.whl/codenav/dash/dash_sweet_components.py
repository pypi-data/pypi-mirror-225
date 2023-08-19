# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 23:39:06 2023

@author: jkris
"""

# https://icon-sets.iconify.design/fluent/folder-arrow-up-16-filled/

# use this scrollbar?
# import feffery_utils_components as fuc
# alldiv = fuc.FefferyScrollbars(divlist, style={"height": "100vh", "color": "white"})
# from dash_holoniq_components import PageTitle

from os import path
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import feffery_antd_components as fac
from dash_iconify import DashIconify
import dash_editor_components as dec
from dash_ace import DashAceEditor
from dash import html  # , dash_table, dcc
from .helper import round_sigfig, set_default


BG_COLOR_1_DARK = "#181818"
BG_COLOR_2_DARK = "#5C5F66"
BG_COLOR_3_DARK = "#373A40"
BG_COLOR_4_DARK = "#25262B"  # darkest one?
BG_COLOR_5_DARK = "#2C3333"
BG_COLOR_BLUE_POP = "#094F9C"
FG_COLOR_1_DARK = "white"
FG_COLOR_2_DARK = "rgb(206, 212, 218)"
BORD_COLOR_1_DARK = "#5C5F66"
# bg_color = "#101113", "#162780"


def resize_col(children, width: str, **kwargs):
    """
    resize_col
    """
    divstyle = {
        "height": "100vh",
        "width": width,
        "minWidth": "6vw",
        "display": "inline-block",
        "overflow": "auto",
        "resize": "horizontal",
        "background": BG_COLOR_1_DARK,
        "border": f"1px solid {BG_COLOR_2_DARK}",
    }
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    return html.Div(children, style=divstyle, **kwargs)


def resize_row(children, height: str, **kwargs):
    """
    resize_row
    """
    divstyle = {
        "height": height,
        "minHeight": "10vh",
        "maxHeight": "90vh",
        "overflow": "auto",
        "resize": "vertical",
        "display": "flex-inline",
        "background": BG_COLOR_1_DARK,
        "border": f"1px solid {BORD_COLOR_1_DARK}",
    }
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    return html.Div(children, style=divstyle, **kwargs)


def flex_col(children, **kwargs):
    """
    flex_col
    """
    divstyle = {
        "display": "flex",
        "flex": "1",
        "flexDirection": "column",
        "minWidth": "6vw",
        "background": BG_COLOR_1_DARK,
    }
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    return html.Div(children, style=divstyle, **kwargs)


def flex_row(children, **kwargs):
    """
    flex_row
    """
    divstyle = {
        "flex": "1",
        "display": "flex-inline",
        "background": BG_COLOR_1_DARK,
        "overflow": "auto",
        "border": f"1px solid {BORD_COLOR_1_DARK}",
        "height": "100%",
    }
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    return html.Div(children, style=divstyle, **kwargs)


def flex_container(children, **kwargs):
    """
    flex_container
    """
    flexdir = "row"
    if "flexcol" in kwargs:
        if kwargs["flexcol"]:
            flexdir = "column"
        del kwargs["flexcol"]
    divstyle = {
        "width": "100%",
        "height": "100%",
        "display": "flex",
        "background": BG_COLOR_1_DARK,
        "colorScheme": "dark",
        "flexDirection": flexdir,
        "minHeight": "2vh",
        "minWidth": "2vw",
    }
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    return html.Div(children, style=divstyle, **kwargs)


def tri_layout(left, topright, botright, splits: list[int] = None):
    """
    tri_layout
    """
    splits = set_default(splits, [30, 50])
    left_col = resize_col(left, f"{splits[0]}vw", id="left")
    topright_row = resize_row(topright, f"{splits[1]}vh", id="topright")
    botright_row = flex_row(botright, id="botright")
    right_col = flex_col([topright_row, botright_row])
    return flex_container(
        [left_col, right_col], style={"width": "100vw", "height": "100vh"}
    )


def quad_layout(left, middle, topright, botright, splits: list[int] = None):
    """
    quad_layout
    """
    splits = set_default(splits, [30, 0, 50])
    left_col = resize_col(left, f"{splits[0]}vw", id="left")
    middle_col = resize_col(
        middle, f"{splits[1]}vw", id="middle", style={"minWidth": "0"}
    )
    topright_row = resize_row(topright, f"{splits[2]}vh", id="topright")
    botright_row = flex_row(botright, id="botright")
    right_col = flex_col([topright_row, botright_row])
    return flex_container(
        [left_col, middle_col, right_col], style={"width": "100vw", "height": "100vh"}
    )


def add_header_div(header_div, content_div):
    """
    add_header_div
    """
    header_style = {
        "flex": "0 0 2rem",
        "border": "",
        "background": BG_COLOR_5_DARK,
    }
    headerrow = flex_row(header_div, style=header_style)
    contentrow = flex_row(content_div, style={"border": ""})
    return flex_container([headerrow, contentrow], flexcol=True)


def pyprism(
    text: str,
    isfile: bool = False,
    linenums: bool = True,
    **kwargs,
):
    """
    mantine_prism
    """
    if isfile:
        with open(text, "r", encoding="utf-8") as filereader:
            text = filereader.read()
    divstyle = {"width": "100%", "height": "100%"}
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    theme = {"colorScheme": "dark"}
    if "theme" in kwargs:
        theme.update(kwargs["theme"])
        del kwargs["theme"]
    prismdiv = dmc.Prism(
        children=text,
        language="python",
        withLineNumbers=linenums,
        style=divstyle,
        **kwargs,
    )
    darkprismdiv = dmc.MantineProvider(
        [prismdiv],
        theme=theme,
    )
    return darkprismdiv


def hover_message(component, message: str, style: dict = None):
    """
    hover_message
    """
    dropdownstyle = {
        "backgroundColor": BG_COLOR_4_DARK,
        "borderColor": BG_COLOR_3_DARK,
    }
    text = dmc.Text(message, size="sm", color=FG_COLOR_1_DARK)
    hover_children = [
        dmc.HoverCardTarget(component),
        dmc.HoverCardDropdown(text, style=dropdownstyle),
    ]
    divstyle = {"minWidth": "initial"}
    if style:
        divstyle.update(style)
    div = dmc.HoverCard(
        children=hover_children,
        openDelay=200,
        closeDelay=0,
        style=divstyle,
    )
    return div


def iconify(name, color):
    """
    icon
    """
    return DashIconify(icon=name, color=color, width=25)


def action_icon(
    iconname: str,
    hover: str,
    call_id: str,
    variant: str = "subtle",
    iconcolor: str = FG_COLOR_1_DARK,
) -> str:
    """
    action_icon
    """
    icon = DashIconify(icon=iconname, color=iconcolor, width=25)
    action = dmc.ActionIcon(icon, variant=variant, size="lg", id=call_id)
    actionhover = hover_message(action, hover)
    darkaction = dmc.MantineProvider(actionhover, theme={"colorScheme": "dark"})
    return darkaction


def pyeditor(text: str, isfile: bool = False, **kwargs):
    """
    pyeditor
    """
    if isfile:
        with open(text, "r", encoding="utf-8") as filereader:
            text = filereader.read()
    pyedit = dec.PythonEditor(
        **kwargs,
        # value=text,
        style={
            "color": FG_COLOR_1_DARK,
            "background": "transparent",
            "width": "100%",
            "height": "100%",
            "overflow": "auto",
        },
    )
    return pyedit


def ace_pyeditor(
    text: str,
    isfile: bool = False,
    **kwargs,
):
    """
    ace_pyeditor
    """
    if isfile:
        with open(text, "r", encoding="utf-8") as filereader:
            text = filereader.read()
    aceeditor = DashAceEditor(
        **kwargs,
        value=text,
        theme="tomorrow",  #  github, monokai, tomorrow, twilight, textmate
        mode="python",
        tabSize=4,
        enableBasicAutocompletion=True,
        enableLiveAutocompletion=True,
        # autocompleter='/autocompleter?prefix=',
        # enableSnippets=True,
        placeholder="Python code ...",
        style={
            "color": FG_COLOR_2_DARK,
            "background": "transparent",
            "width": "100%",
            "height": "100%",
        },
    )
    return aceeditor


def file_tabs(
    items: list,
    call_id: str,
    newtab_id: str,
    edittab_id: str,
    runtab_id: str,
    savetab_id: str,
    **kwargs,
):
    """
    filetabs

    items = {label, key, children, closable: True}
    """
    savebuton = action_icon("fluent:save-28-regular", "Save Current File", savetab_id)
    runbutton = action_icon(
        "ph:play-fill", "Run Current File", runtab_id, iconcolor="#2AB047"
    )
    newtabbutton = action_icon("carbon:new-tab", "New Tab", newtab_id)
    editbutton = action_icon("carbon:edit", "Edit Current File", edittab_id)
    rightdiv = dmc_group([runbutton, editbutton, newtabbutton])
    # add play button here
    tabs = fac.AntdTabs(
        id=call_id,
        type="editable-card",
        items=items,
        tabBarRightExtraContent=rightdiv,
        tabBarLeftExtraContent=savebuton,
        style={"height": "100%"},
        **kwargs,
    )
    return tabs


def icon_button(text: str, iconnames: list[str], message: str, **kwargs):
    """
    icon_button
    """
    buttonstyle = {
        "border": f"1px solid {BG_COLOR_3_DARK}",
        "minWidth": "70px",
        "width": "100%",
        "background": BG_COLOR_BLUE_POP,
    }
    if "style" in kwargs:
        buttonstyle.update(kwargs["style"])
        del kwargs["style"]
    call_id = text
    if "id" in kwargs:
        call_id = kwargs["id"]
    iconslist = [DashIconify(icon=icon, height=25) for icon in iconnames]
    button = dmc.Button(text, leftIcon=iconslist, style=buttonstyle, id=call_id)
    if len(message) > 0:
        button = hover_message(button, message, style={"minWidth": "70px"})
    return button, iconslist


def dmc_group(children: list, style: dict = None):
    """
    dmc_group
    """
    group = dmc.Group(children, grow=True, spacing=5, style={"width": "100%"})
    divstyle = {"width": "100%", "padding": "5px 5px"}
    if style:
        divstyle.update(style)
    groupdiv = html.Div([group], style=divstyle)
    return groupdiv


def tag_search(placeholder: str = "Search", call_id: str = "tagsearch", **kwargs):
    """
    tag_search
    """
    divstyle = {"width": "100%"}  # "padding": "0px 5px",
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    tagsearch = fac.AntdSelect(
        id=call_id,
        options=[],
        locale="en-us",
        placeholder="🔎 " + placeholder,
        mode="tags",
        style=divstyle,
        **kwargs,
    )
    tagsearchdiv = html.Div(tagsearch, style={"width": "100%"})
    return tagsearchdiv


def ant_input(placeholder: str, **kwargs):
    """
    ant_input
    """
    divstyle = {
        "color": FG_COLOR_1_DARK,
        "background": BG_COLOR_2_DARK,
        "borderColor": BG_COLOR_3_DARK,
        "width": "100%",
    }
    if "style" in kwargs:
        divstyle.update(kwargs["style"])
        del kwargs["style"]
    inputdiv = fac.AntdInput(
        placeholder=placeholder,
        allowClear=True,
        style=divstyle,
        **kwargs,
    )
    return inputdiv


def spin_loader(children, call_id: str):
    """
    spin_loader
    """
    spinner = dbc.Spinner(
        children=children,
        id=call_id,
        color="#094F9C",
        delay_show=200,
        delay_hide=100,
        spinner_style={"position": "absolute", "top": "10px"},
    )
    return spinner


def dash_index_string():
    """
    set_index_string
    """
    indexstr = """
<!DOCTYPE html>\n<div style="width:100vw;height:100vh;background:#181818;">\n    <head>\n        {%metas%}\n        <title>{%title%}</title>
        {%favicon%}\n        {%css%}\n    </head>\n    <div>\n        <!--[if IE]><script>
        alert("Dash v2.7+ does not support Internet Explorer. Please use a newer browser.");
        </script><![endif]-->\n        {%app_entry%}\n        <footer>\n            {%config%}
            {%scripts%}\n            {%renderer%}\n        </footer>\n    </div>\n</div>"""
    return indexstr


def dark_text(text: str, style: dict = None):
    """
    dark_text
    """
    divstyle = {
        "background": "transparent",
        "padding": "0.5rem  0 0 2%",
        "height": "100%",
        "verticalAlign": "middle",
        "lineHeight": "100%",
    }
    if style:
        divstyle.update(style)
    div = html.Div(
        html.Div(
            text,
            style={
                "color": "white",
                "width": "100%",
                "height": "100%",
                "padding": "0 0 0 1%",
            },
        ),
        style=divstyle,
    )
    return div


def notify_container(children: list):
    """
    notify_container
    """
    cont = dmc.NotificationsProvider(children)
    darkcont = dmc.MantineProvider([cont], theme={"colorScheme": "dark"})
    return darkcont


def notify(title: str, message: str, iconname: str, iconcolor: str):
    """
    notify
    """
    notif = dmc.Notification(
        id=message,
        title=title,
        action="show",
        message=message,
        icon=iconify(iconname, iconcolor),
    )
    return notif


def search_result(result: dict, resultnum: int, padding: str = "2.5px 5px 2.5px 5px"):
    """
    search_result
    """
    filepath_id = {"type": "respath", "index": f"{resultnum}"}
    sniptext_id = {"type": "restext", "index": f"{resultnum}"}
    filename = path.basename(result["path"])
    div1 = dark_text(f"#{resultnum}: {filename}")
    div2 = dark_text(f"Score : {round_sigfig(result['score'],4)}")
    div3 = dark_text(
        f"      {result['string_num']} / {result['newline_num']} [matches / lines]"
    )
    div4 = html.Div(result["path"], style={"display": "none"}, id=filepath_id)
    div5 = html.Div(result["text"], style={"display": "none"}, id=sniptext_id)
    snipicons = ["heroicons:scissors-solid", "majesticons:open-line"]
    snipbutton, _none = icon_button(
        "",
        snipicons,
        "Open Snip",
        style={"background": BG_COLOR_2_DARK},
        id={"type": "snipbutton", "index": str(resultnum)},
    )
    fileicons = ["ant-design:file-twotone", "majesticons:open-line"]
    filebutton, _none = icon_button(
        "",
        fileicons,
        "Open File",
        style={"background": BG_COLOR_2_DARK},
        id={"type": "filebutton", "index": str(resultnum)},
    )
    buttons = dmc_group([snipbutton, filebutton])
    alldivs = html.Div(
        [div1, div2, div3, div4, div5, buttons],
        id=f"searchtext{resultnum}",
        style={
            "border": f"1px solid {BG_COLOR_2_DARK}",
            "borderRadius": "5px",
            "outline": "{BG_COLOR_1_DARK} solid 5px",
            "background": "transparent",
            "overflow": "hidden",
        },
    )
    container = html.Div(
        alldivs,
        style={
            "padding": padding,
            "background": "transparent",
        },
    )
    # SHOULD I ALSO ADD THE CALLBACK GENERATION HERE?
    return container


def create_search_results(results):
    """
    create_search_results
    """
    divlist = []
    for i, result in enumerate(results):
        if i == 0:
            divlist.append(search_result(result, i + 1, padding="5px 5px 2.5px 5px"))
        elif i == (len(results) - 1):
            divlist.append(search_result(result, i + 1, padding="2.5px 5px 5px 5px"))
        else:
            divlist.append(search_result(result, i + 1))
    alldiv = html.Div(divlist)
    return alldiv


# Other Ideas Antd navigation menu, sidebar, or just use Mantine icons bar
