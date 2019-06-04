import sys,sqlite3
from PyQt5 import QtWidgets , QtGui
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget,QPushButton,QApplication,QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtGui import QIcon , QPixmap
from PyQt5.QtWidgets import (QDialog,QApplication,QMainWindow,QWidget,QTableWidgetItem,QTableWidget,QCheckBox,QGridLayout,QGroupBox,QMenu,QPushButton,QRadioButton, QVBoxLayout,QWidget,QLabel,QLineEdit,QHBoxLayout)

class sims_app():
	def __init__(self):
		self.conn = sqlite3.connect('sims.db')
		self.c = self.conn.cursor()
		self.c.execute("""CREATE TABLE IF NOT EXISTS students(roll INTEGER,name TEXT,
			gender INTEGER, department INTEGER, year INTEGER, batch INTEGER, address TEXT,
			mobile INTEGER, gpa REAL, attendance REAL)""")

	def addStudent(self,roll,name,gender,department,year,batch,address,mobile,gpa,attendance):
		try:
			self.c.execute("INSERT INTO students(roll,name,gender,department,year,batch,address,mobile,gpa,attendance) VALUES (?,?,?,?,?,?,?,?,?,?)",(roll,name,gender,department,year,batch,address,mobile,gpa,attendance))
			self.conn.commit()
			self.c.close()
			self.conn.close()
			QMessageBox.information(QMessageBox(),'Successful','Student is added successfully to the database.')
		except Exception:
			QMessageBox.warning(QMessageBox(),'Error','Could not add Student to database.')

	def searchStudent(self,roll):

		self.c.execute("SELECT * from students WHERE roll ="+str(roll))
		self.data=self.c.fetchone()

		if not self.data:
			QMessageBox.warning(QMessageBox(),'Error','Could not find any student with roll no',+str(roll))
			return None

		self.list=[]
		for i in range(0,10):
			self.list.append(self.data[i])
		self.c.close()
		self.conn.close()

		showStudent(self.list)

class Login(QDialog):
	def __init__(self, parent=None):
		super(Login,self).__init__(parent)
		self.QPixmap=QLabel(self)
		self.QPixmap.resize(400,500)
		self.QPixmap.setPixmap(QtGui.QPixmap("bbg.jpeg"))
		

		self.setStyleSheet(" colour: black ; font-size: 13pt ; font-family: arial")
		
		self.userNameLabel=QLabel("Username")
		self.userPassLabel=QLabel("Password")
		self.textName=QLineEdit(self)
		self.textName.setStyleSheet(" colour: black ; font-size: 11pt ; font-family: arial")
		self.textPass=QLineEdit(self)
		self.textPass.setStyleSheet(" colour: black ; font-size: 11pt ; font-family: arial")
		self.textPass.setEchoMode(QLineEdit.Password)
		
		self.buttonLogin=QPushButton('Login',self)
		self.buttonLogin.setStyleSheet("background:teal; colour: white ; font-size: 13pt ; font-family: arial")
		self.buttonLogin.clicked.connect(self.handleLogin)
		
		layout=QGridLayout(self)
		layout.addWidget(self.userNameLabel,2,1)
		layout.addWidget(self.userPassLabel,3,1)
		layout.addWidget(self.textName,2,2)
		layout.addWidget(self.textPass,3,2)
		layout.addWidget(self.buttonLogin,4,1,1,2)
		self.resize(370,150)

		self.setWindowTitle("Login")
		self.setWindowIcon(QtGui.QIcon("user.png"))

	def handleLogin(self):
		if (self.textName.text() == 'admin'
		 and self.textPass.text() == 'admin'):
			self.accept()
		else:
			QMessageBox.warning(self,'Error','Wrong User or Password')

