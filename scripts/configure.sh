# Copy the salvius initscript to /etc/init.d
sudo cp ./salvius /etc/init.d

# Make the initscript executable
sudo chmod +x /etc/init.d/salvius

# Start salvius automatically on boot
sudo update-rc.d -f salvius defaults
