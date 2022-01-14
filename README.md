## Projet

Pour répondre à un entretien pour un stage de fin d'étude, j'ai besoin d'effectuer ce projet en 1 semaine pour mettre en place une solution de classification video grâce à de l'IA disponible grâce à une API REST.

## IA

Le model que j'ai choisi a été trouver sur ce repo : 
https://github.com/naviocean/pytorch-inception
Je l'ai modifié pour essayer de fair un model Two-streams

Recommended :
Python version : 3.8.6
Package Require See : 
IA/requirements.txt


## Dataset 

Le dataset est téléchargeable ici : https://www.merl.com/pub/tmarks/MERL_Shopping_Dataset/

J'utilise le fichier create_dataset_flux.py pour générer le dataset pré-traité


## API 

Pour l'instant j'ai fait une API en typescript : 

Documentation de l'api ==> http://localhost:9000/documentation (Open-api)


## Pour le lancer : 

cd .../Prod_cali
docker-compose build
Docker-compose up 

## Pour tester : 

Vous pouvez utilisez postman pour tester l'API:
http://localhost:9000/documentation
http://localhost:9000/api/ping
http://localhost:9000/api/version
http://localhost:9000/api/upload
http://localhost:9000/api/result

Et voilà ! :) 