def showStudent(list):
	roll=0
	name=""
	gender=""
	department=""
	year=""
	batch=-1
	address=""
	mobile=-1
	gpa=0
	attendance=0

	roll=list[0]
	name=list[1]

	if list[2]==0:
		gender="Male"
	else:
		gender="Female"

	if list[3]==0:
		department="Computer Systems Engineering"
	else:
		department="Electrical Engineering"

	if list[4]==0:
		year="1st"
	elif list[4]==1:
		year="2nd"
	elif list[4]==2:
		year="3rd"
	else:
		year="4th"

	batch=list[5]
	address=list[6]
	mobile=list[7]
	gpa=list[8]
	attendance=list[9]

	table=QTableWidget()
	tableItem=QTableWidgetItem()
	table.setWindowTitle("Student Details")
	table.setRowCount(10)
	table.setColumnCount(2)

	table.setItem(0,0, QTableWidgetItem("Roll"))
	table.setItem(0,1, QTableWidgetItem(str(roll)))
	table.setItem(1,0, QTableWidgetItem("Name"))
	table.setItem(1,1, QTableWidgetItem(str(name)))
	table.setItem(2,0, QTableWidgetItem("Gender"))
	table.setItem(2,1, QTableWidgetItem(str(gender)))
	table.setItem(3,0, QTableWidgetItem("Department"))
	table.setItem(3,1, QTableWidgetItem(str(department)))
	table.setItem(4,0, QTableWidgetItem("Year"))
	table.setItem(4,1, QTableWidgetItem(str(year)))
	table.setItem(5,0, QTableWidgetItem("Batch"))
	table.setItem(5,1, QTableWidgetItem(str(batch)))
	table.setItem(6,0, QTableWidgetItem("address"))
	table.setItem(6,1, QTableWidgetItem(str(address)))
	table.setItem(7,0, QTableWidgetItem("Mobile"))
	table.setItem(7,1, QTableWidgetItem(str(mobile)))
	table.setItem(8,0, QTableWidgetItem("GPA"))
	table.setItem(8,1, QTableWidgetItem(str(gpa)))
	table.setItem(9,0, QTableWidgetItem("Attendance"))
	table.setItem(9,1, QTableWidgetItem(str(attendance)))
	table.horizontalHeader().setStretchLastSection(True)
	table.show()
	dialog=QDialog()
	dialog.setWindowTitle("Student Details")
	dialog.setWindowIcon(QtGui.QIcon("user.png"))
	dialog.resize(500,429)
	dialog.setLayout(QVBoxLayout())
	dialog.layout().addWidget(table)
	dialog.exec()


	####FE###

class name_gpa_cis():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=0 and year=0 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()
		


class top10gpa_cis(QDialog,name_gpa_cis):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA CIS")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA CIS FE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_gpa_el():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=1 and year=0 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_el(QDialog,name_gpa_el):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA EL FE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA EL")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()
###FE ENDDDDDDDDDDDD


##SE


class name_gpa_cis_se():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=0 and year=1 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_cis_se(QDialog,name_gpa_cis_se):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA CIS SE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA CIS SE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_gpa_el_se():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=1 and year=1 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_el_se(QDialog,name_gpa_el_se):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA EL SE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA EL SE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()

##SE ENDDDDDDD

##TE

class name_gpa_cis_te():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=0 and year=2 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_cis_te(QDialog,name_gpa_cis_te):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA CIS TE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA CIS TE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_gpa_el_te():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=1 and year=2 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_el_te(QDialog,name_gpa_el_te):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA EL TE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA EL")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()
#TE ENDDDDDDDDDD

#BE 

class name_gpa_cis_be():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=0 and year=3 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_cis_be(QDialog,name_gpa_cis_be):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA CIS BE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA CIS BE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_gpa_el_be():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,gpa from students where department=1 and year=3 order by gpa desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10gpa_el_be(QDialog,name_gpa_el_be):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 GPA EL BE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'GPA'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 GPA EL BE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()
#BE ENDDDDDDD



######################################ATTTT 

class name_att_cis():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=0 and year=0 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_cis(QDialog,name_att_cis):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE CIS FE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE CIS FE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_att_el():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=1 and year=0 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_el(QDialog,name_att_el):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE EL FE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE EL FE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()
###FE ENDDDDDDDDDDDD


##SE


