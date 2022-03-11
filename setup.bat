pip install requests
cd libs
python-3.9.10.exe
cd Timetable_new
python setup.py build
python setup.py sdist
python setup.py install
cd..
cd train_graph
python setup.py install
pause
