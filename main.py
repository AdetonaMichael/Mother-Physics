#########################################################################################
# importation of modules to be used in the program
import os,sys
import sqlite3
import math
from PySide2 import QtCore
from PySide2.QtCore    import *
from PySide2.QtGui     import *
from PySide2.QtWidgets import *
from PyQt5.QtWidgets   import *
from win10toast import ToastNotifier
from PySide2.QtWebEngineWidgets import *

# importation of the Graphical user interface file (GUI fILE)
from interface import *

# importation of custom widgets to be used in the program
from Custom_Widgets.Widgets import  loadJsonStyle
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
#creating the mainwindow class
class MainWindow(QMainWindow):
    # establishing connection to databse
    db = sqlite3.connect(resource_path('psupport.db'))
    page_id = 0.
    
    #creating cursor object for performing database query
    controller = db.cursor()

    
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.handel_buttons()
        self.navigate()
        self.get_count()
        self.toast = ToastNotifier()
        self.ui.widget_2.load(QUrl('https:/www.google.com'))
        
        #Applying JSON Stylesheet
        loadJsonStyle(self, self.ui)
         
        #displaying the window
        self.show()
        
        # #qstackwidgets naviation 
        self.ui.prev.clicked.connect(lambda: self.ui.stackedWidget.slideToPreviousWidget())
        self.ui.nxt.clicked.connect(lambda: self.ui.stackedWidget.slideToNextWidget())

        self.ui.formula_list_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.formula_list_page))
        self.ui.solved_examples_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.solved_examples_page))
        self.ui.main_note_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page1))
        
        self.ui.home_about.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.solved_examples_page))
        
        # adding animation to the code
        self.ui.stackedWidget.setTransitionDirection(QtCore.Qt.Horizontal)
        self.ui.stackedWidget.setTransitionSpeed(2000)
        self.ui.stackedWidget.setFadeCurve(QtCore.QEasingCurve.InSine)
        self.ui.stackedWidget.setSlideTransition(True)
        
    #fucntion for managing myown buttons
    def handel_buttons(self):
        self.ui.next_note.clicked.connect(self.next_page)
        self.ui.prev_note.clicked.connect(self.prev_page)
        self.ui.update_update_btn.clicked.connect(self.update)
        self.ui.update_delete_btn.clicked.connect(self.delete)
        self.ui.update_add_btn.clicked.connect(self.add)
        self.ui.update_refresh_btn.clicked.connect(self.refresh)
        self.ui.btn_go.clicked.connect(self.set_url)
        self.ui.convert_button.clicked.connect(self.converter)

    def converter(self):
        try:
            unit1 = self.ui.convert_combo1.currentData()
            unit2 = self.ui.convert_combo2.currentData
            num1 =  self.ui.convert_from_input.text()
            if unit1 == "cm" and unit2 == "m":
                ans = float(num1)/100
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "mm" and unit2 == "cm":
                ans = float(num1)/10
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "m" and unit2 == "cm":
                ans = float(num1)*100
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "cm" and unit2 == "mm":
                ans = float(num1)*10
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "mm" and unit2 == "m":
                ans = float(num1)/1000
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "m" and unit2 == "mm":
                ans = float(num1)*1000
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "km" and unit2 == "m":
                ans = float(num1)*1000
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "m" and unit2 == "km":
                ans = float(num1)/1000
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "mm" and unit2 == "km":
                ans = float(num1)/1000000
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "ft" and unit2 == "cm":
                ans = float(num1)*30.48
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "ft" and unit2 == "mm":
                ans = float(num1)*304.8
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "ft" and unit2 == "inch":
                ans = float(num1)*12
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "inch" and unit2 == "cm":
                ans = float(num1)*2.54
                self.ui.convert_answer.setText(str(ans))
            elif unit1 == "inch" and unit2 == "mm":
                ans = float(num1)*25.4
                self.ui.convert_answer.setText(str(ans))
        except:
            self.ui.convert_answer.setText('Ooops! This Option Does not exist...')


      #function to pull all data from database
    def pullData(self):
       sql = "SELECT * FROM notes where id = %d"%(MainWindow.page_id)
       MainWindow.controller.execute(sql)
       result = MainWindow.controller.fetchone()
       self.ui.note1_label.setText(str(result[2])) 
       self.ui.note_content.insertPlainText (str(result[1]))
       
    #creting function to connect to next page
    def next_page(self):
        try:
            next_id = MainWindow.page_id
            sql = "SELECT * FROM notes WHERE id=%d"%(next_id)
            MainWindow.controller.execute(sql)
            result = MainWindow.controller.fetchone()
            self.ui.single_count_btn.setText(str(result[0]))
            self.ui.note1_label.setText(str(result[2])) 
            self.ui.note_content.setText (str(result[1]))
            MainWindow.page_id += 1
        except:
            MainWindow.page_id += 1
            next_id = MainWindow.page_id
            sql = "SELECT * FROM notes WHERE id=%d"%(next_id)
            MainWindow.controller.execute(sql)
            result = MainWindow.controller.fetchone()
            self.ui.single_count_btn.setText(str(result[0]))
            self.ui.note1_label.setText(str(result[2])) 
            self.ui.note_content.setText (str(result[1]))
            MainWindow.page_id += 1 
                
    def prev_page(self):
        try:
            prev_id = MainWindow.page_id-1
            sql = "SELECT * FROM notes WHERE id=%d"%(prev_id)
            MainWindow.controller.execute(sql)
            result = MainWindow.controller.fetchone()
            self.ui.single_count_btn.setText(str(result[0]))
            self.ui.note1_label.setText(str(result[2])) 
            self.ui.note_content.setText (str(result[1]))
            MainWindow.page_id = prev_id
        except:
            prev_id = MainWindow.page_id-1
            sql = "SELECT * FROM notes WHERE id=%d"%(prev_id)
            MainWindow.controller.execute(sql)
            result = MainWindow.controller.fetchone()
            self.ui.single_count_btn.setText(str(result[0]))
            self.ui.note1_label.setText(str(result[2])) 
            self.ui.note_content.setText (str(result[1]))
            MainWindow.page_id = prev_id
                       
    def get_count(self):
        sql = "SELECT COUNT(*) FROM notes"
        MainWindow.controller.execute(sql)
        result = MainWindow.controller.fetchall() 
        self.ui.total_count_btn.setText(str(result[0][0]))
        main_result = result[0][0]
        return main_result   
    
    def navigate(self):
        sql = 'SELECT * FROM notes'
        result = MainWindow.controller.execute(sql)
        result = MainWindow.controller.fetchone()
        
        #defining and the widget in the textbox interface
        self.ui.update_count_label.setText(str(result[0]))
        self.ui.update_note_title.setText(str(result[2]))
        self.ui.update_note_content.setText(str(result[1]))
        
    def refresh(self):
        try:
            id     = int(self.ui.update_count_label.text())
            sql    = 'SELECT * FROM notes where id=%d'%(id)
            result = MainWindow.controller.execute(sql)
            result = MainWindow.controller.fetchone()
            
            #defining and the widget in the textbox interface
            self.ui.update_count_label.setText(str(result[0]))
            self.ui.update_note_title.setText(str(result[2]))
            self.ui.update_note_content.setText(str(result[1]))
        except:
            self.ui.update_note_content.setText("OooPs!... \n No Content Exist For Record with Id of {}".format(id))
            self.toast.show_toast(title="MOTHER PHYSICS V1.0", msg="Database Refresh Successful", icon_path="icons/atom.ico", threaded=True)
            
            

    # creating function to add data into the database
    def add(self):
        try:
            id_             = int(self.ui.update_count_label.text())
            title_          = str(self.ui.update_note_title.text())
            content_        = str(self.ui.update_note_content.toHtml())
            row = (id_, content_, title_)
            sql = '''INSERT INTO notes(id, content, title) VALUES(?,?,?)'''
            MainWindow.controller.execute(sql,row)
            MainWindow.db.commit()
        except:
            self.ui.update_note_content.setText("An Error Occured While Trying to Add Data to the database \n Record Not Inserted to Database...")
        else:
            self.ui.update_note_content.setText("Record Added To Database Successfully!.. \n Click the Refresh Button To Continue ==>")
            self.toast.show_toast(title="MOTHER PHYSICS V1.0", msg="Record Successfully Added To The Database", icon_path="icons/atom.ico", threaded=True)
            
        
    
    def update(self):
        try:
            #defining and the widget in the textbox interface
            id              = int(self.ui.update_count_label.text())
            title_          = str(self.ui.update_note_title.text())
            content_        = str(self.ui.update_note_content.toHtml())
            
            row = (content_, title_, id)
            sql = '''UPDATE notes SET content=?,  title=? where id = ?'''
            MainWindow.controller.execute(sql,row)
            MainWindow.db.commit()
        except:
            self.ui.update_note_content.setText("There Was An Error While Trying to Update Database Content")
        else:
            self.ui.update_note_content.setText("Database Update Was Successful... \n Click Refresh Button to Continue ==>")
            self.toast.show_toast(title="MOTHER PHYSICS V1.0", msg="Update To The Database Was Successful", icon_path="icons/atom.ico", threaded=True)
            
    
    def delete(self):
        try:
            d =int(self.ui.update_count_label.text())
            sql = 'DELETE FROM notes where id=%d'%(d)
            MainWindow.controller.execute(sql)
            MainWindow.db.commit()
        except:
            self.ui.update_note_content.setText("Unable To Delete Database Record")
        else:
            self.ui.update_note_content.setText("Record Deleted Successfully... \n Click Refresh Button to Continue ==>")
            self.toast.show_toast(title="MOTHER PHYSICS V1.0", msg="Database Record Deleted Successfully!", icon_path="icons/atom.ico", threaded=True)
    def set_url(self):
        the_url = self.ui.browser_input.text()
        self.ui.widget_2.load(QUrl(the_url))
        self.ui.stackedWidget.setCurrentWidget(self.ui.formula_list_page)
   
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # web = QWebEngineView()
    # web.load(QUrl('https://thegeonerds.com'))
    # web.show()
    # web1 = QWebEngineView()
    # web1.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # web1.load(QUrl('formula.pdf'))
    # web1.show()
    sys.exit(app.exec_())
        
#executing the application 
if __name__ == "__main__":
    main()
   
    