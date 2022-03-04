# back-test-unitaire-myran-perales

Lancer le projet : docker-compose up  
Accéder au container : docker exec -it myran-perales-backend-container /bin/bash  
Créer les migrations (elles devraient déjà être crées, mais au cas où) : python3 manage.py makemigrations  
Exécuter les migrations : python3 manage.py migrate  
Créer un superuser (pour accéder à l'admin) : python3 manage.py createsuperuser  

Lancer les tests (sans coverage) : python3 manage.py test  
Lancer les tests (avec coverage) : coverage run --source='.' manage.py test  
Lancer les tests (en sauvegardant la BBD vide, pour éviter de la recréer à chaque nouvelle commande de test) : coverage run --source='.' manage.py test --keepdb  
Lancer les tests d'un dossier précis : coverage run --source='.' manage.py test api.tests.unit_tests  
Lancer un test précis : coverage run --source='.' manage.py test api.tests.unit_tests.test_services.TestServices.test_get_request_to_rick_and_morty_api  

Voir le coverage en console : coverage report  
Voir le coverage en html : coverage html (puis ouvrir htmlcov/index.html)  

N.B : La requête à l'api Rick&Morty est très longue et très gourmande.   
Je l'ai mise dans la liste des products pour pouvoir vérifier les nouveaux produits de l'api externe, mais j'ai finis par la mettre en cache, pour gagner du temps.  

Routes : 
- http://127.0.0.1:8000/admin/
- http://127.0.0.1:8000/api/products (GET only)
- http://127.0.0.1:8000/api/products/{id} (GET only)
- http://127.0.0.1:8000/api/cart (GET, POST and DELETE)

Enjoy !