class name_att_cis_se():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=0 and year=1 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_cis_se(QDialog,name_att_cis_se):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE CIS SE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE CIS SE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_att_el_se():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=1 and year=1 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_el_se(QDialog,name_att_el_se):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE EL SE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE EL SE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()

##SE ENDDDDDDD

##TE

class name_att_cis_te():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=0 and year=2 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_cis_te(QDialog,name_att_cis_te):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE CIS TE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE CIS TE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_att_el_te():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=1 and year=2 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_el_te(QDialog,name_att_el_te):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE EL TE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE EL TE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()
#TE ENDDDDDDDDDD

#BE 

class name_att_cis_be():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=0 and year=3 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_cis_be(QDialog,name_att_cis_be):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE CIS BE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE CIS BE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()



class name_att_el_be():
	def __init__(self):
		self.conn=sqlite3.connect('sims.db')
		self.c = self.conn.cursor()

		self.a=self.c.execute("SELECT name,attendance from students where department=1 and year=3 order by attendance desc limit 10")
		self.b=dict(self.a)
		self.d=list(self.b.keys())
		self.gpa=list(self.b.values())
		self.tup=[str(x) for x in self.gpa]

		self.conn.commit()
		self.conn.close()


class top10att_el_be(QDialog,name_att_el_be):
	def __init__(self):
		super().__init__()


		self.tableWidget=QTableWidget()
		self.tableItem=QTableWidgetItem()
		self.tableWidget.setWindowTitle("TOP 10 ATTENDANCE EL BE")
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(('NAME', 'ATTENDANCE'))
		self.tableWidget.setStyleSheet("background-color:white; border: 1px solid black; color:teal; selection-background-color:cadetblue; selection-color:white;")

		for i in range(0,10):
			self.tableWidget.setItem(i,0, QTableWidgetItem(self.d[i]))

		for j in range(0,10):
			self.tableWidget.setItem(j,1, QTableWidgetItem(self.tup[j]))
			
		self.dialog1=QDialog()
		self.dialog1.setWindowTitle("TOP 10 ATTENDANCE EL BE")
		self.dialog1.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog1.resize(307,432)
		self.dialog1.setLayout(QVBoxLayout())
		self.dialog1.layout().addWidget(self.tableWidget)
		self.dialog1.exec()
#BE ENDDDDDDD

