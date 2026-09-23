# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dyn_motion_tool_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDoubleSpinBox,
    QFrame, QHBoxLayout, QLabel, QMainWindow,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_dyn_motion_tool_mw(object):
    def setupUi(self, dyn_motion_tool_mw):
        if not dyn_motion_tool_mw.objectName():
            dyn_motion_tool_mw.setObjectName(u"dyn_motion_tool_mw")
        dyn_motion_tool_mw.resize(480, 453)
        font = QFont()
        font.setPointSize(10)
        dyn_motion_tool_mw.setFont(font)
        dyn_motion_tool_mw.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(dyn_motion_tool_mw)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.trs_lyt = QHBoxLayout()
        self.trs_lyt.setObjectName(u"trs_lyt")
        self.tr_cb = QCheckBox(self.centralwidget)
        self.tr_cb.setObjectName(u"tr_cb")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tr_cb.sizePolicy().hasHeightForWidth())
        self.tr_cb.setSizePolicy(sizePolicy)

        self.trs_lyt.addWidget(self.tr_cb)

        self.rot_cb = QCheckBox(self.centralwidget)
        self.rot_cb.setObjectName(u"rot_cb")
        sizePolicy.setHeightForWidth(self.rot_cb.sizePolicy().hasHeightForWidth())
        self.rot_cb.setSizePolicy(sizePolicy)
        self.rot_cb.setChecked(True)

        self.trs_lyt.addWidget(self.rot_cb)

        self.scl_cb = QCheckBox(self.centralwidget)
        self.scl_cb.setObjectName(u"scl_cb")
        sizePolicy.setHeightForWidth(self.scl_cb.sizePolicy().hasHeightForWidth())
        self.scl_cb.setSizePolicy(sizePolicy)

        self.trs_lyt.addWidget(self.scl_cb)


        self.verticalLayout.addLayout(self.trs_lyt)

        self.comp_lyt = QHBoxLayout()
        self.comp_lyt.setObjectName(u"comp_lyt")
        self.get_comp_pb = QPushButton(self.centralwidget)
        self.get_comp_pb.setObjectName(u"get_comp_pb")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.get_comp_pb.sizePolicy().hasHeightForWidth())
        self.get_comp_pb.setSizePolicy(sizePolicy1)

        self.comp_lyt.addWidget(self.get_comp_pb)

        self.comp_l = QLabel(self.centralwidget)
        self.comp_l.setObjectName(u"comp_l")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comp_l.sizePolicy().hasHeightForWidth())
        self.comp_l.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.comp_l.setFont(font1)
        self.comp_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.comp_lyt.addWidget(self.comp_l)


        self.verticalLayout.addLayout(self.comp_lyt)

        self.sim_settings_l = QLabel(self.centralwidget)
        self.sim_settings_l.setObjectName(u"sim_settings_l")
        sizePolicy2.setHeightForWidth(self.sim_settings_l.sizePolicy().hasHeightForWidth())
        self.sim_settings_l.setSizePolicy(sizePolicy2)
        self.sim_settings_l.setMinimumSize(QSize(0, 20))
        self.sim_settings_l.setStyleSheet(u"background-color: rgb(95, 95, 127);")

        self.verticalLayout.addWidget(self.sim_settings_l)

        self.conserve_lyt = QHBoxLayout()
        self.conserve_lyt.setObjectName(u"conserve_lyt")
        self.conserve_l = QLabel(self.centralwidget)
        self.conserve_l.setObjectName(u"conserve_l")
        self.conserve_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conserve_lyt.addWidget(self.conserve_l)

        self.conserve_dsb = QDoubleSpinBox(self.centralwidget)
        self.conserve_dsb.setObjectName(u"conserve_dsb")
        self.conserve_dsb.setFrame(False)
        self.conserve_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conserve_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.conserve_dsb.setDecimals(3)
        self.conserve_dsb.setMinimum(0.100000000000000)
        self.conserve_dsb.setMaximum(1.000000000000000)
        self.conserve_dsb.setSingleStep(0.050000000000000)
        self.conserve_dsb.setValue(0.900000000000000)

        self.conserve_lyt.addWidget(self.conserve_dsb)


        self.verticalLayout.addLayout(self.conserve_lyt)

        self.stiffness_lyt = QHBoxLayout()
        self.stiffness_lyt.setObjectName(u"stiffness_lyt")
        self.stiffness_l = QLabel(self.centralwidget)
        self.stiffness_l.setObjectName(u"stiffness_l")
        self.stiffness_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stiffness_lyt.addWidget(self.stiffness_l)

        self.stiffness_dsb = QDoubleSpinBox(self.centralwidget)
        self.stiffness_dsb.setObjectName(u"stiffness_dsb")
        self.stiffness_dsb.setFrame(False)
        self.stiffness_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stiffness_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.stiffness_dsb.setDecimals(3)
        self.stiffness_dsb.setMinimum(0.050000000000000)
        self.stiffness_dsb.setMaximum(1.000000000000000)
        self.stiffness_dsb.setSingleStep(0.050000000000000)
        self.stiffness_dsb.setValue(0.600000000000000)

        self.stiffness_lyt.addWidget(self.stiffness_dsb)


        self.verticalLayout.addLayout(self.stiffness_lyt)

        self.damping_lyt = QHBoxLayout()
        self.damping_lyt.setObjectName(u"damping_lyt")
        self.damping_l = QLabel(self.centralwidget)
        self.damping_l.setObjectName(u"damping_l")
        self.damping_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.damping_lyt.addWidget(self.damping_l)

        self.damping_dsb = QDoubleSpinBox(self.centralwidget)
        self.damping_dsb.setObjectName(u"damping_dsb")
        self.damping_dsb.setFrame(False)
        self.damping_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.damping_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.damping_dsb.setDecimals(3)
        self.damping_dsb.setMaximum(1.000000000000000)
        self.damping_dsb.setSingleStep(0.050000000000000)
        self.damping_dsb.setValue(0.500000000000000)

        self.damping_lyt.addWidget(self.damping_dsb)


        self.verticalLayout.addLayout(self.damping_lyt)

        self.prm_random_lyt = QHBoxLayout()
        self.prm_random_lyt.setObjectName(u"prm_random_lyt")
        self.prm_preset_pb = QPushButton(self.centralwidget)
        self.prm_preset_pb.setObjectName(u"prm_preset_pb")

        self.prm_random_lyt.addWidget(self.prm_preset_pb)

        self.prm_dsb_lyt = QHBoxLayout()
        self.prm_dsb_lyt.setSpacing(0)
        self.prm_dsb_lyt.setObjectName(u"prm_dsb_lyt")
        self.cns_rnd_dsb = QDoubleSpinBox(self.centralwidget)
        self.cns_rnd_dsb.setObjectName(u"cns_rnd_dsb")
        self.cns_rnd_dsb.setFrame(False)
        self.cns_rnd_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cns_rnd_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cns_rnd_dsb.setDecimals(3)
        self.cns_rnd_dsb.setMaximum(1.000000000000000)
        self.cns_rnd_dsb.setSingleStep(0.050000000000000)

        self.prm_dsb_lyt.addWidget(self.cns_rnd_dsb)

        self.stf_rnd_dsb = QDoubleSpinBox(self.centralwidget)
        self.stf_rnd_dsb.setObjectName(u"stf_rnd_dsb")
        self.stf_rnd_dsb.setFrame(False)
        self.stf_rnd_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stf_rnd_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.stf_rnd_dsb.setDecimals(3)
        self.stf_rnd_dsb.setMaximum(1.000000000000000)
        self.stf_rnd_dsb.setSingleStep(0.050000000000000)

        self.prm_dsb_lyt.addWidget(self.stf_rnd_dsb)

        self.dmp_rnd_dsb = QDoubleSpinBox(self.centralwidget)
        self.dmp_rnd_dsb.setObjectName(u"dmp_rnd_dsb")
        self.dmp_rnd_dsb.setFrame(False)
        self.dmp_rnd_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dmp_rnd_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.dmp_rnd_dsb.setDecimals(3)
        self.dmp_rnd_dsb.setMaximum(1.000000000000000)
        self.dmp_rnd_dsb.setSingleStep(0.050000000000000)

        self.prm_dsb_lyt.addWidget(self.dmp_rnd_dsb)

        self.seed_sb = QSpinBox(self.centralwidget)
        self.seed_sb.setObjectName(u"seed_sb")
        self.seed_sb.setFrame(False)
        self.seed_sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.seed_sb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.seed_sb.setMaximum(999)

        self.prm_dsb_lyt.addWidget(self.seed_sb)


        self.prm_random_lyt.addLayout(self.prm_dsb_lyt)


        self.verticalLayout.addLayout(self.prm_random_lyt)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.dyn_scl_lyt = QHBoxLayout()
        self.dyn_scl_lyt.setObjectName(u"dyn_scl_lyt")
        self.dyn_scl_l = QLabel(self.centralwidget)
        self.dyn_scl_l.setObjectName(u"dyn_scl_l")
        self.dyn_scl_l.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dyn_scl_lyt.addWidget(self.dyn_scl_l)

        self.dyn_scl_dsb = QDoubleSpinBox(self.centralwidget)
        self.dyn_scl_dsb.setObjectName(u"dyn_scl_dsb")
        self.dyn_scl_dsb.setFrame(False)
        self.dyn_scl_dsb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dyn_scl_dsb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.dyn_scl_dsb.setDecimals(3)
        self.dyn_scl_dsb.setMinimum(0.010000000000000)
        self.dyn_scl_dsb.setMaximum(10.000000000000000)
        self.dyn_scl_dsb.setSingleStep(0.050000000000000)
        self.dyn_scl_dsb.setValue(0.100000000000000)

        self.dyn_scl_lyt.addWidget(self.dyn_scl_dsb)


        self.verticalLayout.addLayout(self.dyn_scl_lyt)

        self.bake_settings_l = QLabel(self.centralwidget)
        self.bake_settings_l.setObjectName(u"bake_settings_l")
        sizePolicy2.setHeightForWidth(self.bake_settings_l.sizePolicy().hasHeightForWidth())
        self.bake_settings_l.setSizePolicy(sizePolicy2)
        self.bake_settings_l.setMinimumSize(QSize(0, 20))
        self.bake_settings_l.setStyleSheet(u"background-color: rgb(95, 95, 127);")

        self.verticalLayout.addWidget(self.bake_settings_l)

        self.preroll_lyt = QHBoxLayout()
        self.preroll_lyt.setObjectName(u"preroll_lyt")
        self.spc_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.preroll_lyt.addItem(self.spc_3)

        self.bake_roll_cb = QCheckBox(self.centralwidget)
        self.bake_roll_cb.setObjectName(u"bake_roll_cb")
        sizePolicy2.setHeightForWidth(self.bake_roll_cb.sizePolicy().hasHeightForWidth())
        self.bake_roll_cb.setSizePolicy(sizePolicy2)

        self.preroll_lyt.addWidget(self.bake_roll_cb)

        self.spc_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.preroll_lyt.addItem(self.spc_1)

        self.preroll_cb = QCheckBox(self.centralwidget)
        self.preroll_cb.setObjectName(u"preroll_cb")
        sizePolicy.setHeightForWidth(self.preroll_cb.sizePolicy().hasHeightForWidth())
        self.preroll_cb.setSizePolicy(sizePolicy)
        self.preroll_cb.setChecked(True)

        self.preroll_lyt.addWidget(self.preroll_cb)

        self.preroll_sb = QSpinBox(self.centralwidget)
        self.preroll_sb.setObjectName(u"preroll_sb")
        sizePolicy.setHeightForWidth(self.preroll_sb.sizePolicy().hasHeightForWidth())
        self.preroll_sb.setSizePolicy(sizePolicy)
        self.preroll_sb.setFrame(False)
        self.preroll_sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preroll_sb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.preroll_sb.setMinimum(5)
        self.preroll_sb.setMaximum(240)
        self.preroll_sb.setValue(12)

        self.preroll_lyt.addWidget(self.preroll_sb)

        self.spc_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.preroll_lyt.addItem(self.spc_4)


        self.verticalLayout.addLayout(self.preroll_lyt)

        self.post_process_l = QLabel(self.centralwidget)
        self.post_process_l.setObjectName(u"post_process_l")
        sizePolicy2.setHeightForWidth(self.post_process_l.sizePolicy().hasHeightForWidth())
        self.post_process_l.setSizePolicy(sizePolicy2)
        self.post_process_l.setMinimumSize(QSize(0, 20))
        self.post_process_l.setStyleSheet(u"background-color: rgb(95, 95, 127);")

        self.verticalLayout.addWidget(self.post_process_l)

        self.resample_lyt = QHBoxLayout()
        self.resample_lyt.setObjectName(u"resample_lyt")
        self.spc_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resample_lyt.addItem(self.spc_2)

        self.resample_l = QLabel(self.centralwidget)
        self.resample_l.setObjectName(u"resample_l")
        sizePolicy2.setHeightForWidth(self.resample_l.sizePolicy().hasHeightForWidth())
        self.resample_l.setSizePolicy(sizePolicy2)

        self.resample_lyt.addWidget(self.resample_l)

        self.resample_sb = QSpinBox(self.centralwidget)
        self.resample_sb.setObjectName(u"resample_sb")
        self.resample_sb.setMinimumSize(QSize(40, 0))
        self.resample_sb.setFrame(False)
        self.resample_sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resample_sb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.resample_sb.setMaximum(5)

        self.resample_lyt.addWidget(self.resample_sb)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resample_lyt.addItem(self.horizontalSpacer_4)

        self.simplify_cb = QCheckBox(self.centralwidget)
        self.simplify_cb.setObjectName(u"simplify_cb")
        sizePolicy2.setHeightForWidth(self.simplify_cb.sizePolicy().hasHeightForWidth())
        self.simplify_cb.setSizePolicy(sizePolicy2)

        self.resample_lyt.addWidget(self.simplify_cb)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resample_lyt.addItem(self.horizontalSpacer_3)

        self.pre_post_inf_cb = QCheckBox(self.centralwidget)
        self.pre_post_inf_cb.setObjectName(u"pre_post_inf_cb")
        self.pre_post_inf_cb.setChecked(True)

        self.resample_lyt.addWidget(self.pre_post_inf_cb)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resample_lyt.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.resample_lyt)

        self.add_dyn_pb = QPushButton(self.centralwidget)
        self.add_dyn_pb.setObjectName(u"add_dyn_pb")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.add_dyn_pb.sizePolicy().hasHeightForWidth())
        self.add_dyn_pb.setSizePolicy(sizePolicy3)
        self.add_dyn_pb.setStyleSheet(u"QPushButton{background-color: rgb(95, 159, 127)}")

        self.verticalLayout.addWidget(self.add_dyn_pb)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(0)

        self.verticalLayout.addWidget(self.progress_bar)

        dyn_motion_tool_mw.setCentralWidget(self.centralwidget)

        self.retranslateUi(dyn_motion_tool_mw)

        QMetaObject.connectSlotsByName(dyn_motion_tool_mw)
    # setupUi

    def retranslateUi(self, dyn_motion_tool_mw):
        dyn_motion_tool_mw.setWindowTitle(QCoreApplication.translate("dyn_motion_tool_mw", u"DynMotionTool", None))
