# Installation

**Note:** the following commands are for Ubuntu-like distributions.

First of all we need to install pip, the Python packages manager.

``sudo apt install python3-pip``

Now we need to install *pew* to manage our virtual enviroments (*venv* from now on).

``pip3 install install pew``

After this, we need to create the *venv* which will host our project:

``pew new <name>``

Now we are ready to install the requirement via the requeriments.txt file:

``pip3 install -r requeriments.txt``

Once *pip* finish the installation we are ready to clone the repository and start working :)