############ATTTT END
class AddStudent(QDialog):
	def __init__(self):
		super().__init__()

		self.roll=-1
		self.name=""
		self.gender=-1
		self.department=-1
		self.year=-1
		self.batch=-1
		self.address=""
		self.mobile=-1
		self.gpa=0
		self.attendance=0

		self.QPixmap=QLabel(self)
		self.QPixmap.resize(600,400)
		self.QPixmap.setPixmap(QtGui.QPixmap("bbg.jpeg"))


		self.btnCancel=QPushButton("Cancel",self)
		self.btnCancel.setStyleSheet("background:teal ; colour: white ;font-size:14pt ; font-family:arial")
		self.btnReset=QPushButton("Reset",self)
		self.btnAdd=QPushButton("Add",self)

		self.btnCancel.setFixedHeight(30)
		self.btnReset.setFixedHeight(30)
		self.btnAdd.setFixedHeight(30)

		self.yearCombo=QComboBox(self)
		self.yearCombo.addItem("1st")
		self.yearCombo.addItem("2nd")
		self.yearCombo.addItem("3rd")
		self.yearCombo.addItem("4th")

		self.genderCombo= QComboBox(self)
		self.genderCombo.addItem("Male")
		self.genderCombo.addItem("Female")

		self.departmentCombo = QComboBox(self)
		self.departmentCombo.addItem("Computer Systems Engineering")
		self.departmentCombo.addItem("Electrical Engineering")

		self.rollLabel=QLabel("Roll No")
		self.nameLabel=QLabel("Name")
		self.genderLabel=QLabel("Gender")
		self.departmentLabel=QLabel("Department")
		self.yearLabel=QLabel("Year")
		self.batchLabel=QLabel("Batch")
		self.addressLabel=QLabel("Address")
		self.mobileLabel=QLabel("Mobile")
		self.gpaLabel=QLabel("GPA")
		self.attendanceLabel=QLabel("Attendance")

		self.rollText=QLineEdit(self)
		self.nameText=QLineEdit(self)
		self.addressText=QLineEdit(self)
		self.mobText=QLineEdit(self)
		self.batchText=QLineEdit(self)
		self.gpaText=QLineEdit(self)
		self.attendanceText=QLineEdit(self)

		self.grid=QGridLayout(self)
		self.grid.addWidget(self.rollLabel,1,1)
		self.grid.addWidget(self.nameLabel,2,1)
		self.grid.addWidget(self.genderLabel,3,1)
		self.grid.addWidget(self.departmentLabel,4,1)
		self.grid.addWidget(self.yearLabel,5,1)
		self.grid.addWidget(self.batchLabel,6,1)
		self.grid.addWidget(self.addressLabel,7,1)
		self.grid.addWidget(self.mobileLabel,8,1)
		self.grid.addWidget(self.gpaLabel,9,1)
		self.grid.addWidget(self.attendanceLabel,10,1)

		self.grid.addWidget(self.rollText,1,2)
		self.grid.addWidget(self.nameText,2,2)
		self.grid.addWidget(self.genderCombo,3,2)
		self.grid.addWidget(self.departmentCombo,4,2)
		self.grid.addWidget(self.yearCombo,5,2)
		self.grid.addWidget(self.batchText,6,2)
		self.grid.addWidget(self.addressText,7,2)
		self.grid.addWidget(self.mobText,8,2)
		self.grid.addWidget(self.gpaText,9,2)
		self.grid.addWidget(self.attendanceText,10,2)

		self.grid.addWidget(self.btnReset,11,1)
		self.grid.addWidget(self.btnCancel,11,2)
		self.grid.addWidget(self.btnAdd,11,3)

		self.btnAdd.clicked.connect(self.addStudent)
		self.btnCancel.clicked.connect(QApplication.instance().quit)
		self.btnReset.clicked.connect(self.reset)

		self.setLayout(self.grid)
		self.setWindowTitle("Add Student Details")
		self.setWindowIcon(QtGui.QIcon("user.png"))
		self.resize(500,300)
		self.show()
		sys.exit(self.exec())

	def reset(self):
		self.rollText.setText("")
		self.batchText.setText("")
		self.nameText.setText("")
		self.addressText.setText("")
		self.mobText.setText("")
		self.gpaText.setText("")
		self.attendanceText.setText("")

	def addStudent(self):
		self.gender=self.genderCombo.currentIndex()
		self.year=self.yearCombo.currentIndex()
		self.department=self.departmentCombo.currentIndex()
		self.roll=int(self.rollText.text())
		self.name=self.nameText.text()
		self.batch=int(self.batchText.text())
		self.address=self.addressText.text()
		self.mobile=int(self.mobText.text())
		self.gpa=float(self.gpaText.text())
		self.attendance=float(self.attendanceText.text())

		self.sims_app=sims_app()
		self.sims_app.addStudent(self.roll,self.name,self.gender,self.department,self.year,self.batch,self.address,self.mobile,self.gpa,self.attendance)

class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.rollToBeSearched=0
		self.vbox=QVBoxLayout()
		self.text=QLabel("Enter the roll no of student")
		self.editField=QLineEdit()
		self.btnSearch= QPushButton("search",self)
		self.btnSearch.clicked.connect(self.showStudent)
		self.vbox.addWidget(self.text)
		self.vbox.addWidget(self.editField)
		self.vbox.addWidget(self.btnSearch)
		self.dialog=QDialog()
		self.dialog.setWindowTitle("Enter Roll no")
		self.dialog.setWindowIcon(QtGui.QIcon("user.png"))
		self.dialog.setLayout(self.vbox)
#background image
		self.QPixmap=QLabel(self)
		self.QPixmap.resize(5000,800)
		self.QPixmap.setPixmap(QtGui.QPixmap("image.jpeg"))