#if QT_CONFIG(tooltip)
        self.tr_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Enable simulation on Translation", None))
#endif // QT_CONFIG(tooltip)
        self.tr_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Translation", None))
#if QT_CONFIG(tooltip)
        self.rot_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Enable simulation on Rotation", None))
#endif // QT_CONFIG(tooltip)
        self.rot_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Rotation", None))
#if QT_CONFIG(tooltip)
        self.scl_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Enable simulation on Scale", None))
#endif // QT_CONFIG(tooltip)
        self.scl_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Scale", None))
#if QT_CONFIG(tooltip)
        self.get_comp_pb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Use selected transform as compensation transform\n"
"Typical usage: walk, run or characters boarding a vehicle", None))
#endif // QT_CONFIG(tooltip)
        self.get_comp_pb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"\U0001f683Get Comp Transform", None))
#if QT_CONFIG(tooltip)
        self.comp_l.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Current compensation transform\n"
"Transformation from this object will be removed from simulated objects", None))
#endif // QT_CONFIG(tooltip)
        self.comp_l.setText("")
        self.sim_settings_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Simulation Settings", None))
        self.conserve_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Conserve", None))
#if QT_CONFIG(tooltip)
        self.conserve_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Atmospheric drag / viscosity\n"
"1 = no drag, full velocity preserved", None))
#endif // QT_CONFIG(tooltip)
        self.stiffness_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Stiffness", None))
