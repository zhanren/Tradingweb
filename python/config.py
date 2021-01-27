import os

## App conf
name = "Trading Dashboard"

host = "0.0.0.0"

port = int(os.environ.get("PORT", 5000))

debug = False

fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

## File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"

## DB
