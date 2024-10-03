## Simple File server and client
This is our Simple Client Server application build with [Flask](https://flask.palletsprojects.com/en/3.0.x/) for Python.
### 1) Requirements
We provided a requirements file. Simply run `pip install requirements.txt` in the root folder.
### 2) How to run
1) Run the `python server.py`
2) Open another shell and run `python client.py`
3) For sending a file, the file has to be stored in client_storage. Afterward simply type `send [filename].[extension]`
4) To use a file with a simple command e.g. `less`,`nano`, etc. use the appropriate command and the name of the desired file.
E.g. `less [filename].[extension]`
5) If the file was not stored locally, afterward the file is stored in client_storage.
6) Currently, our client only supports simple commands and no pipelining
7) We provided some nonsensical text files, for testing different functionalities.