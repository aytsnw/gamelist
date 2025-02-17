# Gamelist

#### Video Demo: https://youtu.be/8h5I1SlaXJI?si=wRyMIPVRlGR4Uax_

#### Description:

Gamelist is as web application in which the users are able to rate and review the games they have played, classifying them according to gameplay status (playing, finished or wishlist), as well as to have a look at how a given game is performimng review-wise amongst other Gamelist users and general game information.

### Directory breakdown

The application was written using Flask framework and flask-session module, as the directory formatting suggests, and works via support from **IGDB API**. The backend logic is written in the **"app.py"** file, which imports **"helpers.py"**. The route and requests management is being handled in **"app.py"**, whereas data storing and manipulation can be found mostly within the helper functions. The language for querying the database (stored in the file **"games.db"**) is **Sqlite**, and the **"SQL"** module from **CS50's course** is being used to operate the queries via the method ".execute()" applied to the database ("db") object. **"flask_session"** directory works to store users session ids. All the requirements/dependencies are written within **"requirements.txt"**. **"templates"** directory stores **"layout.html"** alongside all the other dynamically generated templates which extend **"layout.html"** via **Jinja** when returned by the app routes. **"static"** directory stores all the static resources such as **JavaScript** files, a **CSS** file (**"styles.css"**) (both being referenced within **"layout.html"**'s header) and imagery resource ("stored in a nested dir. called **"resources"**).

### Routes/HTML files

- **Index (login required):** App's homepage. It displays two containers, one with the games you have reviewed (ranked), including your rating and the (optional) commentary, and another with the website's top rated games and their respective ratings. These two containers are clickable, redirecting the user to their related pages (**My list** and **Global Chart**). *[HTML file: "index.html", route: "/index"]*

- **Login:** User login interface. From here the user is able to go to the register page if not logged in yet. *[HTML file: "login.html", route: "/login]"*

- **Register:** Registering page. *[HTML file: "register.html", route: "/register"]*

- **My list (login required):** Here the user have acess to the full list of the games they reviewed, separated by gameplay state (finished, playing and wishlist). As on **Index** page, the ratings are also displayed. From here the user is able to acess the **Game** page related to each of the games displayed, as well as to remove a game from their list and update their reviews (as by redirecting to **Game** page) *[HTML file: "mylist.html", route: "/mylist"]*

- **Search (login required):** The results page displayed when the search button is clicked, returning clickable results that redirects the user to the associated **Game** page. Some information about the games is already available here, such as the related genres. *[HTML file: "search.html", route: "/search"]*

- **Game (login required):** On this page there is all the information about the game that Gamelist gathers from the IGDB API and displays to the user. Additional features from the app on its own database are the user rating (if there is any) and commentary review, plus the website's rating for that game (calculated using an average score of all Gamelist users). *[HTML file: "game.html", route: "/game"]*

- **Global Chart (login required):** A page that displays a table with the top 15 Gamelist games sorted by rating. Since the page only comports 10 titles at once, the application implements a navigating system by displaying buttons that allow the user to from one index to the other. *[HTML file: "global_chart.html", route: "/global_chart"]*

- **Settings (login required):** A simple account management page. Here, the user is able to change their passwords or to logout (as by redirecting to **Logout** route). *[HTML file: "settings.html", route: "/settings"]*

- **Internal API (login required):** The route that supports the dynamic result-box via JS, displayed when the user types in the search bar. *[HTML file: None, route: "/api/searchbar"]*

- **Logout:** Logout route. Doesn't display any documents. *[HTML file: None, route: /logout]*

### Javascript files

- **rating_color_script.js:** A script to change the background color of the containers that display ratings, according to the value it contains. If more than or equal to 8 it is set to green, if below 8, it is set to yellow and, if below 3, it is set to red.

- **results_box_close.js:** A script to close the dynamic result box of the search bar (displayed when the user is typing), which is triggered whenever the body (except for the search bar and result box) is clicked, implemented for UI quality purposes.

- **toggle_menu.js:** This script acts to display (or close) a micro-menu inside the navbar containing the "settings" and "logout" buttons, leading to **"/setting"** and **"/logout"** routes, respectively.

- **togle_menu_mobile.js:** Works similarly to "toggle_menu.js", but its purpose relies on the need to adapt the UI for mobile devices, hidding some buttons from the navbar, and displaying them whenever it's clicked.

- **search_bar_fetch.js:** This script uses the "fetch" feature from JS to request the internal API (route:"/api/searchbar") via GET with the current value of the search bar encoded in the URL (it will act as the Apicalipse query to the external API after handled inside the route function). The internal API then respods with a formatted response provided by IGDB API endpoint. In addition, the script displays a result box in real time with the data from the response, everytime the user changes the search bar content. To ensure it works properly, a timeout is set and cleared at each interaction, so the API is not flooded nor the script doesn't work as intended. It also has a feature that works similarly to the **"results_box_close.js"** file, hidding the result box when the user empties the input field.






