# README for getweatherdata

This programme reads weather data from an API that i'm exposing from my home network.

## output
The programme writes its output to a Python PANDAS dataframe stored in Parquet form. The column names are self-evident. 

## installation
* Create a folder on the server to hold the files, then copy the .sh, .py, requirements and service file to this folder.
* Create a python virtualenv - mine is called 'openhabstuff'- activate it and run pip install -r requirements.txt.
* Edit `getweatherdata.service` to reflect the location of the stop and start scripts.
* Create a folder to hold the captured data - mine is `$HOME/weather/raw`
* Edit `startGetData.sh` to reflect the name of your python virtualenv and the target location to write data to. 
* Request an API key from me, then update `apiConfig.py` accordingly.
* Install the service:
  ``` bash
  sudo cp getweatherdata.service /lib/systemd/system/
  sudo systemctl daemon-reload 
  sudo systemctl enable getweatherdata 
  sudo systemctl start getweatherdata
  ```

Note that i'm using a self-signed certificate, so python's requests library will complain. You can work around that by setting verify=False and disabling notification of the warning:
```python
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
res = requests.get(url, headers=headers, verify=False)
```
