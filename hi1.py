import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QMessageBox ,QFileDialog
from PyQt5.QtWidgets import QShortcut , QTextEdit

from PyQt5.QtGui import QIcon ,QKeySequence
from PyQt5.QtCore import pyqtSlot

import syntax_pars
import lex , syn


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'mini-Compilateur 2020'


        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 560
        self.initUI()

        self.file_path = None

        self.open_new_file_shortcut = QShortcut(QKeySequence('Ctrl+O'), self)
        self.open_new_file_shortcut.activated.connect(self.open_new_file)

        #self.save_current_file_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        #self.save_current_file_shortcut.activated.connect(self.save_current_file)



        self.scrollable_text_area = QTextEdit()


    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textArea
        self.editor = QPlainTextEdit(self)
        self.editor.move(20, 20)
        self.editor.resize(self.width - 300 , 400)

        self.editor.setStyleSheet("""QPlainTextEdit{
	        font-family:'Consolas'; 
	        color: #ccc; 
	        background-color: #2b2b2b;}""")

        self.highlight = syntax_pars.MiniLangHighlighter(self.editor.document())

        
        
        #infile = open('main.cf', 'r')
        #self.editor.setPlainText(infile.read())

        # Create a Open button in the window
        self.lexBtn = QPushButton('Open', self)
        self.lexBtn.move(self.width - 300 + 50, 20)
        self.lexBtn.clicked.connect(self.open_new_file)
        
        # Create a Save button in the window
        self.synBtn = QPushButton('Save', self)
        self.synBtn.move(self.width - 300 + 150 + 20  , 20)
        self.synBtn.clicked.connect(self.save_current_file)  

        # ===================================================
        # Create a button for the lexical analysis in the window
        self.lexBtn = QPushButton('lex', self)
        self.lexBtn.move(self.width - 300 + 50, 20 + 50)
        self.lexBtn.clicked.connect(self.analyse_lex)
        
        
        # Create a button for the syntaxic analysis in the window
        self.synBtn = QPushButton('syn', self)
        self.synBtn.move(self.width - 300 + 150 + 20  , 20 + 50)
        self.synBtn.clicked.connect(self.analyse_syn)        


        # Create a clear button in the window
        self.clearBtn = QPushButton('Clear', self)
        self.clearBtn.move(self.width - 300 + 30, 20 + 50 + 50 )
        self.clearBtn.clicked.connect(self.clear_btn)

        
        # output textArea 
        self.output = QPlainTextEdit(self)
        self.output.move( 20 , 440)
        self.output.resize( self.width - 20 * 2 , 100)



        self.show()
    

    def open_new_file(self):
        self.file_path, filter_type = QFileDialog.getOpenFileName(self, "Open new file","", "All files (*)")
        print("file path" + self.file_path)
        if self.file_path:
            with open(self.file_path, "r") as f:
                file_contents = f.read()
                self.title = self.file_path

            self.editor.setPlainText(file_contents)
        else:
            self.invalid_path_alert_message()
 

    # pb
    def save_current_file(self):
        if not self.file_path:
            new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this file as...", "", "All files (*)")
            if new_file_path:
                self.file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False
                
        file_contents = self.editor.document().toPlainText()
        with open(self.file_path, "w") as f:
            f.write(file_contents)





    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Fichier invalide!")
        messageBox.setText("Le fichier / direction s??l??ctionn?? n'est pas valid. Veuillez choisir un fichier valide.")
        messageBox.exec()


# work 
    def closeEvent(self, event):
        messageBox = QMessageBox()
        title = "Voulez-vous quitter l'application?"
        message = "Alerte !!\n\nISi vous quittez sans sauvegarder le projet actuel, vous risquez de perdre touyes les modifications apport??es.\n\nVoulez-vous rnregistrer le fichier avant de quitter?"
        
        reply = messageBox.question(self, title, message, messageBox.Yes | messageBox.No | messageBox.Cancel, messageBox.Cancel)
        if reply == messageBox.Yes:
            return_value = self.save_current_file()
            if return_value == False:
                event.ignore()
        elif reply == messageBox.No:
            event.accept()
        else:
            event.ignore()


    @pyqtSlot()
    def analyse_lex(self):
        print("lex function ... ")
        # get the text
        editorValue = self.editor.document().toPlainText()
        
        if editorValue == "":
            print("empty") # critical
            QMessageBox.warning(self, 'err', "Vous n'avez rien ??crit", QMessageBox.Close, QMessageBox.Close)
        else:
            x , _ = lex.lexical(editorValue)
            for tok in x:
                self.output.setPlainText(self.output.document().toPlainText() + str(tok) + '\n')
            self.output.setPlainText(self.output.document().toPlainText() + "=========== DONE ! ===========")

            QMessageBox.question(self, 'Output Message', "entit?? lexicalement correcte :)\nvouz pouvez voir la liste des tokens\nl??-dessous",QMessageBox.Ok,QMessageBox.Ok)

    def analyse_syn(self):
 
        print("syn function ... ")

    def clear_btn(self):
        self.editor.document().setPlainText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())