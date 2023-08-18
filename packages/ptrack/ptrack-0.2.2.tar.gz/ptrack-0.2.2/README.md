# P-Track - Progress Tracker

### Welcome to ptrack, a powerful and user-friendly CLI utility for tracking the progress of your file operations.
### Designed to be as concise, efficient and performance-optimized, ptrack works swiftly and accurately, while providing insight into the progress of the task at hand.

*Version: 0.2.2*

***

![Welcome to P-Track](./.gitlab/media/main.gif)

## Key Features

+ Progress Bar: ptrack comes equipped with an aesthetically pleasing progress bar that updates in real-time, giving you a visual representation of your ongoing file operation.
+ Verbose Mode: If you prefer a more in-depth perspective, ptrack has a verbose mode which displays detailed information about each file being processed.
+ Copying and Moving Files: ptrack supports both copying and moving files on any unix-like opperating system, including Linux, macOS, and BSD.
+ Downloading Files: ptrack can be used to download files from specified URLs. It will display the progress of the download in real-time, and will also display the download speed.
+ Interruption Handling: ptrack is built to respect your system's interruption signals. It will promptly stop operations when such signals are received, reducing the risk of data corruption.
+ High Performance: Above all, ptrack stands out for its speed and accuracy. It ensures your file operations are executed swiftly and with a high degree of precision.


## Installation:

### **ptrack** can easily be installed from various platforms:

### **PyPI**:
    pip install ptrack

### **Conda**:
    conda install -c concise ptrack

### **Arch User Repository (AUR)**:
#### For Arch Linux users, ptrack is available from on the AUR for all Arch or Arch based distro with the help of your favorite AUR helper, eg:
    yay -Sy ptrack

### **From Source**:
#### If you prefer to install from source, clone this repo, cd into it and run:
    pip install -e .

    # or python3 ./setup.py install



# Usage

The basic usage of ptrack isvery simple:

`ptrack [-h] [-v] [-c] [-m] [-d] [-V] [SOURCE...] [DESTINATION]`

```bash
### Downloading Files
  ptd [OPTIONS] URL(S)                 ( or ptrack -d URL(S) )

### Copying Files:
 ptc [OPTIONS] SOURCE... DESTINATION   ( or ptrack -c SOURCE... DESTINATION )

### Moving Files:
  ptm [OPTIONS] SOURCE... DESTINATION  ( or ptrack -m SOURCE... DESTINATION )
```

Refer to the User Guide for more detailed instructions and use-cases.


## Options:

* -h, --help      show this help message and exit
* -v, --verbose   verbose output
* -c, --copy      copy files (You can use `ptc` instead of `ptrack -c`)
* -m, --move      move files (You can use `ptm` instead of `ptrack -m`)
* -d, --download  download files (You can use `ptd` instead of `ptrack -d`)
* -V, --version   show program's version number and exit


![Regular Copy](./.gitlab/media/copy.gif)

![Regular Copy](./.gitlab/media/download.gif)

![Verbose Copy](./.gitlab/media/vcopy.gif)


## License
ptrack is open source and licenced under the MIT/X Consortium license

## Support
If you encounter any problems or have suggestions for ptrack, please open an issue on GitLab. We value your feedback and will respond as quickly as possible.


