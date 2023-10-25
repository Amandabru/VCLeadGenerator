How to setup server

1. get a chromedriver and drop it into driver folder 
https://googlechromelabs.github.io/chrome-for-testing/#stable

2. add that driver to your PATH variable by opening paths and adding the whole path to /driver
```sudo nano /etc/paths``` might be in other spot on x86 macs and windows

3. install python stuff, pip3 install should work

might work

How to serve

install uvicorn and fastapi

````python -m pip install fastapi uvicorn[standard]````

then serve with

````uvicorn serve:app --reload````

then get data from db with

http://127.0.0.1:8000/fetch/[AMOUNT]
