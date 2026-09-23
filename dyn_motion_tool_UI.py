# coding:utf-8
"""
    :module: sticky_tool_UI.py
    :description: Add procedural secondary / follow-through motion to the selected transforms
    :author: Michel 'Mitch' Pecqueur
    :date: 2026.06

import aresTools.dynMotionTool.dyn_motion_tool_UI as dmt_ui
dmt_ui.DynMotionToolUI()

import dynMotionTool.dyn_motion_tool_UI as dmt_ui
dmt_ui.DynMotionToolUI()
"""

import re
from functools import partial
from pathlib import Path

import maya.cmds as mc
import shiboken6 as shiboken
from PySide6 import QtWidgets, QtGui, QtCore

from . import dynMotion as dm
from .UI import dyn_motion_tool_ui as gui
from .__init__ import __version__  # noqa

try:
    from maya.OpenMayaUI import MQtUtil
except:
    pass


class DynMotionToolUI(gui.Ui_dyn_motion_tool_mw, QtWidgets.QMainWindow):
    """
    DynMotionTool Main Window
    """

    def __init__(self):
        mc.help(popupMode=True)
        delete_qwidget(name='dyn_motion_tool_mw')
        self.comp_tr = ''

        QtWidgets.QMainWindow.__init__(self, get_maya_window())

        self.setupUi(self)

        self.default_icons_path = Path(__file__).parent / 'icons'
        self.icon_file = self.default_icons_path / 'dynMotionTool_64.png'
        self.setWindowIcon(QtGui.QIcon(str(self.icon_file)))

        self.tool_name = 'DynMotionTool'
        self.tool_version = __version__
        self.setWindowTitle(f'{self.tool_name} v{self.tool_version}')

        self.setup_menu_bar()
        self.tooltip_to_statusbar()
        self.setup_connections()

        self.progress_bar.setValue(100)
        self.progress_bar.setEnabled(False)
        self.progress_bar.setFormat('Ready')

        self.show()

    def setup_connections(self):
        """
        Connect widgets
        """
        self.comp_l.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.comp_l.customContextMenuRequested.connect(self.comp_ctx)

        add_ctx(self.conserve_dsb, [.9], default_idx=0)
        add_ctx(self.stiffness_dsb, [.6], default_idx=0)
        add_ctx(self.damping_dsb, [.5], default_idx=0)
        add_ctx(self.dyn_scl_dsb, [.1], default_idx=0)

        self.prm_preset_pb.clicked.connect(self.prm_ctx)
        add_ctx(self.cns_rnd_dsb, [0], default_idx=0)
        add_ctx(self.stf_rnd_dsb, [0], default_idx=0)
        add_ctx(self.dmp_rnd_dsb, [0], default_idx=0)
        add_ctx(self.seed_sb, [0], default_idx=0)

        self.get_comp_pb.clicked.connect(self.set_comp)

        add_ctx(self.resample_sb, [0, 2, 3], default_idx=0)

        self.preroll_cb.stateChanged.connect(lambda state: self.preroll_sb.setEnabled(state))
        add_ctx(self.preroll_sb, [12, 24, 48], default_idx=0)

        self.add_dyn_pb.clicked.connect(self.run_sim)

    def setup_menu_bar(self):
        """
        Add menu bar
        """
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setNativeMenuBar(False)

        plt = self.menu_bar.palette()
        plt.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(55, 55, 55))
        self.menu_bar.setPalette(plt)

        # Help Menu
        self.help_menu = QtWidgets.QMenu(self.menu_bar)
        self.help_menu.setTitle('?')

        self.about_a = QtGui.QAction(self)
        self.about_a.setText('About')
        self.help_menu.addAction(self.about_a)

        self.menu_bar.addAction(self.help_menu.menuAction())

        self.about_a.triggered.connect(self.about_dialog)

        # Add menu bar
        self.setMenuBar(self.menu_bar)

    def set_comp(self):
        """
        Set compensation transform
        """
        sel = mc.ls(sl=1, tr=1)
        if len(sel) > 1:
            warning_msg('Select one single transform or nothing to clear')
            return
        if sel:
            self.comp_tr = sel[0]
        else:
            self.comp_tr = ''
        self.comp_l.setText(self.comp_tr)

    def comp_ctx(self):
        """
        Compensation context menu
        """
        names = ['Clear']
        values = ['']
        content = [{'type': 'cmds', 'name': name, 'cmd': self.clear_comp} for name, value in zip(names, values)]
        popup_menu(content=content, parent=self.prm_preset_pb)

    def clear_comp(self):
        """
        Clear compensation transform
        """
        self.comp_tr = ''
        self.comp_l.setText(self.comp_tr)

    def run_sim(self):
        """
        Run simulation
        """
        sel = mc.ls(sl=1, tr=1)
        if not sel:
            warning_msg('Select at least one transform')
            return
        trs = [int(wid.isChecked()) for wid in [self.tr_cb, self.rot_cb, self.scl_cb]]

        with UndoChunk():
            self.progress_bar.setEnabled(True)
            self.progress_bar.setFormat('Simulation in progress')
            self.progress_bar.setValue(0)

            preroll = (0, self.preroll_sb.value())[self.preroll_cb.isChecked()]

            dm.dyn_motion(objlist=sel, fromsel=False,
                          trs=trs, comp=self.comp_tr or None,

                          conserve=self.conserve_dsb.value(),
                          stiffness=self.stiffness_dsb.value(),
                          damping=self.damping_dsb.value(),

                          prm_random=(self.cns_rnd_dsb.value(), self.stf_rnd_dsb.value(), self.dmp_rnd_dsb.value()),
                          seed=self.seed_sb.value(),

                          dyn_scl=self.dyn_scl_dsb.value(),

                          bakeroll=self.bake_roll_cb.isChecked(),
                          preroll=preroll,
                          set_infinity=self.pre_post_inf_cb.isChecked(),

                          resample=self.resample_sb.value() or None,
                          simplify=self.simplify_cb.isChecked(),

                          progress=self.progress_bar)

        warning_msg('Simulation Complete!')

        self.progress_bar.setValue(100)
        self.progress_bar.setFormat('Ready')
        self.progress_bar.setEnabled(False)

    def tooltip_to_statusbar(self):
        """
        Copy toolTip messages to statusTip
        """
        for item in self.findChildren(QtWidgets.QWidget):
            tooltip = item.toolTip()
            if tooltip:
                item.setStatusTip(tooltip.replace('\n', ', '))

    def set_prm(self, value):
        """
        Set dyn parameters
        """
        values = [eval(v) for v in value.split()]
        widgets = [self.cns_rnd_dsb, self.stf_rnd_dsb, self.dmp_rnd_dsb, self.seed_sb]
        for wid, val in zip(widgets, values):
            wid.setValue(val)

    def prm_ctx(self):
        """
        Dyn parameters context menu
        """
        names = ['None\t0 0 0 0',
                 'Mild\t0.1 0.1 0.1 7',
                 'Stronger\t0.2 0.2 0.2 7']
        values = [re.sub(r'[^0-9+\-.]', ' ', name).strip() for name in names]
        content = [{'type': 'cmds', 'name': name, 'cmd': partial(self.set_prm, value)}
                   for name, value in zip(names, values)]
        popup_menu(content=content, parent=self.prm_preset_pb)

    def about_dialog(self):
        """
        Display some info about this tool
        """
        try:
            about_dlg = AboutDialog(parent=self,
                                    icon_file=self.icon_file,
                                    title=f'About {self.tool_name}')
            text = (f"{self.tool_name} Version {__version__}\n"
                    f"Copyright © 2026 Michel 'Mitch' Pecqueur\n\n")
            about_dlg.set_text(text)
            about_dlg.append_url('https://github.com/robotmitchum/dynMotionTool')
            about_dlg.exec()
        except Exception as e:
            print(e)
            pass


