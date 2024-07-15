import socket
import sys
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QMenu, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon


class Browser(QMainWindow):
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        super().__init__()
        self.host = host
        self.port = port
        self.history_list = []
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.initUI()
                # Create a socket for TCP communication


    @pyqtSlot(str)
    def send_data_to_server(self, message, address='localhost', port=10000):
        try:

            # Connect to the server
            server_address = (address, port)
            self.sock.connect(server_address)

            # Send the message
            self.sock.sendall(message.encode())

            # Receive the response
            data = self.sock.recv(10000).decode()

            # Print the response
            print(f'Received: {data}')
        finally:
            # Close the socket
            self.sock.close()



    def initUI(self):
        self.setWindowTitle("My Browser")
        self.setGeometry(100, 100, 800, 600)

        # Create address bar
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.load_url)
        self.toolbar = self.addToolBar("Address")
        self.toolbar.addWidget(self.address_bar)

        # Create home button
        home_button = QAction(QIcon("home.png"), "Home", self)
        home_button.triggered.connect(self.go_home)
        self.toolbar.addAction(home_button)

            # Create refresh button
        refresh_button = QAction(QIcon("refresh.png"), "Refresh", self)
        refresh_button.triggered.connect(self.refresh)
        self.toolbar.insertAction(self.toolbar.actions()[0], refresh_button)

# Create back and forward buttons

        forward_button = QAction(QIcon("forward.png"), "Forward", self)
        forward_button.triggered.connect(self.forward)
        self.toolbar.insertAction(self.toolbar.actions()[0], forward_button)


        back_button = QAction(QIcon("backb.png"), "Back", self)
        back_button.triggered.connect(self.back)
        self.toolbar.insertAction(self.toolbar.actions()[0], back_button)


        #self.toolbar.addAction(forward_button)



# Create history button
        history_button = QAction(QIcon("history.png"), "History", self)
        history_button.triggered.connect(self.show_history)
        self.toolbar.addAction(history_button)
        #self.toolbar.insertAction(self.toolbar.actions()[0], history_button)

# Create new tab button
        new_tab_button = QAction(QIcon("newtab.png"), "New Tab", self)
        new_tab_button.triggered.connect(self.new_tab)
        self.toolbar.insertAction(self.toolbar.actions()[0], new_tab_button)


        # Create first tab
        self.new_tab()


    def request(self, url):
        request_str = f"GET {url} HTTP/1.1\r\nHost: {self.host}:{self.port}\r\n\r\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.sendall(request_str.encode())
        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data
        s.close()
        return response.split(b"\r\n\r\n")[1]


    def load_url(self):
        url = self.address_bar.text()
        self.history_list.append(url)
        self.current_view().load(QUrl(url))

    def go_home(self):
        self.current_view().load(QUrl("https://www.google.com"))

    def back(self):
        self.current_view().back()

    def forward(self):
        self.current_view().forward()

    def refresh(self):
        self.current_view().reload()

    def show_history(self):
        menu = QMenu(self)
        for url in self.history_list:
            action = QAction(url, self)
            action.triggered.connect(lambda checked, url=url: self.current_view().load(QUrl(url)))
            menu.addAction(action)
        menu.exec_(self.toolbar.mapToGlobal(self.toolbar.actionGeometry(self.sender()).bottomLeft()))

    def new_tab(self):
        view = QWebEngineView()
        view.load(QUrl("https://www.google.com"))
        index = self.tabs.addTab(view, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() == 1:
            self.close()
        else:
            self.tabs.removeTab(index)

    def current_view(self):
        return self.tabs.currentWidget()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser('localhost',80)
    browser.show()
    sys.exit(app.exec_())
