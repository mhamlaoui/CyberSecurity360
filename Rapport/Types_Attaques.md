# Types d’Attaques : 

## DDoS (Distributed Denial of Service)
![DDoS](Divers/DDos.png)

### Définition
Une attaque en déni de service ou en déni de service distribué (DDoS pour *Distributed Denial of Service* en anglais) vise à rendre inaccessible un serveur par l’envoi de multiples requêtes jusqu’à le saturer ou par l’exploitation d’une faille de sécurité afin de provoquer une panne ou un fonctionnement fortement dégradé du service.

### Comment ça fonctionne ?
Les attaquants créent un **botnet** en infectant des appareils connectés (PC, IoT, routeurs…) avec des malwares. Ce réseau, contrôlé à distance, sert à lancer des attaques DDoS en inondant une cible de trafic.

Comme dans *Game of Thrones*, chaque bot peut en infecter d'autres. Certains louent ces botnets via des services d'« attaque à louer » pour permettre à d'autres de lancer des DDoS sans compétences techniques.

### Types d’attaques DDoS

- **Attaques volumétriques** : saturent la bande passante avec un très grand volume de trafic  
  *Exemples* : UDP Flood, ICMP Flood, attaques par réflexion (CLDAP, Memcached).
  
- **Attaques de protocole** : exploitent des failles des protocoles réseau pour épuiser les ressources  
  *Exemples* : SYN Flood, Ping of Death, Smurf.
  
- **Attaques applicatives (couche 7)** : ciblent des applications web avec des requêtes légitimes en apparence  
  *Exemple* : HTTP/HTTPS Flood.

### Se protéger

Les services de lutte contre les attaques DDoS sont fournis par des prestataires spécialisés qui détectent et bloquent rapidement le trafic malveillant, souvent en quelques secondes. Face à l’évolution constante des attaques, ils doivent investir régulièrement dans leurs capacités de défense.

#### Principaux types de protection

- **CDN (Content Delivery Network)** : filtre les attaques en bordure du réseau en rejetant le trafic non Web (non HTTP/HTTPS). Il agit comme un proxy entre les utilisateurs et les sites protégés, actif en continu.

- **Nettoyage cloud** : redirige le trafic vers des centres de traitement via BGP ou DNS. Ce système protège tous les ports, protocoles et applications, et peut être activé à la demande ou de façon permanente.

- **WAF (Web Application Firewall)** : protège la couche application (couche 7) contre les attaques ciblant les requêtes HTTP (GET/POST).

- **Protection sur site** : repose sur des équipements installés dans le réseau de l’entreprise. Utile pour les attaques discrètes ou quand une faible latence est essentielle (ex : jeux en ligne, visioconférence).

- **Protection hybride** : combine défense locale (pour les attaques légères) et cloud (pour les attaques massives).

- **Signalement cloud** : permet aux équipements sur site de transmettre automatiquement les informations de l’attaque aux centres cloud pour une réponse rapide.



## Phishing
![Phishing](Divers/Phishing.png)

### Définition
Le terme **phishing** fait référence aux tentatives de vol d'informations sensibles, telles que des noms d'utilisateur, mots de passe, numéros de carte bancaire ou d'autres données confidentielles, dans le but de les utiliser ou de les vendre.

L’attaquant se fait passer pour une source de confiance avec une demande alléchante, attirant ainsi la victime, à la manière d’un pêcheur utilisant un appât.

### Comment ça fonctionne ?
Dans une attaque typique, le criminel collecte les coordonnées d’une ou plusieurs cibles, puis envoie des messages de phishing par **email** ou **SMS**. 

L’attaquant joue souvent sur un **sentiment d’urgence** pour pousser la victime à :
- fournir des données sensibles,
- ou cliquer sur un lien frauduleux.

Ce lien mène généralement à un **faux site Web**, conçu pour :
- voler des identifiants,
- ou accéder à des données confidentielles.

#### Méthodes utilisées pour tromper la victime :
- Une adresse email semblant légitime (ex. domaine très proche d’une entreprise connue),
- Un site web ressemblant parfaitement à celui d'une entreprise réelle,
- Un email bien rédigé, avec des logos ou éléments visuels authentiques.

### Types d’attaques phishing

- **Spear phishing** : attaque ciblée sur une personne précise avec des données personnalisées.
- **Whaling** : forme de spear phishing visant des dirigeants (PDG, DSI...).
- **BEC (Business Email Compromise)** : usurpation d’un cadre pour détourner des paiements.
- **Clone phishing** : duplication d’un email légitime, avec liens/pièces jointes malveillants.
- **Vishing** : escroquerie par appel vocal à l’aide de numéros usurpés.
- **Raquettes** : envoi de faibles volumes de messages depuis des domaines/IP multiples pour contourner les filtres anti-spam.

