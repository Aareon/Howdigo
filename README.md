# Howdigo
A tool that streams project-related data from various web APIs to reports you can present to potential employers. 


You just finished your project? Well how'd it go?

You can say it went well and that you learned a lot while building it, but what did the public think of it? 
Would companies be impressed? 

Howdigo Report Builder can help you validate your project by backing it up with visualized data 
from various social/web platforms (Reddit only so far). Employers like being presented facts, and your data could be 
what separates you from those who only TALK about their projects. 


Step 1: Submit posts of your project in subreddit communities you think will value your project, 
      then give it a little time to allow people to see it and give feedback.

Step 2: Create a Reddit Application (Tutorial: https://www.youtube.com/watch?v=NRgfgtzIhBQ&t=445s) and insert your app's info 
        into 'report/api.ini' (don't worry about github, that's work in progress). 
        
Step 3: run 'pip install requirements' if you don't have all the dependencies (This was built w/ Python 3.6, but it may work 
      w/ other versions of Python as well).  

Step 4: Run 'python main.py' at the command line.  




Things you can help with: 

-finding a method to break out of the Reddit API streaming generator so users don't have to restart the app everytime 
 they want to build a new report.

-scaling this tool to work w/ Github, Facebook, YouTube, Google, Twitter, & other web APIs where projects 
                can be shared. 
-making more models to visualize data streamed from the APIs. 
