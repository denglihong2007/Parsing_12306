cd libs
python-3.9.10.exe
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install requests
cd Timetable_new
python setup.py build
python setup.py sdist
python setup.py install
cd..
cd train_graph
python setup.py install
pause