#if QT_CONFIG(tooltip)
        self.stiffness_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"How strongly the simulated position is pulled back toward the goal each frame\n"
"1 = rigid, no lag", None))
#endif // QT_CONFIG(tooltip)
        self.damping_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Damping", None))
#if QT_CONFIG(tooltip)
        self.damping_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Suppresses oscillation\n"
"0 = no damping 'bouncy forever'", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.prm_preset_pb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Apply randomization to parameters to get variation with cloned or symmetrical rigs\n"
"Click to load a preset", None))
#endif // QT_CONFIG(tooltip)
        self.prm_preset_pb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"\U0001f3b2 Parameter Randomization", None))
#if QT_CONFIG(tooltip)
        self.cns_rnd_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Conserve Randomization", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.stf_rnd_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Stiffness Randomization", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.dmp_rnd_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Damping Randomization", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.seed_sb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Random generator seed, a different value gives a different random result", None))
#endif // QT_CONFIG(tooltip)
        self.dyn_scl_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Dynamic Scale Factor", None))
#if QT_CONFIG(tooltip)
        self.dyn_scl_dsb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Overall dynamic scale factor\n"
"Higher value = More motion keeping character", None))
#endif // QT_CONFIG(tooltip)
        self.bake_settings_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Bake Settings", None))
