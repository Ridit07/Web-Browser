import socket
from bs4 import BeautifulSoup

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.example.com", 80))

request = "GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n"

s.send(request.encode())

response = s.recv(1024)
html_content = response.split(b"\r\n\r\n")[1]

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
parsed_html_content = soup.prettify()

# Render the parsed HTML content using Tkinter
import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
html_display = scrolledtext.ScrolledText(root, width=80, height=30)
html_display.pack()
html_display.insert(tk.END, parsed_html_content)
root.mainloop()


# import socket

# mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mysock.connect(('data.pr4e.org', 80))
# cmd = 'GET http://data.pr4e.org/page2.htm HTTP/1.0\r\n\r\n'.encode()
# mysock.send(cmd)

# while True:
#     data = mysock.recv(512)
#     if len(data) < 1:
#         break
#     print(data.decode(),end='')

# mysock.close()