#picture
		self.picLabel=QLabel(self)
		self.picLabel.resize(150,150)
		self.picLabel.move(600,20)
		self.picLabel.setScaledContents(True)
		self.picLabel.setPixmap(QtGui.QPixmap("user.png"))
		
		self.btnEnterStudent=QPushButton("Enter Student Details",self)
		self.btnShowStudentDetails=QPushButton("Show Student Details",self)
		self.btnEnterStudent.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnShowStudentDetails.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")

		self.CIS=QLabel("SOFTWARE BY        Ukasha,Mahnoor And       Iraj.",self)
		self.CIS.move(410,660)
		self.CIS.resize(1000,40)
		self.CISFont=self.CIS.font()
		self.CISFont.setPointSize(15)
		self.CIS.setStyleSheet("color:black; font-size: 15pt; font-family: Arial Rounded MT Bold")

		self.CIS=QLabel("COMPUTER AND INFORMATION SYSTEM",self)
		self.CIS.move(510,285)
		self.CIS.resize(500,40)
		self.CISFont=self.CIS.font()
		self.CISFont.setPointSize(15)
		self.CIS.setStyleSheet("color:black; font-size: 15pt; font-family:Arial Rounded MT Bold ")
		
		
		
		self.EL=QLabel('ELECTRICAL',self)
		self.EL.move(630,450)
		self.EL.resize(200,40)
		self.ELFont=self.EL.font()
		self.ELFont.setPointSize(20)
		self.EL.setStyleSheet("color:black; font-size: 15pt; font-family: Arial Rounded MT Bold")

		self.TOP10GPA=QLabel("TOP 10 GPA",self)
		self.TOP10GPA.move(50,320)
		self.TOP10GPA.resize(180,50)
		self.TOP10GPAFont=self.TOP10GPA.font()
		self.TOP10GPAFont.setPointSize(13)
		self.TOP10GPA.setStyleSheet("color:black; font-size: 15pt; font-family:Arial Rounded MT Bold ")

		self.TOP10GPA=QLabel("TOP 10 ATTENDANCE",self)
		self.TOP10GPA.move(50,390)
		self.TOP10GPA.resize(250,50)
		self.TOP10GPAFont=self.TOP10GPA.font()
		self.TOP10GPAFont.setPointSize(13)
		self.TOP10GPA.setStyleSheet("color:black; font-size: 15pt; font-family: Arial Rounded MT Bold")

		self.TOP10GPA=QLabel("TOP 10 GPA",self)
		self.TOP10GPA.move(50,485)
		self.TOP10GPA.resize(180,50)
		self.TOP10GPAFont=self.TOP10GPA.font()
		self.TOP10GPAFont.setPointSize(15)
		self.TOP10GPA.setStyleSheet("color:black; font-size: 15pt; font-family: Arial Rounded MT Bold")

		self.TOP10GPA=QLabel("TOP 10 ATTENDANCE",self)
		self.TOP10GPA.move(50,555)
		self.TOP10GPA.resize(250,50)
		self.TOP10GPAFont=self.TOP10GPA.font()
		self.TOP10GPAFont.setPointSize(15)
		self.TOP10GPA.setStyleSheet("color:black; font-size: 15pt; font-family: Arial Rounded MT Bold")

		self.btnshowTop10GPA_CIS=QPushButton("FE",self)
		self.btnshowTop10GPA_CIS.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_EL=QPushButton("FE",self)
		self.btnshowTop10GPA_EL.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_CIS_SE=QPushButton("SE",self)
		self.btnshowTop10GPA_CIS_SE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_EL_SE=QPushButton("SE",self)
		self.btnshowTop10GPA_EL_SE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_CIS_TE=QPushButton("TE",self)
		self.btnshowTop10GPA_CIS_TE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_EL_TE=QPushButton("TE",self)
		self.btnshowTop10GPA_EL_TE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_CIS_BE=QPushButton("BE",self)
		self.btnshowTop10GPA_CIS_BE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10GPA_EL_BE=QPushButton("BE",self)
		self.btnshowTop10GPA_EL_BE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")

		self.btnshowTop10ATT_CIS=QPushButton("FE",self)
		self.btnshowTop10ATT_CIS.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_EL=QPushButton("FE",self)
		self.btnshowTop10ATT_EL.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_CIS_SE=QPushButton("SE",self)
		self.btnshowTop10ATT_CIS_SE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_EL_SE=QPushButton("SE",self)
		self.btnshowTop10ATT_EL_SE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_CIS_TE=QPushButton("TE",self)
		self.btnshowTop10ATT_CIS_TE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_EL_TE=QPushButton("TE",self)
		self.btnshowTop10ATT_EL_TE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_CIS_BE=QPushButton("BE",self)
		self.btnshowTop10ATT_CIS_BE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")
		self.btnshowTop10ATT_EL_BE=QPushButton("BE",self)
		self.btnshowTop10ATT_EL_BE.setStyleSheet("background:teal; color:white; font-size: 15pt; font-family: Arial Rounded MT Bold;")


		self.btnEnterStudent.move(370,200)
		self.btnEnterStudent.resize(300,50)
		self.btnEnterStudentFont=self.btnEnterStudent.font()
		self.btnEnterStudentFont.setPointSize(10)
		self.btnEnterStudent.setFont(self.btnEnterStudentFont)
		self.btnEnterStudent.clicked.connect(self.enterstudent)

		self.btnshowTop10GPA_CIS.move(300,320)
		self.btnshowTop10GPA_CIS.resize(180,40)
		self.btnshowTop10GPA_CISFont=self.btnshowTop10GPA_CIS.font()
		self.btnshowTop10GPA_CISFont.setPointSize(10)
		self.btnshowTop10GPA_CIS.setFont(self.btnshowTop10GPA_CISFont)
		self.btnshowTop10GPA_CIS.clicked.connect(self.showtop10gpa_cis)

		self.btnshowTop10GPA_EL.move(300,485)
		self.btnshowTop10GPA_EL.resize(180,40)
		self.btnshowTop10GPA_ELFont=self.btnshowTop10GPA_EL.font()
		self.btnshowTop10GPA_ELFont.setPointSize(10)
		self.btnshowTop10GPA_EL.setFont(self.btnshowTop10GPA_ELFont)
		self.btnshowTop10GPA_EL.clicked.connect(self.showtop10gpa_el)

		#####

		self.btnshowTop10GPA_CIS_SE.move(500,320)
		self.btnshowTop10GPA_CIS_SE.resize(180,40)
		self.btnshowTop10GPA_CIS_SEFont=self.btnshowTop10GPA_CIS_SE.font()
		self.btnshowTop10GPA_CIS_SEFont.setPointSize(10)
		self.btnshowTop10GPA_CIS_SE.setFont(self.btnshowTop10GPA_CIS_SEFont)
		self.btnshowTop10GPA_CIS_SE.clicked.connect(self.showtop10gpa_cis_se)

		self.btnshowTop10GPA_EL_SE.move(500,485)
		self.btnshowTop10GPA_EL_SE.resize(180,40)
		self.btnshowTop10GPA_EL_SEFont=self.btnshowTop10GPA_EL_SE.font()
		self.btnshowTop10GPA_EL_SEFont.setPointSize(10)
		self.btnshowTop10GPA_EL_SE.setFont(self.btnshowTop10GPA_EL_SEFont)
		self.btnshowTop10GPA_EL_SE.clicked.connect(self.showtop10gpa_el_se)
		####