#if QT_CONFIG(tooltip)
        self.bake_roll_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Timeline is advanced frame-by-frame before sampling\n"
"Slower but required for pinned controls", None))
#endif // QT_CONFIG(tooltip)
        self.bake_roll_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Bake Roll", None))
#if QT_CONFIG(tooltip)
        self.preroll_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Run simulation for a given number of frames before the first frame", None))
#endif // QT_CONFIG(tooltip)
        self.preroll_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Preroll", None))
#if QT_CONFIG(tooltip)
        self.preroll_sb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Number of frames used for preroll", None))
#endif // QT_CONFIG(tooltip)
        self.post_process_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Post-process", None))
        self.resample_l.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Resample", None))
#if QT_CONFIG(tooltip)
        self.resample_sb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Gaussian resample filter on the output curves\n"
"Smooth high-frequency noise", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.simplify_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Runs Maya's curve-simplify filter on the output curves", None))
#endif // QT_CONFIG(tooltip)
        self.simplify_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Simplify", None))
#if QT_CONFIG(tooltip)
        self.pre_post_inf_cb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Set pre- and post-infinity to linear, helps with motion blur for first and last frames", None))
#endif // QT_CONFIG(tooltip)
        self.pre_post_inf_cb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"Set Infinity", None))
#if QT_CONFIG(tooltip)
        self.add_dyn_pb.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Run simulation on selected transforms", None))
#endif // QT_CONFIG(tooltip)
        self.add_dyn_pb.setText(QCoreApplication.translate("dyn_motion_tool_mw", u"\U0001f300Add Dynamic Motion", None))
#if QT_CONFIG(tooltip)
        self.progress_bar.setToolTip(QCoreApplication.translate("dyn_motion_tool_mw", u"Scientific fact: looking at a progress bar makes the process faster", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

