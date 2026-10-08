# Sources : règles essentielles

Carte des sources, accès, nommage des bruts et en-tête des fichiers dérivés :
`procedures.md`, à lire avant toute récupération. Vérification et intégration :
`/veille` et `/maj-regles`.

- Officielle avant communautaire. En cas de contradiction, l'officielle l'emporte et la
  contradiction est signalée.
- Toute donnée communautaire porte la mention **communautaire** là où elle est consignée.
- Termes français officiels uniquement : jamais de traduction maison d'un nom anglais.
- Chaque donnée porte sa version et sa date de consultation ; git ne date que le fichier.
- Points, détachements, meneurs et appuis, options : uniquement par
  `outils/veille.py --extraire`, jamais recopiés à la main.
- Méfiance envers les PDF trouvés par recherche web : vérifier l'édition (`Last-Modified`,
  version) avant usage.
- Page inaccessible ou vide par `curl` ou WebFetch : réessayer avec Claude in Chrome
  avant de conclure à un échec.
- Ne jamais contourner une authentification, un paiement ou une protection anti-robot :
  consigner la limite et demander le document.
