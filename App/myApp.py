import sys
import psycopg2
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap

qtCreatorFile = "MyUI.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class myApp(QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipcodeList.itemSelectionChanged.connect(self.zipcodeChanged)
        self.ui.applyButton.clicked.connect(self.apply)
        self.ui.clearButton.clicked.connect(self.clear)
        self.ui.refreshButton.clicked.connect(self.refresh)

    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password=''")
        except:
            print('Unable to connect!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query failed!")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if(self.ui.stateList.currentIndex()>=0):
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query failed!")

    def cityChanged(self):
        self.ui.zipcodeList.clear()
        city = self.ui.cityList.selectedItems()[0].text()
        if(len(self.ui.cityList.selectedItems())>0):
            sql_str = "SELECT distinct postal_code FROM business WHERE city ='" + city + "' ORDER BY postal_code;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.zipcodeList.addItem(row[0])
            except:
                print("Query failed!")
    
    def zipcodeChanged(self):
        city = self.ui.cityList.selectedItems()[0].text()
        if (self.ui.zipcodeList.selectedItems()):
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()

            self.ui.categoryList.clear()
            sql_str = "SELECT distinct category FROM business WHERE city = '" + city + "' AND postal_code='" + zipcode + "' ORDER BY category;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.categoryList.addItem(row[0])
            except:
                print("Query failed!")

            sql_str = "SELECT name, address, city, reviewrating, review_count, numcheckins FROM business WHERE city = '" + city + "' AND postal_code='" + zipcode + "' ORDER BY name;"
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3;}"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Reviews', 'Check-Ins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 200)
                self.ui.businessTable.setColumnWidth(1, 200)
                self.ui.businessTable.setColumnWidth(2, 100)
                currentRowCount = 0

                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Zipcode Changed Query failed!")

            sql_str = "SELECT COUNT(name) FROM business WHERE postal_code = '" + str(zipcode) + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.numBusinesses.setText(str(results[0][0]))
            except:
                print("Display # of business Query failed!")

            sql_str = "SELECT population FROM zipcodeData WHERE zipcode = '" + str(zipcode) + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.population.setText(str(results[0][0]))
            except:
                print("Display population Query failed!")

            sql_str = "SELECT meanincome FROM zipcodeData WHERE zipcode = '" + str(zipcode) + "';"
            try:
                results = self.executeQuery(sql_str)
                self.ui.income.setText(str(results[0][0]))
            except:
                print("Display mean income Query failed!")

            sql_str = "SELECT COUNT(category) as temp, category distinct FROM business WHERE postal_code = '" + str(zipcode) + "' GROUP BY category ORDER BY temp DESC;"
            for i in reversed(range(self.ui.categoryTable.rowCount())):
                self.ui.categoryTable.removeRow(i)
            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3;}"
                self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
                self.ui.categoryTable.setColumnCount(len(results[0]))
                self.ui.categoryTable.setRowCount(len(results))
                self.ui.categoryTable.setHorizontalHeaderLabels(['# of Businesses', 'Category'])
                self.ui.categoryTable.resizeColumnsToContents()
                self.ui.categoryTable.setColumnWidth(1, 200)
                currentRowCount = 0

                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.categoryTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Zipcode Changed Query failed!")
    
    def apply(self):
        city = self.ui.cityList.selectedItems()[0].text()
        if (self.ui.zipcodeList.selectedItems()):
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()
            if (self.ui.categoryList.selectedItems()):
                category = self.ui.categoryList.selectedItems()[0].text()

                sql_str = "SELECT name, address, city, reviewrating, review_count, numcheckins FROM business WHERE city = '" + city + "' AND postal_code='" + zipcode + "' AND category='" + category + "' ORDER BY name;"
                for i in reversed(range(self.ui.businessTable.rowCount())):
                    self.ui.businessTable.removeRow(i)

                try:
                    results = self.executeQuery(sql_str)
                    style = "::section {""background-color: #f3f3f3;}"
                    self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable.setColumnCount(len(results[0]))
                    self.ui.businessTable.setRowCount(len(results))
                    self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Reviews', 'Check-Ins'])
                    self.ui.businessTable.resizeColumnsToContents()
                    self.ui.businessTable.setColumnWidth(0, 200)
                    self.ui.businessTable.setColumnWidth(1, 200)
                    self.ui.businessTable.setColumnWidth(2, 100)
                    currentRowCount = 0

                    for row in results:
                        for colCount in range(0, len(results[0])):
                            self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    
                except:
                    print("Apply Query failed!")

    def clear(self):
        self.zipcodeChanged()

    def refresh(self):
        city = self.ui.cityList.selectedItems()[0].text()
        if (self.ui.zipcodeList.selectedItems()):
            zipcode = self.ui.zipcodeList.selectedItems()[0].text()

            sql_str = "SELECT name, numcheckins FROM business WHERE city = '" + city + "' AND postal_code='" + zipcode + "' ORDER BY numcheckins DESC;"
            for i in reversed(range(self.ui.popularTable.rowCount())):
                self.ui.popularTable.removeRow(i)

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3;}"
                self.ui.popularTable.horizontalHeader().setStyleSheet(style)
                self.ui.popularTable.setColumnCount(len(results[0]))
                self.ui.popularTable.setRowCount(len(results))
                self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', 'Check-Ins'])
                self.ui.popularTable.resizeColumnsToContents()
                self.ui.popularTable.setColumnWidth(0, 350)
                currentRowCount = 0

                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.popularTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Refresh Query failed!")

            sql_str = "SELECT name, reviewrating, review_count FROM business WHERE city = '" + city + "' AND postal_code='" + zipcode + "' ORDER BY reviewrating DESC;"
            for i in reversed(range(self.ui.successfulTable.rowCount())):
                self.ui.successfulTable.removeRow(i)

            try:
                results = self.executeQuery(sql_str)
                style = "::section {""background-color: #f3f3f3;}"
                self.ui.successfulTable.horizontalHeader().setStyleSheet(style)
                self.ui.successfulTable.setColumnCount(len(results[0]))
                self.ui.successfulTable.setRowCount(len(results))
                self.ui.successfulTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Reviews'])
                self.ui.successfulTable.resizeColumnsToContents()
                self.ui.successfulTable.setColumnWidth(0, 275)
                self.ui.successfulTable.setColumnWidth(1, 75)
                currentRowCount = 0

                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.successfulTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Refresh Query failed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(app.exec_())
