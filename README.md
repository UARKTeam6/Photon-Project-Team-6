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
* Required Python Libraries (these will be installed by running install.py in step 3)
    * <ins>__PLACEHOLDER for libraries we decide will be needed in install.py__<ins>

### 2. Clone The Repository
* To clone this repository to the virtual machine run these commands:
    * git clone https://github.com/UARKTeam6/Photon-Project-Team-6.git
    * cd Photon-Project-Team-6

### 3. Setup and Install Required Libaries
* This command will install the required Python libraries:
    * python3 install.py

### 4. Running the Photon Game
* Use the following command to run the game
    * python3 <ins>__PLACEHOLDER for either main.py or game.py whichever name we choose__<ins>

### 5. Additional Notes and Gameplay
* The game uses UDP sockets for communication:
    * Broadcast: 0.0.0.0 :7500
    * Receive: 127.0.0.1 :7501
* You will be greeted by a splash entry screen for approximately <ins>__PLACEHOLDER for # seconds we decide to show__<ins>
* Next you will see a player entry screen and fill in the player id number
    * To clear entries press f12 and to start game press f5
* After starting the game you will see the play action screen
* Once the game ends you can press f1 to clear player data and return to the player entry screen