# User feedback

def warning_msg(msg: str, color: list = (.0, .0, .0)):
    """
    Display warning message as in-view message AND to stdout
    :param msg:
    :param color:
    :return:
    """
    back_color = rgbf_to_hex(color)
    mc.inViewMessage(amg=msg, pos='topCenter', fade=True, bkc=back_color)
    mc.warning(msg)


def rgbf_to_hex(rgb: list = (1., 1., 0), gamma: float = 2.2) -> int:
    """
    Convert rgb color to integer
    This is the color format accepted for in-view message
    :param rgb: Floating point rgb values
    :param gamma: Gamma correction
    :return: Encoded color
    """
    gc = 1.0 / gamma
    col = [int(round(v ** gc * 255)) for v in rgb]
    return (col[0] << 16) + (col[1] << 8) + col[2]


# Widgets utility functions


class AboutDialog(QtWidgets.QDialog):
    """
    Display an info dialog
    """

    def __init__(self, parent: QtWidgets.QWidget = None, title: str = 'About', icon_file: Path | str | None = None):
        super().__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.setFixedSize(0, 0)
        self.setWindowTitle(title or 'About')

        # Icon
        self.icon_l = QtWidgets.QLabel(self)
        self.icon_pixmap = None
        self.set_icon(icon_file)

        # Message with clickable URL
        self.msg_l = QtWidgets.QLabel(self)
        self.msg_l.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.msg_l.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.msg_l.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.msg_l.linkActivated.connect(self.handle_link_clicked)

        # - Layout -
        self.content_lyt = QtWidgets.QHBoxLayout()
        self.content_lyt.addWidget(self.icon_l)
        self.content_lyt.addWidget(self.msg_l)

        self.lyt = QtWidgets.QVBoxLayout()
        self.lyt.addLayout(self.content_lyt)

        self.setLayout(self.lyt)

    def set_icon(self, icon_file: Path | str | None = None):
        if icon_file:
            self.icon_pixmap = QtGui.QPixmap(str(icon_file))
        else:
            self.icon_pixmap = QtGui.QPixmap(64, 64)
            self.icon_pixmap.fill(QtCore.Qt.GlobalColor.green)
        self.icon_l.setPixmap(self.icon_pixmap)

    def set_text(self, value: str, append: bool = True):
        v = value.replace('\n', '<br>')
        if append:
            self.msg_l.setText(self.msg_l.text() + v)
        else:
            self.msg_l.setText(v)

    def append_url(self, value: str, end_line: str = '\n'):
        v = end_line.replace('\n', '<br>')
        self.msg_l.setText(f'{self.msg_l.text()}<a href="{value}">{value}</a>' + v)

    def handle_link_clicked(self, url: str):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        self.accept()


