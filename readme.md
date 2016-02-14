# Salvius

Salvius is a humanoid robot made from recycled materials. The robot is designed
to be as easy as possible for anyone to build on a limited budget.

Salvius is a robot made out of recycled materials, designed to be able to
perform a wide range of tasks by having a body structure that is similar
to that of a human. The primary goal for Salvius is to create a humanoid
robot that can function dynamically in a domestic environment.  

**Key features:**
  - Web based user interface
  - Easily customizable robots
  - REST API
  - Modular design makes it easy to connect new hardware

## Setup

```bash
# Clone the git repo
git clone https://github.com/gunthercox/Salvius.git

# Move to the Salvius directory
cd Salvius

# Install the package using pip
sudo pip install . --upgrade
```

### Testing the installation

Once installed, you should be able to start Salvius by entering the command `salvius` into the terminal.
After that, you should be able to view the robot's api in your browser by going to `http://localhost:8000/api/`

### Configure Salvius to run at startup

To configure Salvius to start running when your device boots,
execute the following from inside the `scripts` directory.
```
bash configure.sh
```

**Note:** that if you no longer wish to run Salvius at startup, you can disable
this functionality by running `bash deconfigure.sh` from inside the `scripts`
directory.

## Verbal communication

Salvius uses the [ChatterBot](https://github.com/gunthercox/ChatterBot) library
to generate responses to verbal input.

### Speech recognition

Speech recognition is accomplished using the [pocketsphinx](http://cmusphinx.sourceforge.net/wiki/tutorialpocketsphinx)
speech recognition library for Python. Salvius is currently only configured to
recognize English language models, but it is possible to build grammars for other
languages for pocketsphinx.

### Speech synthesis

Salvius uses the [Emic 2 Text-to-Speech Module](https://www.sparkfun.com/products/11711)
to process text into verbal sounds. A guide for using the Emic board with your
Raspberry Pi can be found [here](http://zorg-emic.readthedocs.org/en/stable/using-with-raspberry-pi/).

### Handwriting

The robot can hold a pen and write when given a string of text.
The robot's handwriting is based on a grid in which each letter is created as a
result of horizontal and vertical lines.

**Note** This functionality is being re-implemented. See https://github.com/gunthercox/Salvius/issues/5 for details.

### Object recognition

This includes face recognition, object tacking and learning to recognize new items.
Salvius currently does not have the ability to do this, however there is plans
to implement this in the future.

## Notes

#### SSH into Rapsberry Pi

- ```ssh pi@192.168.1.4``` (Your local ip may differ).
- The default password is ```password```.

#### Instlling psutil

The python package `psutil` is used to display various system statistics.
To use install this package you will need to run `sudo apt-get install python-dev`.

#### Running on Pi from a flash drive

1. In Ubuntu `cd` into `/media/user_name/disk_name` to get to the content on the flash drive.
2. Log in to http://routerlogin.net/ to get a list of the ips of connected devices.
3. `ssh pi@192.168.1.2`
4. Mount the flash drive using `sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt`
5. Then `cd` into `/mnt/salvius`
6. Run the server using `python salvius.py runserver`
7. In a browser navigate to `192.168.1.2:8000`

## Contributors
This project has been made possible with funding from the following sources:
Jennifer Cox, Adam Iredale, Janet Wise, Glen Zenor, Boris Hofer, 
Señora Alderperson, Wilbraham Music, Chris Cox, June Cox, Rantz, Yuri Yerofeyev