####TE
		self.btnshowTop10GPA_CIS_TE.move(700,320)
		self.btnshowTop10GPA_CIS_TE.resize(180,40)
		self.btnshowTop10GPA_CIS_TEFont=self.btnshowTop10GPA_CIS_TE.font()
		self.btnshowTop10GPA_CIS_TEFont.setPointSize(10)
		self.btnshowTop10GPA_CIS_TE.setFont(self.btnshowTop10GPA_CIS_TEFont)
		self.btnshowTop10GPA_CIS_TE.clicked.connect(self.showtop10gpa_cis_te)

		self.btnshowTop10GPA_EL_TE.move(700,485)
		self.btnshowTop10GPA_EL_TE.resize(180,40)
		self.btnshowTop10GPA_EL_TEFont=self.btnshowTop10GPA_EL_TE.font()
		self.btnshowTop10GPA_EL_TEFont.setPointSize(10)
		self.btnshowTop10GPA_EL_TE.setFont(self.btnshowTop10GPA_EL_TEFont)
		self.btnshowTop10GPA_EL_TE.clicked.connect(self.showtop10gpa_el_te)

##TE END

###BE

		self.btnshowTop10GPA_CIS_BE.move(900,320)
		self.btnshowTop10GPA_CIS_BE.resize(180,40)
		self.btnshowTop10GPA_CIS_BEFont=self.btnshowTop10GPA_CIS_BE.font()
		self.btnshowTop10GPA_CIS_BEFont.setPointSize(10)
		self.btnshowTop10GPA_CIS_BE.setFont(self.btnshowTop10GPA_CIS_BEFont)
		self.btnshowTop10GPA_CIS_BE.clicked.connect(self.showtop10gpa_cis_be)

		self.btnshowTop10GPA_EL_BE.move(900,485)
		self.btnshowTop10GPA_EL_BE.resize(180,40)
		self.btnshowTop10GPA_EL_BEFont=self.btnshowTop10GPA_EL_BE.font()
		self.btnshowTop10GPA_EL_BEFont.setPointSize(10)
		self.btnshowTop10GPA_EL_BE.setFont(self.btnshowTop10GPA_EL_BEFont)
		self.btnshowTop10GPA_EL_BE.clicked.connect(self.showtop10gpa_el_be)