# Misc UI functions

class UndoChunk(object):
    """
    Open/close an undo chunk to ensure correct undo behavior when calling code from a UI

    Example:
    from aresCoreUI.ui_utils import UndoChunk

    with UndoChunk():
        res = mc.ls(...)
        print(res)

    UndoChunk is active only within current context
    """

    def __enter__(self):
        mc.undoInfo(ock=True)

    def __exit__(self, typ, val, traceback):
        mc.undoInfo(cck=True)


def get_maya_window() -> QtWidgets or None:
    """
    Get Maya main window
    :return: Maya window pointer
    """
    mwindow = MQtUtil.mainWindow()
    pointer = shiboken.wrapInstance(int(mwindow), QtWidgets.QMainWindow)
    return pointer


def delete_qwidget(name: str):
    """
    Delete given QWidget
    :param name:
    :return: None
    """
    mwindow = MQtUtil.findControl(name)
    if mwindow:
        pointer = shiboken.wrapInstance(int(mwindow), QtWidgets.QMainWindow)
        shiboken.delete(pointer)


def add_ctx(widget: QtWidgets.QWidget, values: list = (), names: list | None = None, default_idx: int | None = None,
            trigger: QtWidgets.QWidget | None = None):
    """
    Add a simple context menu setting provided values to the given widget

    (Ported from PyQt5 with minor modifications to make it work)

    :param widget: The widget to which the context menu will be added
    :param values: A list of values to be added as actions in the context menu
    :param default_idx:
    :param names: A list of strings or values to be added as action names
    must match values length
    :param trigger: Optional widget triggering the context menu
    typically a QPushButton or QToolButton
    """
    if not names:
        names = list(values)
        if default_idx is not None:
            names[default_idx] = f'{names[default_idx]} (Default)'

    def show_context_menu(event):
        menu = QtWidgets.QMenu(widget)
        for name, value in zip(names, values):
            if value == '---':
                menu.addSeparator()
            else:
                action = menu.addAction(f'{name}')
                if hasattr(widget, 'setValue'):
                    action.triggered.connect(partial(widget.setValue, value))
                elif hasattr(widget, 'setFullPath'):
                    action.triggered.connect(partial(widget.setFullPath, value))
                elif hasattr(widget, 'setText'):
                    action.triggered.connect(partial(widget.setText, value))

        pos = widget.mapToGlobal(widget.contentsRect().bottomLeft())
        menu.setMinimumWidth(widget.width())
        menu.exec_(pos)
        menu.deleteLater()

    widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
    if trigger is None:
        widget.customContextMenuRequested.connect(show_context_menu)
    else:
        trigger.clicked.connect(show_context_menu)


def popup_menu(content: list, parent: QtWidgets.QWidget | None = None):
    """
    Create a popup menu

    :param content: a list of dictionary containing action names (str) execution commands (python)
    :param parent: Specify parent widget

    [
        { 'type': 'cmds', 'name': 'Hello', 'cmd': 'print("Hello world !")' },
        { 'type': '---' },
        { 'type': 'cmds', 'name': 'Knock-Knock', 'cmd': 'print("Who's there?")' }
    ]

    type : separator as '---' or command as 'cmds'
    name : Name of the command displayed in popup_menu
    """
    # Create menu widget
    menu = QtWidgets.QMenu(parent)
    cur_pos = QtGui.QCursor.pos()

    # Populate menu
    for item in content:
        if 'type' in list(item.keys()):
            if item['type'] == '---':
                menu.addSeparator()
            elif item['type'] == 'cmds':
                action = menu.addAction(item['name'])
                action.triggered.connect(item['cmd'])

    # exec menu
    menu.exec_(cur_pos)
    menu.deleteLater()
