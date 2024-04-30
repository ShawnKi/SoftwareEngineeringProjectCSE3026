Welcome to our fitness tracking app!
To get started, go to https://fitness-app-image-6vh2ppreea-uc.a.run.app
We also host the website on the domain chasmfit.com, but as we are making use of Google's experimental features, sometimes this version will not load. Try turning off vpns or using a different browser if this one gives you issues. 
For non logged in users, we offer a simplified experiance, with a browsable selection of workouts (We used Canva to find simplfied and easy to understand images for our workout selection). 
Once you log in, you can take our quiz, which will ensure help us generate a customized plan for you. Try browsing our workouts page and seeing what workouts you want to add yo your plan. You can either build a custom schedule on our schedule page by either dragging and dropping the workouts, or by having us auto-generate one for you. 
You can then go to our planner to see the workouts for that day, and check of the ones you've completed. 
You can also customize your profile by easily changing your profile picture and personal details from our profile page. 

Technical implementation:
We use python flask to manage the backend of our app. We use a mySQL database to manage user data. All userdata is stored in a json string and then loaded into individual html pages to load content for those pages. We modify individual parts of this JSON string when the user givs certain input. 
Inside the html pages, we use javascript functions to handle dynamic elements of our website, and we use CSS to style our pages. 

Testing:
In order to test our website, we would test new features by testing a range of possible inputs, both ones that are likely to be inputed by a user and ones that may be put in maliciously. We testing SQL injection on our signup and login pages, and we ensure that we parameterize inputs before sending requests to the mySQL database.
We also used GPT4 to analyze certain functions in both app.py and the HTML files to provide testing input to ensure that we can handle all types of user input.

Development lifecycle:
We followed a loose verison of the AGILE software development lifecycle, with planning the features we wanted to implement in a given week, how we would design and connect them. We would then implement these features and upload the individual changes to seperate github branches. After testing and review, we would merge these changes, and then deploy these changes. When planning new features, we would also examine old features that needed to be updated. This lifecycle allowed us to make incremental changes while constantly ensuring an intuative and accessable UI.

Deployment:
We use AWS to host the website and Google features to have our domain hosted with chasmfit.com. We dockerized our core files to ensure easy updates and testing. 

Known issues:
- Chasmfit.com will sometimes go down and not be accessble by certain IPs. After extensive testing we concluded this was a quirk with Google's domain mapping feature, and we could not fix it on our end.
- The sets and reps for the planner will sometimes not line up with those in the schedule. This is due to loading in only certain parts from the userdata. We concluded that this issue only has a minimal impact on the user experiance and thus we focused our efforts on more critical bugs. 