###BE END


###################buttonnn ATTTT
		 
		self.btnshowTop10ATT_CIS.move(300,390)
		self.btnshowTop10ATT_CIS.resize(180,40)
		self.btnshowTop10ATT_CISFont=self.btnshowTop10ATT_CIS.font()
		self.btnshowTop10ATT_CISFont.setPointSize(10)
		self.btnshowTop10ATT_CIS.setFont(self.btnshowTop10ATT_CISFont)
		self.btnshowTop10ATT_CIS.clicked.connect(self.showtop10att_cis)

		self.btnshowTop10ATT_EL.move(300,555)
		self.btnshowTop10ATT_EL.resize(180,40)
		self.btnshowTop10ATT_ELFont=self.btnshowTop10ATT_EL.font()
		self.btnshowTop10ATT_ELFont.setPointSize(10)
		self.btnshowTop10ATT_EL.setFont(self.btnshowTop10ATT_ELFont)
		self.btnshowTop10ATT_EL.clicked.connect(self.showtop10att_el)

		#####

		self.btnshowTop10ATT_CIS_SE.move(500,390)
		self.btnshowTop10ATT_CIS_SE.resize(180,40)
		self.btnshowTop10ATT_CIS_SEFont=self.btnshowTop10ATT_CIS_SE.font()
		self.btnshowTop10ATT_CIS_SEFont.setPointSize(10)
		self.btnshowTop10ATT_CIS_SE.setFont(self.btnshowTop10ATT_CIS_SEFont)
		self.btnshowTop10ATT_CIS_SE.clicked.connect(self.showtop10att_cis_se)

		self.btnshowTop10ATT_EL_SE.move(500,555)
		self.btnshowTop10ATT_EL_SE.resize(180,40)
		self.btnshowTop10ATT_EL_SEFont=self.btnshowTop10ATT_EL_SE.font()
		self.btnshowTop10ATT_EL_SEFont.setPointSize(10)
		self.btnshowTop10ATT_EL_SE.setFont(self.btnshowTop10ATT_EL_SEFont)
		self.btnshowTop10ATT_EL_SE.clicked.connect(self.showtop10att_el_se)
		####
