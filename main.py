import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QTextEdit,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import fastf1
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class F1LapTimeDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("F1 Lap Time Dashboard")
        self.setGeometry(100, 100, 1400, 900)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QGridLayout(self.main_widget)

        # Dropdowns for year, race, and session
        self.year_combo = QComboBox(self)
        self.year_combo.setFont(QFont('Arial', 12))
        self.year_combo.addItems([str(year) for year in range(2020, 2024)])
        
        self.race_combo = QComboBox(self)
        self.race_combo.setFont(QFont('Arial', 12))
        self.race_combo.addItems(['Monza', 'Spa', 'Silverstone', 'Monaco'])

        self.session_combo = QComboBox(self)
        self.session_combo.setFont(QFont('Arial', 12))
        self.session_combo.addItems(['FP1', 'FP2', 'FP3', 'Q', 'R'])

        self.dropdown_layout = QHBoxLayout()
        self.dropdown_layout.addStretch(1)
        self.dropdown_layout.addWidget(QLabel("Year:", self))
        self.dropdown_layout.addWidget(self.year_combo)
        self.dropdown_layout.addWidget(QLabel("Race:", self))
        self.dropdown_layout.addWidget(self.race_combo)
        self.dropdown_layout.addWidget(QLabel("Session:", self))
        self.dropdown_layout.addWidget(self.session_combo)
        self.dropdown_layout.addStretch(1)
        self.dropdown_widget = QWidget()
        self.dropdown_widget.setLayout(self.dropdown_layout)
        self.layout.addWidget(self.dropdown_widget, 0, 0, 1, 6, alignment=Qt.AlignCenter)

        # Dropdown and buttons
        self.driver_label = QLabel("Select Driver:", self)
        self.driver_label.setFont(QFont('Arial', 14))
        self.layout.addWidget(self.driver_label, 1, 0)

        self.driver_combo = QComboBox(self)
        self.driver_combo.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.driver_combo, 1, 1)

        self.set_graph_button = QPushButton("Set Driver for Graph", self)
        self.set_graph_button.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.set_graph_button, 1, 2)
        self.set_graph_button.clicked.connect(self.update_graph)

        self.more_info_button = QPushButton("More Info for Track", self)
        self.more_info_button.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.more_info_button, 1, 5)
        self.more_info_button.clicked.connect(self.show_more_info)

        # Lap Times List
        self.table_widget = QTableWidget(self)
        self.table_widget.setFont(QFont('Arial', 12))
        self.table_widget.setAlternatingRowColors(True)
        self.layout.addWidget(self.table_widget, 2, 0, 3, 3)

        self.interval_button = QPushButton("Change Interval to Distance from Leader", self)
        self.interval_button.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.interval_button, 5, 0, 1, 3)
        self.interval_button.clicked.connect(self.change_interval)

        # Radio Messages / Track Update
        self.radio_messages = QTextEdit(self)
        self.radio_messages.setFont(QFont('Arial', 12))
        self.radio_messages.setReadOnly(True)
        self.layout.addWidget(self.radio_messages, 4, 3, 2, 3)

        # Lap Time Graph
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, 2, 3, 2, 3)

        self.graph_driver_combo = QComboBox(self)
        self.graph_driver_combo.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.graph_driver_combo, 1, 3, 1, 2)
        self.graph_driver_combo.currentIndexChanged.connect(self.update_graph)

        self.load_stylesheet()
        self.load_drivers()

    def load_stylesheet(self):
        with open("styles.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_drivers(self):
        # Load a session to get the list of drivers
        session = fastf1.get_session(2023, "Monza", "R")
        session.load()
        drivers = session.drivers
        for driver in drivers:
            self.driver_combo.addItem(driver)

    def load_lap_times(self):
        selected_driver = self.driver_combo.currentText()
        session = fastf1.get_session(2023, "Monza", "R")
        session.load()

        driver_laps = session.laps.pick_driver(selected_driver)

        self.table_widget.setRowCount(len(driver_laps))
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Lap Number", "Lap Time"])

        for i, lap in enumerate(driver_laps.iterlaps()):
            lap_number = QTableWidgetItem(str(lap["LapNumber"]))
            lap_time = QTableWidgetItem(str(lap["LapTime"]))
            self.table_widget.setItem(i, 0, lap_number)
            self.table_widget.setItem(i, 1, lap_time)

    def update_graph(self):
        selected_driver = self.driver_combo.currentText()
        session = fastf1.get_session(2023, "Monza", "R")
        session.load()

        driver_laps = session.laps.pick_driver(selected_driver)
        lap_numbers = driver_laps["LapNumber"]
        lap_times = driver_laps["LapTime"].dt.total_seconds()

        self.ax.clear()
        self.ax.plot(lap_numbers, lap_times, marker="o", linestyle="-", color="b")
        self.ax.set_title(f"Lap Times for {selected_driver}")
        self.ax.set_xlabel("Lap Number")
        self.ax.set_ylabel("Lap Time (seconds)")
        self.canvas.draw()

    def change_interval(self):
        # Dummy implementation to change interval to distance from leader
        # This would require more complex logic and integration with FastF1 data
        print("Changing interval to distance from leader...")

    def show_more_info(self):
        # Dummy implementation to show more info for the track
        # This would require additional data and implementation
        print("Showing more info for the track...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = F1LapTimeDashboard()
    window.show()
    sys.exit(app.exec_())


# def get_driver_information(session, driver):
#     driver = session.get_driver(driver)
#     return driver


# def get_drivers_information(session, drivers):
#     drivers_sessions = []
#     for driver in drivers:
#         driver_session = session.get_driver(driver)
#         drivers_sessions.append(driver_session)

#     return drivers_sessions


# def get_session(
#     year,
#     gp,
#     session_identifier,
#     is_laps,
#     is_telemetry,
#     is_weather,
#     is_messages,
#     is_livedata,
# ):
#     gp_session = fastf1.get_session(2021, "Monza", "Q")
#     gp_session.load()
#     return gp_session


# def get_driver_laps(session, driver):
#     return session.laps.pick_driver(driver).reset_index()


# def get_driver_quick_laps(session, driver):
#     return session.laps.pick_driver(driver).pick_quicklaps().reset_index()


# def plot_telemetry(year, gp, session_identifier, drivers):
#     fastf1.plotting.setup_mpl()

#     gp_session = get_session(
#         year, gp, session_identifier, True, True, True, True, False
#     )
#     laps = get_driver_quick_laps(gp_session, "RIC")

#     fig, ax = plt.subplots(figsize=(8, 8))

#     sns.scatterplot(
#         data=laps,
#         x="LapNumber",
#         y="LapTime",
#         ax=ax,
#         hue="Compound",
#         palette=fastf1.plotting.COMPOUND_COLORS,
#         s=80,
#         linewidth=0,
#         legend="auto",
#     )
#     ax.set_xlabel("Lap Number")
#     ax.set_ylabel("Lap Time")

#     # The y-axis increases from bottom to top by default
#     # Since we are plotting time, it makes sense to invert the axis
#     ax.invert_yaxis()
#     plt.suptitle("Alonso Laptimes in the 2023 Azerbaijan Grand Prix")

#     # Turn on major grid lines
#     plt.grid(color="w", which="major", axis="both")
#     sns.despine(left=True, bottom=True)

#     plt.tight_layout()
#     plt.show()


# def run_gui():
#     print("RUNNING GUI (NOT REALLY I HAVEN't MADE IT)")


# def main():
#     run_gui()
#     year = 2019
#     gp = "Monza"
#     session_identifier = "Q"
#     drivers = ["RIC"]
#     plot_telemetry(year, gp, session_identifier, drivers)


# if __name__ == "__main__":
#     main()
