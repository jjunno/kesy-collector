# Keruusysteemi (KESY)

Keruusysteemi, "kesy", "KESY", "pickup system".
A personal project that consists of multiple repositories.

User (me) picks up a trash with a grabber. The collector takes a picture of the trash and uploads it to server along with location data and climate data.

The collector = Raspberry Pi with camera module, Sense Hat.

# kesy-collector (this)

.. is only one of the few KESY repositories.

This repository contains code for the collector. The actual Trash -action (taking the picture, controlling the camera and Sense Hat) is Python.

This repository also includes a Node.js server with Express and HTTP. Since the RPI does not have any GPS or SIM module, we can connect it to a mobile phone hotspot. We need the network for data upload anyway, but we can also get the device location with HTTP.

The HTTP serves HTML and Socket.io to the mobile phone.

The Express listens a single route, which is being used in Python. When the camera takes the photo, this route is called. It requests the location data from the mobile phone. The data is also uploaded to the receiver.


# .env

```
ENV=development

#Show camera preview with few second delay before capturing the photo. Can only be used with ENV = development.
SHOW_PREVIEW=False

#Image settings
IMAGE_WIDTH=1920
IMAGE_HEIGHT=1080

#The path the captured image should be saved to.
#Without ending slash!
IMAGE_SAVE_PATH=/home/pi/Pictures

LOCAL_NODE_API_URL=http://localhost:3000/api/v1/clientLocation
RECEIVER_API_URL=http://host/api/v1/trash
RECEIVER_API_USERNAME=foo
RECEIVER_API_PASSWORD=bar

EXPRESS_PORT=3000
HTTP_PORT=8080
```

# knexfile.js

```
// Update with your config settings.

/**
 * @type { Object.<string, import("knex").Knex.Config> }
 */
module.exports = {
  development: {
    client: 'mysql2',
    connection: {
      host: 'localhost',
      port: 3306,
      user: 'username',
      password: 'password',
      database: 'database',
      dateStrings: true,
      typeCast: function (field, next) {
        if (field.type == 'TINY' && field.length == 1) {
          return field.string() == '1'; // 1 = true, 0 = false
        }
        return next();
      },
    },
  },
};

```

# Install

```
python3 -m venv env --system-site-packages
source env/bin/activate
pip3 install -r src/requirements.txt

npm install
mkdir storage/images
touch src/knexfile.js
```

# Usage

```
source env/bin/activate
python3 src/main.py

node src/server.js
```
