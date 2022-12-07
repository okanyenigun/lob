# Limit Order Book

A draft django application works on stock order data

## How to install

-Create a virtual env\
python -m venv .env\
(for mac-> python3 -m venv .env)\

-Select the new venv as your interpreter\

-Install requirements\
pip install -r requirements.txt\

-Install talib package \
(only for windows)\
pip install TA_Lib-0.4.24-cp38-cp38-win_amd64.whl\

-Run server\
python manage.py runserver\

-go to localhost\
http://127.0.0.1:8000/\

## How it works
APPS:\

|-- builder -> responsible for dataset preparation (from order to lob)\
   |   |-- controller.py -> a kind of controller; mainly static methods\
   |   |-- meta.py -> a singleton class to store data\
   |   |-- urls.py -> urls\
   |   |-- views.py -> views\
   |   |-- services -> where the actual work is done\
   |   |   |-- dataproc.py -> cleaning & filling\
   |   |   |-- mold.py -> creating MOLD ITCH\
   |   |   |-- lobber.py -> creating lob rows\
   |   |   |-- proc.py -> a procedure to run each in order to obtain df\
   
|-- backtester -> responsible for backtest\
   |   |-- controller.py -> a kind of controller; handles requests (passed from views)\
   |   |-- urls.py -> urls\
   |   |-- views.py -> views\
   |   |-- services -> where the actual work is done\
   |   |   |-- backt.py -> backtest class\

|-- indicators -> financial indicators\
   |   |-- abs.py -> an abstract class for indicators\
   |   |-- macd.py -> macd indicator\
   |   |-- rsi.py -> rsi indicator\
   
|-- utility -> utility functions\
   |   |-- charts.py -> responsible for creating charts\
   |   |-- utils.py -> helper methods\
