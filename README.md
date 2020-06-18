# CrappyScrapper
A simple facebook data scrapping tool, which allows to get all the friends of a person as a csv file
**Please note, that this tool will not work if your target hid has his/her friend list!**

# How it works?
Since Facebook has removed friends getter from their API, the way this tool works is by downloading the Facebook friends list into memory.
However Facebook has strong protection mechanisms from downloading the code of their pages by wget, for example and they also have it obfuscated.
As there is no way to download the page directly, this tool is implemented by famous atumation library **selenium** and uses Chrome to download the page with friend list manually.

# How to use it?
With the compiled version, the only requirement is to have Google Chrome installed. When you launch an application, 
just enter the Facebook id of the person, whom friend list you want to get and follow the straight forward instructions provided by the program.

**For non-compiled python version, you will need the following packages to be installed besides Chrome:**
 - html.parser
 - selenium
 - requests
 - time
 - os
 - pickle
 - getpass
 - translit
 - pandas
