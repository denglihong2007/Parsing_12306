cd libs
python-3.10.3-amd64.exe
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests
pip install pyqt5
cd Timetable_new
python setup.py build
python setup.py sdist
python setup.py install
cd..
cd train_graph
python setup.py install
pause
