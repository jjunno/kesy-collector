# kesy

Keruu Systeemi

Raspberry Pi #1 - Kerääjä
Roskapoimijaan liitettävä Rasberry Pi, jossa on ainakin kamera sekä mahdollisesti Sense Hat muun datan keräämistä sekä ohjaamista varten.
RPI#1 saa virtansa varavirtalähteestä.

Keräysprosessi
Kerätään roska, painetaan Sense Hatin painiketta joka ottaa poimijan piikeistä kuvan. Lisäksi tallennetaan Sense Hatista dataa, sekä mahdollisesti dataa mobiililaitteesta (jos RPI#1 on mobiililaitteen jaetussa verkossa kiinni).
Data voidaan joko tallentaa laitteen paikalliseen tietokantaan, joka synkronoidaan REST APIlla myöhemmin kotiverkossa taustajärjestelmään.

Taustajärjestelmä
Todennäköisesti VPS Ubuntu, jossa on kontitettu Node.js Express REST API sekä kontitettu nginx Vue 3 Vuetify.
Node.js ottaa RESTiä vastaan RPI#1:stä joko reaaliajassa tai manuaalisessa synkronoinnissa.
Data tallennetaan MySQL kantaan.

Node.js myös palvelee dataa Vue:lle, jota voidaan esitellä sivuston kävijöille.

INSTALL
python3 -m venv env --system-site-packages
source env/bin/activate
pip3 install -r src/requirements.txt

ENV=development

# Show camera preview with few second delay before capturing the photo. Can only be used with ENV = development.

SHOW_PREVIEW=False

# Image settings

IMAGE_WIDTH=1920
IMAGE_HEIGHT=1080

# The path the captured image should be saved to.

# Without ending slash!

IMAGE_SAVE_PATH=/home/keijo/Pictures

LOCAL_NODE_API_URL=http://localhost:3000/api/v1/clientLocation
RECEIVER_API_URL=http://192.168.1.4:3000/api/v1/trash
RECEIVER_API_USERNAME=foo
RECEIVER_API_PASSWORD=bar

EXPRESS_PORT=3000
HTTP_PORT=8080
