pip install flask flask-babel flask-sqlalchemy paho-mqtt
sudo ln -s $(pwd) /opt/mqtt-oled-display 
sudo ln -s /opt/mqtt-oled-display/mqtt-oled-display.service /etc/systemd/system/mqtt-oled-display.service
cat /etc/systemd/system/mqtt-oled-display.service 