# Photon-Project-Team-6

## Team Members

| Real Name         | Github Username |
|:-----------------:|:---------------:|
| Adam Wilson       | awilso14        |
| Matthew Senetho   | Mearion         |
| Sebastian Cabrera | BurstingMocha85 |
| Evan Gassaway     | evangassaway25  |

## Instructions to run the project

### 1. Prerequisites and Required Installations
* Debian Virtual Machine
* PostgreSQL (This is already installed on the Virtual Machine)
    * Database name: photon
    * Table name: players
* Any version of Python 3
* Git
* Required Python Libraries (these will be installed by running install.sh in step 3)
    * tkinter
    * pygame
    * psycopg2-binary
    * pillow

### 2. Clone The Repository
* To clone this repository to the virtual machine run these commands:
    * git clone https://github.com/UARKTeam6/Photon-Project-Team-6.git
    * cd Photon-Project-Team-6

### 3. Setup and Install Required Libaries
* These commands will install the required Python libraries:
    * chmod +x install.sh
    * ./install.sh
         * Password: student

### 4. Running the Photon Game
* Use the following command to run the game
    * python3 main.py
### 5. Additional Notes and Gameplay
* The game uses UDP sockets for communication:
    * Broadcast: 0.0.0.0 :7500
    * Receive: 127.0.0.1 :7501
* You will be greeted by a splash entry screen for approximately 3 seconds
* Next you will see a player entry screen and fill in the player id number
    * To clear entries press f12 and to start game press f5
* After starting the game you will see the play action screen
* Once the game ends you can press f1 to clear player data and return to the player entry screen


