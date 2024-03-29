# BruteForceForm  

**DISCLAIMER: ANY MALICIOUS USE OF THIS PROJECT'S CONTENTS WILL NOT HOLD THE AUTHOR RESPONSIBLE, THE CONTENTS ARE SOLELY FOR EDUCATIONAL PURPOSES**  

### How does it work?  

The program GETs the login page and saves all the gotten cookies. It then parses the HTML document and saves all the input fields with current values, thus, bypassing the [csrf validation](https://portswigger.net/web-security/csrf). After that it updates username and password fields with current guess. It then sends the request and checks the response against the `error_check`.  

### Usage  
```
usage: ./BruteForceForm.py [-h] -u USERNAMES -w WORDLIST -e ERROR_CHECK [-o OUTPUT] [--post post url] [--username-field USERNAME_FIELD] [--password-field PASSWORD_FIELD]
                           [--tor]
                           target_url

Example commands:
  ./BruteForceForm.py <login_page_url> -u username_file.txt -w passwords.txt -e "password didn't match"
  ./BruteForceForm.py <login_page_url> -u username_file.txt -w passwords.txt --username-field user -e "password didn't match"
  ./BruteForceForm.py <login_page_url> -u username_file.txt -w passwords.txt --post <post_url> -e "password didn't match"

positional arguments:
  target_url            url of target

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAMES, --usernames USERNAMES
                        file with usernames
  -w WORDLIST, --wordlist WORDLIST
                        file with passwords
  -e ERROR_CHECK, --error-check ERROR_CHECK
                        error check that should be not be present in response body upon success and present upon fail
  -o OUTPUT, --output OUTPUT
                        file where found matches will be stored
  --post post url       url to post form (defaults to target_url)
  --username-field USERNAME_FIELD
                        name of username input field
  --password-field PASSWORD_FIELD
                        name of password input field
  --tor                 proxy the requests through tor
```

**This program exploits primitive vulnerability and might not work on more advanced systems**  

The project is based on the book *Black Hat Python: Python Programming for Hackers and Pentesters* by Justin Seitz. The code was converted to Python 3 and modified to use Python's `requests` package. Functionality of searching for multiple usernames, command line support and tor proxy option was also added.  

Code was implemented and tested with Python 3.9.2 on Debian 9.  
