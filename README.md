# Epidemic-Coding
The code is run through the terminal using $python simulation.py, this will return both the plots created by the code and also a moving day by day heat map of how the virus has spread through the simulated population.

Before running the code make sure that you have matplotlib, numpy, pandas and random installed, otherwise you will run into errors when trying to run the code from the terminal.

Additionally, you may need to reinstall these packages if they haven't been installed correctly. If you run into errors from numpy, firstly run '$python -m pip install numpy', to check if you have it installed. If you have it installed, run '$python -m uninstall numpy' to uninstall it. Then run '$python -m pip install numpy' to reinstall it. For errors involving matplotlib, run '$python -m pip install matplotlib --force-reinstall --user', and the errors should be solved.

Running python simulation.py without any additional command line argument will run the code will the default values set for each variable.
Running $python simulation.py -h or $python simulation.py --help will run the help command, this will list all of the possible arguments to change the values of the variables.
The variables that will be listed are:
--Size, it will take an integer value and simulate a grid of size N x N, the default value for this variable is set as 40

--Start, it will take an integer value and use it as the value for how many people are infected at the start of the simulation,the default value for this variable is set to 2 

--Inf, infection chance, it will take a float(decimal) value and use that value for the chance of someone becoming infected when close enough to an infected individual, the deafualt value is set to 0.2

--Range, it will take an integer value and use that as how many squares in the grid the infection can travel to infect a new person, the default value for this is set to 2 

--Rec, recovery chance, it will take a float(decimal) value as the chance that a given infected individual will recover per day, the default value for this is set to 0.3

--Death, death chance, it will take a float(deciaml) value as the chance that an infected individual can die per day, the default value for this is set to 0.05

--Hosprate, it will take a float(decimal) value as the chance that an infected individual can be sent to hospital each day they are infected, the default value for this is set to 0.1

--Hospcap, hospital capacity, it will take a float(decimal) value and use it as the proportion of the of the total population that can be hospitalised before the hospitals are at capacity and can no longer help the patients, the default value for this is set to 0.05

--Demo, population demographic, this will take a string input of either 'S'(stationary - equal proportion of old and young people), 'C'(constrictive - more old people than young people), or 'E'(expansive - more young people than old people), the default demographic is 'S'

--Vac, vaccination proportion, it will take a float(decimal) value and use it as the proportion of the population that will recieve a vaccination, the default value for this is set to 0.25

--Proc, protection, it will take a float(decimal) value and will use it as the factor at wich the infection rate is divided by when an individual has been vacccianted, this is the only float value that does not have to be in the range between 0 and 1, the default value for this is 5

--Immune, it will take an integer value and use it as the amount of days that a person will remain immune from the virus once recovered, when this value is set lower than the amount of days the sim runs for this allows for 2rd and 3rd waves of infections, the default value for this is set to 1000

--Duration, it will take an integer value and use it as the ammount of days that the simulation will run for, the default value for this is set to 40

--File, it will take a string input and if given will use it to name the plot produced and save them to the current working directory instead of displaying the plots, there is no default input for this argument. When the file save option is used, the animation does not display, and only the plot will be saved in a file.

To run the simulation with differnt values for any of the variables run:
$python simulation.py --[the argument you want to change]=[the value you want to run the sim with]

For example:
running 
$python simulation.py --Size=25 
will run the simulation with a grid size of 25 by 25 instead of the default 40 by 40 

Multiple arguments can be changed at the same time, for example:
running 
$python simulation.py --Inf=0.6 --Death=0.3 --Duration=20 --File=Name
will run the simulation with an infection rate of 0.6, a death rate of 0.3, over a 20 day period and will save the plot as Name instead of displaying the plots and animation.

Note that the arguments are case sensitive, for example --size will not work as an argument but --Size will. This also applies to the inputs for the --Demo argument, it will only accept 'S','C' or 'E' the inputs given as lower case letters or any input that is not one of these 3 will not be accepted and will retun a message stating that only one of the 3 choices that are then listed will be accepted.

All float vlaues for inputs with the exception of --Proc will require values between 0 and 1, any value given in the arguments that is not within this range will result in an error message and will ask the user to input a new value for that specific argument before continuing,
for example:
$python simulation.py --Inf=2
will return a message saying that the value must be between 0 and 1 and will then ask for a new input of that value within the range specified, if the user tries to input an invalid value again the code will reject the value and ask again for a new input.

The float vlaue for --Proc will only accept values above 1, any value given in the arguments for this that is less than 1 will be rejected and will return a message asking for the input to be greater than 1 and will ask the user for a new input. If the new input is once again invalid it will return the same message and ask for a new value greater than 1. This continues until a valid value is inputted.