####TE
		self.btnshowTop10ATT_CIS_TE.move(700,390)
		self.btnshowTop10ATT_CIS_TE.resize(180,40)
		self.btnshowTop10ATT_CIS_TEFont=self.btnshowTop10ATT_CIS_TE.font()
		self.btnshowTop10ATT_CIS_TEFont.setPointSize(10)
		self.btnshowTop10ATT_CIS_TE.setFont(self.btnshowTop10ATT_CIS_TEFont)
		self.btnshowTop10ATT_CIS_TE.clicked.connect(self.showtop10att_cis_te)

		self.btnshowTop10ATT_EL_TE.move(700,555)
		self.btnshowTop10ATT_EL_TE.resize(180,40)
		self.btnshowTop10ATT_EL_TEFont=self.btnshowTop10ATT_EL_TE.font()
		self.btnshowTop10ATT_EL_TEFont.setPointSize(10)
		self.btnshowTop10ATT_EL_TE.setFont(self.btnshowTop10ATT_EL_TEFont)
		self.btnshowTop10ATT_EL_TE.clicked.connect(self.showtop10att_el_te)

##TE END

###BE

		self.btnshowTop10ATT_CIS_BE.move(900,390)
		self.btnshowTop10ATT_CIS_BE.resize(180,40)
		self.btnshowTop10ATT_CIS_BEFont=self.btnshowTop10ATT_CIS_BE.font()
		self.btnshowTop10ATT_CIS_BEFont.setPointSize(10)
		self.btnshowTop10ATT_CIS_BE.setFont(self.btnshowTop10ATT_CIS_BEFont)
		self.btnshowTop10ATT_CIS_BE.clicked.connect(self.showtop10att_cis_be)

		self.btnshowTop10ATT_EL_BE.move(900,555)
		self.btnshowTop10ATT_EL_BE.resize(180,40)
		self.btnshowTop10ATT_EL_BEFont=self.btnshowTop10ATT_EL_BE.font()
		self.btnshowTop10ATT_EL_BEFont.setPointSize(10)
		self.btnshowTop10ATT_EL_BE.setFont(self.btnshowTop10ATT_EL_BEFont)
		self.btnshowTop10ATT_EL_BE.clicked.connect(self.showtop10att_el_be)
###BE END		 

############333BUTTONN ATT END
		self.btnShowStudentDetails.move(700,200)
		self.btnShowStudentDetails.resize(300,50)
		self.btnShowStudentDetailsFont=self.btnEnterStudent.font()
		self.btnShowStudentDetailsFont.setPointSize(10)
		self.btnShowStudentDetails.setFont(self.btnShowStudentDetailsFont)
		self.btnShowStudentDetails.clicked.connect(self.showStudentDialog)

		self.resize(1280,800)
		self.setWindowTitle("Student information storing System")
		self.setWindowIcon(QtGui.QIcon("user.png"))
		

	def enterstudent(self):
		AddStudent()

	def showStudentDialog(self):
		self.dialog.exec()

	def showtop10gpa_cis(self):
		top10gpa_cis()

	def showtop10gpa_el(self):
		top10gpa_el()

	def showtop10gpa_cis_se(self):
		top10gpa_cis_se()

	def showtop10gpa_el_se(self):
		top10gpa_el_se()

	def showtop10gpa_cis_te(self):
		top10gpa_cis_te()

	def showtop10gpa_el_te(self):
		top10gpa_el_te()

	def showtop10gpa_cis_be(self):
		top10gpa_cis_be()

	def showtop10gpa_el_be(self):
		top10gpa_el_be()

######att

	def showtop10att_cis(self):
		top10att_cis()

	def showtop10att_el(self):
		top10att_el()

	def showtop10att_cis_se(self):
		top10att_cis_se()

	def showtop10att_el_se(self):
		top10att_el_se()

	def showtop10att_cis_te(self):
		top10att_cis_te()

	def showtop10att_el_te(self):
		top10att_el_te()

	def showtop10att_cis_be(self):
		top10att_cis_be()

	def showtop10att_el_be(self):
		top10att_el_be()

	def showStudent(self):

		if self.editField.text() is "":
			QMessageBox.warning(QMessageBox(),'Error','You must enter the roll no to show result')

			return None

		showstudent=sims_app()
		showstudent.searchStudent(int(self.editField.text()))


if __name__ == "__main__":
	app = QApplication(sys.argv)
	login=Login()

	if login.exec_() == QDialog.Accepted:
		window=Window()
		window.show()
	sys.exit(app.exec_())