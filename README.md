# Keruusysteemi (KESY)

Keruusysteemi, "kesy", "KESY", "pickup system".
A personal project that consists of multiple repositories.

User (me) picks up a trash with a grabber. The collector takes a picture of the trash and uploads it to server along with location data and climate data.

The collector = Raspberry Pi with camera module, Sense Hat.

# kesy-receiver (this)

.. is only one of the few KESY repositories.

The repository contains code for the server that receives the data from the collector. Please note that this server does not expose any GET methods. 

The data is saved to a MySQL database.

The receiver might be referred as "master server" aswell.


### POST new Trash

```
POST {{host}}/api/v1/trash

{
    "uuid": "str(36) unique",
    "accuracy": "decimal(6,2) nullable",
    "latitude": "decimal(10, 8) nullable",
    "longitude": "decimal(11,8) nullable",
    "encodedImage": "base64 nullable"
}
```

Should be accessed from the Python that controls the camera.
Creates a new row to the master database. Also saves the image to `storage/images`.

New row = a new collected trash.

### PUT location data

```
PUT {{host}}/api/v1/trash

{
    "uuid": "str(36) unique",
    "accuracy": "decimal(6,2) nullable",
    "latitude": "decimal(10, 8) nullable",
    "longitude": "decimal(11,8) nullable",
}
```

Should be accessed from the kesy-collector Node.js.
Updates the given UUID row location data.

# Install

```
npm install
mkdir storage/images
touch .env
touch src/knexfile.js
```

## .env

```
NODE_ENV=development
PORT=3000

RPI1_USERNAME=foo
RPI1_PASSWORD=bar
```

## knexfile.js

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

## Usage

```
node src/server.js
```
