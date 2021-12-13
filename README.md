# Moonlight Smart Home

Moonlight Smart Home, an IoT-based application, is a simplistic smart home system designed to carry out 
the fundamental functionality of a real-world smart home. 

## Software
| Name        | Version     |
| ----------- | ----------- |
| [Raspbian GNU / Linux](https://www.raspbian.org/RaspbianInstaller) | 10 (buster) |
| [Python](https://www.python.org/downloads/)      | 3.7.3       |
| [Arduino Sketch](https://www.arduino.cc/en/software) | 1.8.16 |
| [Thonny Python](https://thonny.org/) | 3.3.14 |
| [Mosquitto MQTT Broker](https://mosquitto.org/) | 3.1.1 |
| [JavaScript](https://nodejs.org/en/) | 10.24.0 |
| [SQLiteStudio](https://sqlitestudio.pl/) |  3.2.1 |


## Instructions
The /Dashboard folder contains all python code related to the Python Dash dashboard.

- /Dashboard/app.py runs the server that dash will be mounted on.
- /Dashboard/index.py is the main thread that runs the dashboard computations.
- /Dashboard/apps/ is responsible for displaying the layouts of different pages.
- /Dashboard/assets/ contains the CSS file used to style the dashboard.
- /Dashboard/utils/ holds all files (python and javascript) that are used to carry out the functionality of the system.

The /Sketch folder contains the necessary code for the NodeMCU ESP8266.
- /Sketch/Dashboard-MQTT/ handles the analog data read from the NodeMCU and publishing to the MQTT broker.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages:

```bash
pip3 install dash
pip3 install plotly
pip3 install numpy
pip3 install pandas
pip3 install smtplib
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)
