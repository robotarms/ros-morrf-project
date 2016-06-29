import sys
import rospy

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from image_window import Image
from image_window import Image

from morrf_ros.msg import *
import cv2
import numpy as np
import json

from error_popup.not_initialized import NotInitialized
from error_popup.no_image_selected import NoImage

from publishers.image_publisher import StartImagePublisher
from publishers.commander_publisher import StartCommanderPublisher
from publishers.costmap_publisher import StartCostmapPublisher

STARTX = 1000
STARTY = 1000
WIDTH = 250
HEIGHT = 700

class Config(QtGui.QMainWindow):

    def __init__(self):
        super(Config, self).__init__()
        self.setGeometry(STARTX, STARTY, WIDTH, HEIGHT)
        self.setWindowTitle("Config")

        self.image_load = QtGui.QAction("Load Image", self)
        self.image_load.triggered.connect(self.load_image)
        self.appQuit = QtGui.QAction("Quit", self)
        self.appQuit.triggered.connect(qApp.quit)

        main_menu = self.menuBar()

        load_menu = main_menu.addMenu('&File')
        load_menu.addAction(self.image_load)
        load_menu.addAction(self.appQuit)


        launch_button = QtGui.QPushButton("Launch MORRF", self)
        launch_button.resize(250, 50)
        launch_button.clicked.connect(self.launch_morrf)

        self.pick_paths = QtGui.QPushButton("Pick path", self)
        self.pick_paths.resize(250, 50)
        self.pick_paths.clicked.connect(self.sendToPathPicker)
        self.pick_paths.setEnabled(False)

        self.iterations = QtGui.QLineEdit()
        self.iterations.setFrame(True)
        self.iterations.setMaxLength(4)
        self.iterations.setText("500")

        self.tree_number = QtGui.QLineEdit()
        self.tree_number.setFrame(True)
        self.tree_number.setMaxLength(4)
        self.tree_number.setText("5")

        self.segment_length = QtGui.QLineEdit()
        self.segment_length.setFrame(True)
        self.segment_length.setMaxLength(4)
        self.segment_length.setText("5")

        self.objective_number = QtGui.QLineEdit()
        self.objective_number.setFrame(True)
        self.objective_number.setMaxLength(4)
        self.objective_number.setText("1")

        self.method_box = QtGui.QComboBox()
        self.method_box.addItem("Weighted Sum")
        self.method_box.addItem("Tchebycheff")
        self.method_box.addItem("Boundary Intersection")

        self.min_distance = QtGui.QCheckBox("", self)
        self.min_distance.setChecked(True)

        self.stealth = QtGui.QCheckBox("", self)
        self.stealth.setChecked(False)

        self.safe = QtGui.QCheckBox("", self)
        self.safe.setChecked(False)

        layout = QtGui.QFormLayout()
        layout.addRow("# Of Iterations", self.iterations)
        layout.addRow("# Of Trees", self.tree_number)
        layout.addRow("Segment Length", self.segment_length)
        layout.addRow("Stealthy", self.stealth)
        layout.addRow("Safely", self.safe)
        layout.addRow("Quickly", self.min_distance)
        layout.addRow("Method Type", self.method_box)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(launch_button)
        main_layout.addWidget(self.pick_paths)

        self.win = QtGui.QWidget(self)
        self.win.setLayout(main_layout)

        self.setCentralWidget(self.win)
        self.show()

    def launch_morrf(self):
        if not hasattr(self, "image_window"):
            self.error = NoImage()

        elif self.is_completed() and self.image_window.isCompleted():

            #Deinitializing variable to prevent errors
            self.image_window.delMorrfPaths()

            initializer = morrf_init()

            goal = self.image_window.getGoalPoint()
            start = self.image_window.getStartPoint()

            initializer.goal.x = goal[0]
            initializer.goal.y = goal[1]
            initializer.start.x = start[0]
            initializer.start.y = start[1]
            initializer.number_of_iterations = int(self.iterations.text())
            initializer.segment_length = int(self.segment_length.text())
            initializer.number_of_trees = int(self.tree_number.text())
            initializer.objective_number = int(self.getObjectiveNumbers())
            initializer.minimum_distance_enabled = self.min_distance.isChecked()
            initializer.method_type = int(self.getMethodType())
            initializer.map = self.map_convert()
            initializer.width = initializer.map.width
            initializer.height = initializer.map.height

            self.costmap_response = StartCostmapPublisher(initializer.map, self.stealth.isChecked(), self.safe.isChecked(), self.image_window.getEnemyLocations())

            initializer.cost_maps = self.costmap_response.cost_maps

            self.morrf_response = StartCommanderPublisher(initializer)

            self.image_window.printMorrfPaths(self.morrf_response)
            self.pick_paths.setEnabled(True)

        else:
            self.error = NotInitialized()

    def sendToPathPicker(self):
        print "Sending to path palette"

        self.outputToDropbox(self.morrf_response)

    def saveBoundImage(self, image):

        test = QImage(image.width, image.height, QImage.Format_RGB16)

        for i in range(image.height):
            for j in range(image.width):

                index = i * image.width + j
                color = image.int_array[index]

                qrgb = QColor(color, color, color)

                test.setPixel(j, i, qrgb.rgb())

        test.save("/home/wfearn/Dropbox/MORRF_OUTPUT/maps/boundary.png")


    def getObjectiveNumbers(self):

        counter = 0

        if self.stealth.isChecked():
            counter +=1

        if self.safe.isChecked():
            counter += 1

        if self.min_distance.isChecked():
            counter +=1

        return counter

    def getMethodType(self):
        if self.method_box.currentText() == "Weighted Sum":
            return 0
        elif self.method_box.currentText() == "Tchebycheff":
            return 1
        else:
            return 2

    def is_completed(self):
        if self.iterations.text() == "":
            return False
        elif self.tree_number.text() == "":
            return False
        elif self.segment_length.text() == "":
            return False
        elif self.objective_number.text() == "":
            return False
        else:
            return True

    def load_image(self):
        self.image_name = QtGui.QFileDialog.getOpenFileName(self, "Load Image")
        self.image_window = Image(self.image_name)

    def map_convert(self):
        if hasattr(self, "image_name"):
            image = int16_image()

            img = cv2.imread(str(self.image_name))

            image.width = img.shape[1]
            image.height = img.shape[0]
            image.name = str(self.image_name)

            for j in range(image.height):
                for i in range(image.width):
                    image.int_array.append(np.int16(img[j,i,0]))

            return image
        else:
            return None


    def contextMenuRequested(self, point):
        pass

    def outputToDropbox(self, morrf_output):

        self.image_window.saveMapToDropbox()
        self.saveBoundImage(self.costmap_response.boundary_image)

        morrf_output_path = "/home/wfearn/Dropbox/MORRF_OUTPUT/morrf_output/morrf_output.txt"
        map_output_path = "/home/wfearn/Dropbox/MORRF_OUTPUT/maps/%s" % self.image_window.getMapName()
        start = self.image_window.getStartPoint()
        goal = self.image_window.getGoalPoint()

        json_output = {}

        json_output["enemies"] = []
        for pos in self.image_window.getEnemyLocations():
            json_output["enemies"].append(str(pos.x) + "," + str(pos.y))

        json_output["start"] = str(start[0]) + "," + str(start[1])
        json_output["goal"] = str(goal[0]) + "," + str(goal[1])

        #Making file path concise for retrieval from other computer
        path_array = morrf_output_path.split("/")
        json_output["morrf_output"] = path_array[4] + "/" + path_array[5] + "/" + path_array[6]

        waypoint_output = []
        cost_output = []

        for index in range(len(morrf_output.paths)):
            waypoint_output.append([])
            cost_output.append([])

            for point in morrf_output.paths[index].waypoints:
                waypoint_output[index].append(point)

            for cost in morrf_output.paths[index].cost:
                cost_output[index].append(cost)

        print waypoint_output
        print cost_output
        print json.dumps(json_output)

        f = open("/home/wfearn/Dropbox/MORRF_OUTPUT/morrf_output/output_values.txt", "w")

        for i in range(len(self.costmap_response.cost_values)):

            cv = self.costmap_response.cost_values[i]
            for j in range(len(cv.vals)):

                f.write("%s %s\t%s\n" % (cv.vals[j].position.x, cv.vals[j].position.y, cv.vals[j].cost))


       # for path in cost_output:
       #     for cost in path:
       #         f.write(str(cost.data) + " ")

       #     f.write("\n")

       # for path in waypoint_output:
       #     for point in path:
       #         f.write(str(point.x) + " " + str(point.y) + " ")
       #     f.write("\n")

        f.close()
