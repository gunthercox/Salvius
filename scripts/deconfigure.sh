# Copy the salvius initscript to /etc/init.d
sudo rm /etc/init.d/salvius

# Do not start salvius automatically on boot
sudo update-rc.d -f salvius remove
