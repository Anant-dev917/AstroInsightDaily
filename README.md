# AstroInsightDaily
A web application for the latest astronomy news from various sources and your daily fill of high definition deep space pics straight from NASA, and the story behind it.
The web application displays latest news articles from different websites under the 'AstroInsightDaily' API. There's also a webpage dedicated to NASA's picture of the day, which displays a new picture of the universe daily alongwith a brief explanation of the picture by a professional astronomer. All this is taken from NASA's APOD API from NASA Open API website. You'll have to login to receive your own API key. Finally, the application also has basic sign-up and login features with database support. In fact, signed-in users have the option to "save" any news article they're reading, such that they can continue reading it in their profile section later. This news article is saved in a separate MongoDB collection. Each user will have their article stored in a separate document under their unique username, so you can save as many news articles as you want across multiple users.

This project is made using the flask framework. You need to set up a virtual environment before downloading flask and any other necessary packages. I used MongoDB for database, but you're free to use any database you're comfortable with. However, if you want to use MongoDB, you'll have to create an account on MongoDB atlas website. From there, you can follow the steps to download MongoDB compass GUI for your desktop and start using the database.

Certain parts of the project utilise flash messages for displaying user error. The HTML files 'base.html' and 'message.html' are used for that purpose specifically.

'message.html' retreives the error message specified by you from your python file, and displays it on the webpage. The 'base.html' file contains the basic HTML layout for the flash message with bootstrap, javascript and CSS. You can customize 'message.html' file to change the theme of the flash messages as per your vision. 

Additionally, the 'home.htm' homepage file for the web application utilises javascript's 'jQuery' library to pass on the clicked news article info from the webpage to the flask endpoint.   




This project started out as part of a flask learning course I was taking, but I was unsatisfied with the project I had done there. So what started out as a basic microblog web application turned into this in little over a month's time. The project itself is not exactly a novelty, but the code is mine and so is the web layout. This project helped me feel more comfortable with flask and HTML/CSS and was created for both as a learning project and for employment purposes. Feel free to use it as part of your academic project, for learning, or even improving upon it to create your own application.