### Se protéger

Même si des **employés bien formés** sont la meilleure défense, plusieurs mesures techniques peuvent renforcer la sécurité :

- **Filtrer les spams** : utiliser des outils de filtrage pour bloquer les emails suspects.
- **Mettre à jour les logiciels de sécurité** : appliquer les correctifs et renforcer les politiques de mot de passe.
- **Activer la MFA (authentification multifactorielle)** : ajoute une sécurité supplémentaire en cas de vol d'identifiants.
- **Sauvegarder et chiffrer les données** : permet de limiter les conséquences en cas d’attaque.
- **Former les employés** : sensibiliser aux dangers des liens et pièces jointes suspects.
- **Bloquer les sites malveillants** : utiliser des filtres web pour restreindre l’accès aux sites à risque.


## SQL Injection
![SQL](Divers/SQL.png)

### Définition
Les attaques par **injection SQL** exploitent les failles de sécurité d’une application qui interagit avec des bases de données.

L’attaque consiste à **modifier une requête SQL en cours** en y injectant un morceau de requête malveillant, souvent via un formulaire, afin de :
- accéder à la base de données,
- modifier ou supprimer des données,
- compromettre la sécurité du système.

### Comment ça fonctionne ?
Une application web insère directement des données saisies par l'utilisateur dans une requête SQL **sans vérification ni filtrage**.

Un attaquant peut injecter des **commandes SQL malveillantes** dans des champs de saisie (ex : formulaire de connexion, barre de recherche), en utilisant :
- des caractères spéciaux : `'`, `"`, `--`, `;`
- des mots-clés SQL : `SELECT`, `DELETE`, `OR 1=1`, etc.

#### Exemple :
```sql
SELECT * FROM utilisateurs WHERE nom = '' OR '1'='1' ;
```
Cette requête renverra tous les utilisateurs car `'1'='1'` est toujours vrai, ce qui peut permettre de contourner l’authentification ou d’accéder à des données sensibles.

---

## Les types d’attaques SQL Injection

### 1. SQLi en bande

- **Basé sur les erreurs** : exploite les messages d’erreur de la base.
- **Basé sur UNION** : utilise l’opérateur `UNION` pour extraire des données.

### 2. SQLi aveugle (inférentiel)

- **Booléen** : déduit les infos selon si la réponse change ou non.
- **Basé sur le temps** : mesure les délais de réponse pour obtenir des infos.

### 3. SQLi hors bande

- Exploite des fonctions du serveur (comme DNS ou HTTP) pour exfiltrer les données sans réponse directe.

---

## Se protéger

- ✅ Utiliser des **requêtes préparées** (paramétrées).
- ✅ **Valider et filtrer** toutes les entrées utilisateur.
- ✅ **Limiter les droits** du compte SQL utilisé.
- ✅ **Ne pas afficher les erreurs SQL** aux utilisateurs.
- ✅ Utiliser un **pare-feu applicatif (WAF)** si possible.



## Ransomware
![Ranso](Divers/Ranso.png)


### Définition
Les **rançongiciels** (ou **ransomwares**) sont des logiciels malveillants qui bloquent l’accès à un ordinateur ou à des fichiers en les **chiffrant**, puis réclament à la victime le **paiement d’une rançon** pour en retrouver l’accès.

L’infection peut survenir :
- après l’ouverture d’une **pièce jointe piégée**,
- en cliquant sur un **lien malveillant**,
- en **naviguant sur un site compromis**,
- ou suite à une **intrusion** dans le système.

### Comment ça fonctionne ?
1. L’attaquant **infecte un système** (souvent par email, lien ou faille de sécurité).
2. Les fichiers sont **chiffrés**, devenant inutilisables.
3. Une **demande de rançon** est affichée, souvent en **cryptomonnaie**, pour fournir la clé de déchiffrement.

⚠️ **Même en payant, rien ne garantit** que les données seront récupérées.

### Types d’attaques par ransomware

- **Chiffrement** : les fichiers sont chiffrés et une rançon est exigée pour les déchiffrer.
- **Verrouillage** : l’accès à l’ordinateur ou au système est complètement bloqué.
- **Extorsion (double extorsion)** : l’attaquant menace aussi de **divulguer les données volées**.
- **Propagation réseau** : le ransomware se propage à travers un **réseau** pour infecter d'autres machines.
- **Mobile** : cible les **appareils mobiles**, en les chiffrant ou les bloquant.
- **Serveurs** : attaque les **serveurs d’entreprise** ou **cloud** pour interrompre les opérations.

### Se protéger

