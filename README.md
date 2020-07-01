# description
this script does two things, reading temperature and humidity from a dht22 connected to your pi as well as writing it to a google spreadsheet.

## dht22 setup
this is described here [https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py]

## google sheets access
a basic authentification with readonly is described here and was used as template for this project
[https://developers.google.com/sheets/api/quickstart/python]
tbh: the authentification on the raspberry is a bit painful, because you have to broweser authenticate on the raspberry, which is very slow. be brave!
[https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append]
this shows how values can be appended to a spreadsheet.

### troubleshooting
it took me a while to figure out that the token.pickle file needed to be deleted for switching from readonly to full spreadsheet scope. this is because it contained the permissions associated with readonly. if the script does not find the `token.pickle` file, you will have to re-auth. see [https://stackoverflow.com/questions/38534801/google-spreadsheet-api-request-had-insufficient-authentication-scopes]
the credentials.json have to be in the root folder of the repo as well. you can obtain them via the quickstart url above.

## cron syntax
for every 5 minutes, this might wat you want:
`*/5 * * * * cd /home/pi/devel/dht22_to_spreadsheet; /usr/bin/python3 main.py >> /home/pi/devel/log.log 2>&1`
the `cd` is needed for the credentials and token file to be found..
