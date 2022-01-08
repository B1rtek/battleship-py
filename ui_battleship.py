# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'battleship.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Battleship(object):
    def setupUi(self, Battleship):
        if not Battleship.objectName():
            Battleship.setObjectName(u"Battleship")
        Battleship.resize(528, 512)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Battleship.sizePolicy().hasHeightForWidth())
        Battleship.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(Battleship)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setMaximumSize(QSize(782, 562))
        self.page_main_menu = QWidget()
        self.page_main_menu.setObjectName(u"page_main_menu")
        self.verticalLayout_3 = QVBoxLayout(self.page_main_menu)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_title = QLabel(self.page_main_menu)
        self.label_title.setObjectName(u"label_title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(24)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_title, 0, Qt.AlignVCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.button_main_play = QPushButton(self.page_main_menu)
        self.button_main_play.setObjectName(u"button_main_play")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_main_play.sizePolicy().hasHeightForWidth())
        self.button_main_play.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.button_main_play, 0, Qt.AlignHCenter)

        self.button_main_htp = QPushButton(self.page_main_menu)
        self.button_main_htp.setObjectName(u"button_main_htp")
        sizePolicy3.setHeightForWidth(self.button_main_htp.sizePolicy().hasHeightForWidth())
        self.button_main_htp.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.button_main_htp, 0, Qt.AlignHCenter)

        self.button_main_quit = QPushButton(self.page_main_menu)
        self.button_main_quit.setObjectName(u"button_main_quit")
        sizePolicy3.setHeightForWidth(self.button_main_quit.sizePolicy().hasHeightForWidth())
        self.button_main_quit.setSizePolicy(sizePolicy3)

        self.verticalLayout_2.addWidget(self.button_main_quit, 0, Qt.AlignHCenter)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.stackedWidget.addWidget(self.page_main_menu)
        self.page_fleet_creator = QWidget()
        self.page_fleet_creator.setObjectName(u"page_fleet_creator")
        self.verticalLayout = QVBoxLayout(self.page_fleet_creator)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_setup_title = QLabel(self.page_fleet_creator)
        self.label_setup_title.setObjectName(u"label_setup_title")
        sizePolicy2.setHeightForWidth(self.label_setup_title.sizePolicy().hasHeightForWidth())
        self.label_setup_title.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(16)
        self.label_setup_title.setFont(font1)

        self.verticalLayout.addWidget(self.label_setup_title, 0, Qt.AlignHCenter)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_setup_exit = QPushButton(self.page_fleet_creator)
        self.button_setup_exit.setObjectName(u"button_setup_exit")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.button_setup_exit.sizePolicy().hasHeightForWidth())
        self.button_setup_exit.setSizePolicy(sizePolicy4)

        self.horizontalLayout_4.addWidget(self.button_setup_exit)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.grid_setup_board = QGridLayout()
        self.grid_setup_board.setSpacing(0)
        self.grid_setup_board.setObjectName(u"grid_setup_board")

        self.horizontalLayout.addLayout(self.grid_setup_board)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.button_setup_rand = QPushButton(self.page_fleet_creator)
        self.button_setup_rand.setObjectName(u"button_setup_rand")
        sizePolicy4.setHeightForWidth(self.button_setup_rand.sizePolicy().hasHeightForWidth())
        self.button_setup_rand.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.button_setup_rand)

        self.button_setup_rot = QPushButton(self.page_fleet_creator)
        self.button_setup_rot.setObjectName(u"button_setup_rot")

        self.horizontalLayout_3.addWidget(self.button_setup_rot)

        self.button_setup_done = QPushButton(self.page_fleet_creator)
        self.button_setup_done.setObjectName(u"button_setup_done")

        self.horizontalLayout_3.addWidget(self.button_setup_done)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.stackedWidget.addWidget(self.page_fleet_creator)
        self.page_game = QWidget()
        self.page_game.setObjectName(u"page_game")
        self.horizontalLayout_15 = QHBoxLayout(self.page_game)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.button_game_main = QPushButton(self.page_game)
        self.button_game_main.setObjectName(u"button_game_main")

        self.horizontalLayout_14.addWidget(self.button_game_main)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_20)


        self.verticalLayout_13.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_18)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_8)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)

        self.grid_game_player_board = QGridLayout()
        self.grid_game_player_board.setSpacing(0)
        self.grid_game_player_board.setObjectName(u"grid_game_player_board")

        self.horizontalLayout_8.addLayout(self.grid_game_player_board)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_11)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_9)


        self.verticalLayout_10.addLayout(self.verticalLayout_6)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_14)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_16)

        self.grid_game_player_fleet = QGridLayout()
        self.grid_game_player_fleet.setSpacing(0)
        self.grid_game_player_fleet.setObjectName(u"grid_game_player_fleet")

        self.horizontalLayout_11.addLayout(self.grid_game_player_fleet)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_17)


        self.verticalLayout_9.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_15 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_15)


        self.verticalLayout_10.addLayout(self.verticalLayout_9)


        self.horizontalLayout_12.addLayout(self.verticalLayout_10)

        self.line = QFrame(self.page_game)
        self.line.setObjectName(u"line")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy5)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_12.addWidget(self.line)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_10)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_12)

        self.grid_game_enemy_board = QGridLayout()
        self.grid_game_enemy_board.setSpacing(0)
        self.grid_game_enemy_board.setObjectName(u"grid_game_enemy_board")

        self.horizontalLayout_9.addLayout(self.grid_game_enemy_board)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_13)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_11)


        self.verticalLayout_11.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_12 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_12)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_15)

        self.grid_game_enemy_fleet = QGridLayout()
        self.grid_game_enemy_fleet.setSpacing(0)
        self.grid_game_enemy_fleet.setObjectName(u"grid_game_enemy_fleet")

        self.horizontalLayout_10.addLayout(self.grid_game_enemy_fleet)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_14)


        self.verticalLayout_8.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_13)


        self.verticalLayout_11.addLayout(self.verticalLayout_8)


        self.horizontalLayout_12.addLayout(self.verticalLayout_11)


        self.verticalLayout_12.addLayout(self.horizontalLayout_12)

        self.game_plain_text_edit_log = QPlainTextEdit(self.page_game)
        self.game_plain_text_edit_log.setObjectName(u"game_plain_text_edit_log")
        self.game_plain_text_edit_log.setAcceptDrops(False)
        self.game_plain_text_edit_log.setInputMethodHints(Qt.ImhNone)
        self.game_plain_text_edit_log.setFrameShape(QFrame.StyledPanel)
        self.game_plain_text_edit_log.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.game_plain_text_edit_log.setUndoRedoEnabled(False)
        self.game_plain_text_edit_log.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.game_plain_text_edit_log.setReadOnly(True)
        self.game_plain_text_edit_log.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout_12.addWidget(self.game_plain_text_edit_log)

        self.verticalLayout_12.setStretch(0, 3)
        self.verticalLayout_12.setStretch(1, 1)

        self.horizontalLayout_13.addLayout(self.verticalLayout_12)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_19)


        self.verticalLayout_13.addLayout(self.horizontalLayout_13)


        self.horizontalLayout_15.addLayout(self.verticalLayout_13)

        self.stackedWidget.addWidget(self.page_game)
        self.page_htp = QWidget()
        self.page_htp.setObjectName(u"page_htp")
        self.verticalLayout_5 = QVBoxLayout(self.page_htp)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_htp_title = QLabel(self.page_htp)
        self.label_htp_title.setObjectName(u"label_htp_title")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_htp_title.sizePolicy().hasHeightForWidth())
        self.label_htp_title.setSizePolicy(sizePolicy6)
        self.label_htp_title.setFont(font)

        self.verticalLayout_4.addWidget(self.label_htp_title, 0, Qt.AlignHCenter)

        self.label_htp_tutorial = QLabel(self.page_htp)
        self.label_htp_tutorial.setObjectName(u"label_htp_tutorial")
        sizePolicy1.setHeightForWidth(self.label_htp_tutorial.sizePolicy().hasHeightForWidth())
        self.label_htp_tutorial.setSizePolicy(sizePolicy1)
        self.label_htp_tutorial.setAlignment(Qt.AlignJustify|Qt.AlignTop)
        self.label_htp_tutorial.setWordWrap(True)
        self.label_htp_tutorial.setMargin(5)

        self.verticalLayout_4.addWidget(self.label_htp_tutorial)

        self.button_htp_back = QPushButton(self.page_htp)
        self.button_htp_back.setObjectName(u"button_htp_back")

        self.verticalLayout_4.addWidget(self.button_htp_back, 0, Qt.AlignHCenter)


        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_7)

        self.stackedWidget.addWidget(self.page_htp)

        self.horizontalLayout_2.addWidget(self.stackedWidget)

        Battleship.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Battleship)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 528, 21))
        Battleship.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Battleship)
        self.statusbar.setObjectName(u"statusbar")
        Battleship.setStatusBar(self.statusbar)

        self.retranslateUi(Battleship)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Battleship)
    # setupUi

    def retranslateUi(self, Battleship):
        Battleship.setWindowTitle(QCoreApplication.translate("Battleship", u"Battleship", None))
        self.label_title.setText(QCoreApplication.translate("Battleship", u"Battleship", None))
        self.button_main_play.setText(QCoreApplication.translate("Battleship", u"Play", None))
        self.button_main_htp.setText(QCoreApplication.translate("Battleship", u"Help", None))
        self.button_main_quit.setText(QCoreApplication.translate("Battleship", u"Quit", None))
        self.label_setup_title.setText(QCoreApplication.translate("Battleship", u"Set up your fleet", None))
        self.button_setup_exit.setText(QCoreApplication.translate("Battleship", u"Back", None))
        self.button_setup_rand.setText(QCoreApplication.translate("Battleship", u"Generate random", None))
        self.button_setup_rot.setText(QCoreApplication.translate("Battleship", u"Rotate", None))
        self.button_setup_done.setText(QCoreApplication.translate("Battleship", u"Done", None))
        self.button_game_main.setText(QCoreApplication.translate("Battleship", u"Main Menu", None))
        self.label_htp_title.setText(QCoreApplication.translate("Battleship", u"How to play", None))
        self.label_htp_tutorial.setText(QCoreApplication.translate("Battleship", u"The goal of the game is to destroy your enemy's fleet.\n"
"But first, in order to fight them, you need your own fleet - which you prepare on the setup page.\n"
"In there, you can see your fleet, and three buttons which you can use to move the ships around. First, you select a ship by clicking on it. To move it to a new location, click any other empty field, and if there is enough space for that ship there, it will be moved. The field on which you click will contain the left upmost segment of the ship you moved. To rotate the selected ship, press the \"Rotate\" button. To generate a new random fleet, press the \"Generate random\" button. When you're done setting up your fleet, press \"Done\" to start the game.\n"
"The game screen consists of two boards and two sets of fleet displays, and a message log, where you can see what has been happening in the last few moves. To shoot at a certain field, click on it with the left mouse button, to mark or unmark that field, click on it with the right mouse button. The ene"
                        "my will move every one second when it's their turn. The player who first destroys the rival's fleet wins. Good luck!", None))
        self.button_htp_back.setText(QCoreApplication.translate("Battleship", u"Back", None))
    # retranslateUi