- **Ne cliquez jamais** sur des liens suspects (emails, sites inconnus).
- Ne **partagez pas** d'informations personnelles avec des sources non fiables.
- **N’ouvrez aucune pièce jointe douteuse**, surtout celles contenant des macros.
- **Évitez d’utiliser** des clés USB ou supports inconnus.
- **Mettez à jour** régulièrement le système et les logiciels.
- Téléchargez uniquement depuis des **sites fiables et sécurisés** (`https`).
- Utilisez un **VPN** sur les réseaux Wi-Fi publics.


## Malware
![Malware](Divers/Malware.png)

### Définition
Un **malware** (ou logiciel malveillant) est un programme conçu pour **infiltrer**, **perturber** ou **endommager** un ordinateur ou un réseau, généralement **à l’insu du propriétaire**.

Les cybercriminels utilisent les malwares pour :
- détourner un appareil,
- espionner les systèmes,
- corrompre, voler ou supprimer des données.

### Comment ça fonctionne ?
Une attaque par malware commence généralement par :
- l’exploitation d’une **vulnérabilité technique**,
- ou des techniques d’**ingénierie sociale** (liens ou fichiers piégés).

L’utilisateur est incité à **télécharger ou ouvrir un fichier malveillant**.

Une fois le malware exécuté, il peut :
- voler des informations,
- endommager des fichiers,
- ou permettre un **accès distant** à l’attaquant pour exploiter le système.

### Types d’attaques par malware

- **Virus** : se propage via des fichiers et infecte d’autres programmes.
- **Vers (Worms)** : se propagent automatiquement sur un réseau sans intervention humaine.
- **Chevaux de Troie (Trojans)** : se présentent comme des logiciels légitimes mais ouvrent un accès à l’attaquant.
- **Ransomware** : chiffre les fichiers et réclame une rançon.
- **Spyware** : surveille l’activité de l’utilisateur pour **voler des informations sensibles**.
- **Adware** : affiche des **publicités non sollicitées**, souvent accompagnées d’autres malwares.
- **Rootkits** : masquent des processus ou fichiers malveillants pour **éviter leur détection**.

### Se protéger

- Utiliser un **antivirus à jour** pour détecter et bloquer les malwares.
- Éviter les **liens et pièces jointes suspects** dans les e-mails ou messages.
- **Mettre à jour régulièrement** le système d’exploitation et les logiciels pour corriger les failles.
- Ne pas télécharger de fichiers depuis des **sites non fiables**.
- Ne jamais insérer de **clés USB inconnues** dans un ordinateur.
- Utiliser des **outils de sécurité réseau**, comme les **pare-feux** et les **VPN**, pour sécuriser les connexions.


## Man-in-the-Middle (MITM)
![MITM](Divers/MITM.png)

### Définition
Une attaque **Man-in-the-Middle (MITM)** se produit lorsqu'un **attaquant s'interpose secrètement** entre deux parties qui communiquent, dans le but :
- d’intercepter,
- d’espionner,
- d’altérer,
- ou de rediriger leurs échanges de données.

L'attaquant peut ainsi **voler des informations sensibles** (identifiants, données bancaires) ou **injecter des contenus malveillants** dans les communications, souvent **sans que les victimes ne s'en aperçoivent**.

### Comment ça fonctionne ?
L’attaquant peut :
- espionner les données échangées,
- les modifier,
- ou injecter du code malveillant.

Ce type d’attaque est particulièrement courant dans les environnements suivants :
- **réseaux Wi-Fi publics**,
- **connexions non sécurisées**,
- **sites web non vérifiés**.

### Types d’attaques MITM

- **Interception de communication** :  
  L’attaquant intercepte les données échangées entre deux parties (ex. : identifiants, messages, transactions).

- **Injection de contenu** :  
  L’attaquant modifie le contenu transmis (ex. : injection de code malveillant dans une page Web).

- **Attaque de redirection (DNS Spoofing)** :  
  L'utilisateur est redirigé vers un **faux site Web**, par usurpation d’adresse DNS.

- **Attaque par usurpation de session** :  
  Le pirate **vole un cookie ou un jeton d’authentification** pour se faire passer pour l’utilisateur légitime.

### Se protéger

- Utiliser des **connexions sécurisées (HTTPS)** pour chiffrer les données échangées.
- Éviter les **réseaux Wi-Fi publics non sécurisés**, surtout pour les transactions sensibles.
- **Vérifier les certificats SSL/TLS** des sites visités.
- Utiliser un **VPN** pour chiffrer les communications sur les réseaux publics ou non fiables.
- **Mettre à jour régulièrement** les logiciels pour corriger les failles de sécurité connues.
