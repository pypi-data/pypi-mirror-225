# Trust Platform Design Suite - Usecase Help - IP Protection

This document helps to understand Pre and Post steps of Usecase transaction diagram.

## Setup requirements
 - [EV76R77A](https://www.microchip.com/en-us/development-tool/EV76R77A)
 - [MPLAB X IDE](https://www.microchip.com/en-us/development-tools-tools-and-software/mplab-x-ide) v6.00 or above

## Pre Usecase transaction Steps
 - Connect EV76R77A board to PC running Trust Platform Design Suite. It is required to connect both TARGET USB and DEBUG USB to PC.
 - Ensure *MPLAB X Path* is set in *File* -> *Preference* under *System Settings*. This helps
    - To program the Usecase prototyping kit to factory reset application by TPDS
    - To open the embedded project of the Usecase
 - Note that *~/.trustplatform/pic32cmls60_ip_protection* is the **Usecase working directory**. It contains the resources generated during transaction diagram execution.
    - ~ indicates home directory.
        - Windows home directory is \user\username
        - Mac home directory is /users/username
        - Most Linux/Unix home directory is /home/username


## Post Usecase transaction Steps
On completing Usecase steps execution on TPDS, it is possible to either run the embedded project or view C source files by clicking *MPLAB X Project* or *C Source Folder* button.

- Once the Usecase project is loaded on MPLAB X IDE,
    - Set the project as Main -> right click on Project and select *Set as Main Project*
    - Set the configuration -> right click on Project, expand *Set Configuration* to select *default*
    - Build and Program the project -> right click on Project and select *Make and Program Device*
- Log from the embedded project can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1

