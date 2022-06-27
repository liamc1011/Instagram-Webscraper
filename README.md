# Instagram Webscraper

See who doesn't follow you back on Instagram! 
<br> This program works by having the user log in to their account on the Instagram website, 
then scraping their follower and following lists and comparing the differences between the two. 
A table will be generated showing everybody associated with your Instagram account, whether they follow you, and whether
you follow them.
<br><br> I decided to go the webscraping route to do this since Instagram's API is extremely limiting, and doesn't allow for
access to this kind of user data anymore (see the [Cambridge Analytica](https://techcrunch.com/2018/04/04/facebook-instagram-api-shut-down/) scandal).
However, webscraping has its unfortunate limitations. 
Right now, Instagram Webscraper is not optimized to handle accounts with large follower/following lists 
(I would say anything >2000 followers/following).
This is due to the nature of webscraping and having to scroll on the website in order to see the accounts, as well
as the fact that Instagram just adds accounts to the DOM and never removes elements (I think) 
which results in a sluggish page when you have so many DOM elements. 

-------

## Getting Started

Start by cloning this repo: 
```console
git clone github.com/liamc1011/Instagram-Webscraper
```

Install dependencies: 
```console
pip install -r requirements.txt
```

You will need to have [Google Chrome](https://google.com/chrome) installed on your local machine. 
<br> You will also need a [Chromedriver executable](https://chromedriver.chromium.org/downloads) for this to work. 
Locate and download the correct Chromedriver version for the version of Chrome that you have on your local machine. 
Unzip the download and place the executable in the folder in this repo titled `chromedrivers`

> To find which version of Chrome you're using, type `chrome://version` in the Chrome search bar.
> <br> Linux users can also do: 
> ```console
> google-chrome --version 
> ``` 

## Usage
```console
python3 main.py [options]
```
> `[options]` are optional. See below for explanation on when you might want to use them.
> 

By default this will output to the console. If you want the output in a file instead:
```console
python3 main.py [options] > file.txt
```

#### Options
- `--tfa` : use if two factor authentication is enabled for your Instagram account
- `--debug` : use if you want to print out the current list length as users are scraped (useful for debugging purposes)
- `--head` : use if you want to open Selenium in headful mode (see the action happening!). Default is headless mode.

## Troubleshooting
For macOS users, the first time you attempt to open the Chromedriver executable you may run into the following error:
> App can’t be opened because it is from an unidentified developer.
> 
To fix this, locate the Chromedriver executable in Finder and right click on it, then click "Open". 
You will get a message like this: 
> “chromedriver” is an app downloaded from the Internet. Are you sure you want to open it?
> 

Click OK. This should start the Chromdriver executable in Terminal. 
Once the Chromdriver executable has started successfully, then you can terminate the process.
Running Instagram-Webscraper should not cause this error now.