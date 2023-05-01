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
