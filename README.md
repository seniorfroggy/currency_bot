# Currency bot
## Description
This is a telegram bot to get Central Bank of Russia currency rates in json format.
## Relevance
Sometimes there is a need to quickly get currency rates, and a convenient bot interface and file format will help you to do it. 
## Usage:

**To use the project, follow the attached instructions:**

1. Create a folder with the selected name(*currency_bot* in my case) and clone this repository there:
```
mkdir currency_bot
cd currency_bot
git clone git@github.com:seniorfroggy/currency_bot.git
```
2. After that, go to the project folder and switch to the "main" branch:
```
cd currency_bot
git checkout main
```
3. To use the project, you need to install all the modules used in it, it is recommended to use a virtual environment:
>  ```python -m venv venv```  
> For Linux and MacOs:  
> ```source venv/bin/activate```  
> For Windows:  
> ```venv\Scripts\activate.bat```
```
pip install -r requirements.txt
chmod +x main.py
```
4. Starting the bot: 
```bash
./start.sh "your token"
```
