# installer les dependances
pip install flask flask-babel flask-sqlalchemy paho-mqtt

# installer les serviecs
sudo ln -s $(pwd) /opt/mqtt-oled-display 

sudo ln -s /opt/mqtt-oled-display/mqtt-oled-display.service /etc/systemd/system/mqtt-oled-display.service
cat /etc/systemd/system/mqtt-oled-display.service 

sudo ln -s /opt/mqtt-oled-display/mqtt-oled-display-webserver.service /etc/systemd/system/mqtt-oled-display-webserver.service
cat /etc/systemd/system/mqtt-oled-display-webserver.service 

# demarrer et tester les services
sudo service mqtt-oled-display-webserver start
sudo service mqtt-oled-display start

journalctl -u mqtt-oled-display-webserver --no-pager -f
journalctl -u mqtt-oled-display --no-pager -f


# activer les services au démarrage
sudo systemctl enable mqtt-oled-display
sudo systemctl enable mqtt-oled-display-webserver

