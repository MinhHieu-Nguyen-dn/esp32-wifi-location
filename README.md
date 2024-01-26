# Find a user’s in-house location 
**Using WiFi signal from ESP32 and Random Forest machine learning model**  
*Class: Internet of Things and Applications - Final project*

## Install guide:

1. Project's virtual environment  
*Note: Python **3.5** is selected here based on the root project. Newer versions of Python might work as well - Give it a try!*  
`conda create -n iot_where python=3.5 -c conda-forge` 

2. Create a new PyCharm project with the above env (Conda env interpreter: Python 3.5 (iot_where)).  

3. Clone repo:  
```
git clone https://github.com/MinhHieu-Nguyen-dn/esp32-wifi-location.git
cd whereami
```

4. Install dependencies:  
```
pip install -r requirements.txt
```  

5. Install `access_points` package (terminal: in the wrapper folder `whereami`):  
`git clone https://github.com/kootenpv/access_points`  
Then mark the wrapper access_points folder (path is `.\whereami\access_points`) as **Sources root**.

## Setup guide:

1. Setup project's structure:  
- Set content root to `whereami` folder (the outer folder the wraps this whole repo).  
- Mark directories in `.gitignore` as **Excluded**.
- Mark the wrapper access_points folder (path is `.\whereami\access_points`) as **Sources root**.  

2. Local network:  
Let's say we will work on port `8090`.  
- In `send_data_server/send_data_server.ino`:
```
const uint16_t port = 8090;
```

- In `socket_app.py` - for terminal testing:
```
s.bind(('0.0.0.0', 8090))
```

- In `flask_app.py` - for both terminal and web interface testing:
```
s.bind(('0.0.0.0', 8090))
```

##### Now we configure the IP Address where the server (your device) and the client (ESP32) will communicate: (for Windows user)  
- Open Command Prompt
- Enter:  
```
ipconfig
```
- Scroll down to "Wireless LAN adapter Wi-Fi" part, then copy the value of `IPv4 Address`
- Go to `send_data_server/send_data_server.ino`:
```
const char * host = "your_IPv4_Address";
```

### To finish setting up the project:
(terminal: in the wrapper folder `whereami`)
```
python setup.py install
```

## Train your model:
**(terminal: in the wrapper folder `whereami`)**  
This part works personally for each user. Let's say, you want to predict the location of ESP32 on the floor of the building, do the following training process:  
- Go to a floor where you call it *"floor_name"*:
```
whereami learn -l floor_name -n 50
```
From this, the model starts scanning WiFi data to build model. In this example, the model will learn "floor_name" WiFi signals where you put your machine (laptop) at, take 50 samples, 15 seconds between 2 samples.  
You can see the progress bar in the terminal.  
- Do similarly when you go to different floor to train the model.  
- The data for training (labels with features) and trained model (file .pkl) is stored at a newly created directory named:  
```
.whereami
```

### Review the model and training data:

```
# get a list of already learned locations
whereami locations

# cross-validated accuracy on historic data
whereami crossval
# 0.99319

# probabilities per class
whereami predict_proba
# {"floor_1": 0.99, "floor_2": 0.01}
```

## Now push the code to ESP32 to use this device:
1. Open `send_data_server/send_data_server.ino` with Arduino IDE  
2. Connect your ESP32 to the device, setup correct USB port of device, then push the code.  
3. Check the Serial to see if it runs correctly.
4. Connect ESP32 to a charger.

The ESP32 device now can be used to scan WiFi Signal, send to the local server hosted on the laptop to perform in-house location prediction.

Next step is opening the local server to receive data from ESP32. 

## Prediction:
For a terminal result, run `socket_app.py` to start listening on your port setup before. Result of data sending to server and prediction will be displayed in the terminal.  

For a web application interface, run `flask_app.py`. The result will be displayed on the web interface everytime the user reload it.
