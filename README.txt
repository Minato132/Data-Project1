This is simple GitHub Repo that will host a local website showing Salary statistics for Software Developers from multiple countries.

The website contains an explore page with visual representations of the general statistics of the Salary, and a predict page which
allows you to calculate salary as a software developer based on certain parameters

The model was trained on data from the StackOverFlow 2020 Developer Survey.


To host the website:

  In PowerShell, load up the Repo using any IDE of your choice

  In the terminal, activate the virtual python environment using the activate script in the env folder
    A possible error that might result is the IDE failing to detect the virtual environment folder. 
    In this case, in each of the python files (app, predict_page, explore_page, ml), there is a line
      #! <directory>

    Make sure to replace the location of that directory with the Path to the python.exe file that is under
    the env file. 

  In terminal, run the command
    streamlit run app.py


Enjoy!
