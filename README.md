# BruteForceForm  

**DISCLAIMER: ANY MALICIOUS USE OF THE CONTENTS FROM THIS PROJECT WILL NOT HOLD THE AUTHOR RESPONSIBLE, THE CONTENTS ARE SOLELY FOR EDUCATIONAL PURPOSE**  

### How does it work?  

The program GETs the login page and saves all the gotten cookies. It then parses the HTML document and saves all the input fields with current values, thus, bypassing the [csrf validation](https://portswigger.net/web-security/csrf). After that it updates username and password fields with current guess. It then sends the request and checks the response against the `error_check`.  

### Usage  
* Usernames are taken from `username_file`  
* Passwords are taken from `wordlist_file`  
* Found username and passwords matches are saved in `output_file`  
* `target_url` is the url for GET request  
* `target_post` is the url for POST request  
* `username_field` and `password_field` are input field's names of username and password fields respectively, change them accordingly  
* `error_check` is the text the website returns upon unsuccessful attempt. This text should not be contained in the successful request   

**This program exploits primitive vulnerability and might not work on more advanced systems**  

The project is based on the book *Black Hat Python: Python Programming for Hackers and Pentesters* by Justin Seitz. The code was converted to Python 3 and modified to use Python's `requests` package. Functionality of searching for multiple usernames was also added.  

Code was implemented and tested with Python 3.9.2 on Debian 9.  