0.Installer image docker
```
liliasfaxi/hadoop-cluster
```

1.Lancer le docker 
```bash
docker run -it liliasfaxi/hadoop-cluster /bin/bash
```

2.Faire les commandes
```bash
echo "127.0.0.1 hadoop-master" >> /etc/hosts
echo "127.0.0.1 hadoop-worker1" >> /etc/hosts
echo "127.0.0.1 hadoop-worker2" >> /etc/hosts
```

3.Installer Openssh si non présent
```bash
apt update && apt install -y openssh-server
```

4.Le run le ssh
```bash
service ssh start
service ssh status
```

5.Lancer le dfs
```bash
start-dfs.sh
start-yarn.sh
jps
```

---
Application WordCount

"WordCount!" est l'exemple typique de MapReduce, c’est le "Hello World!" de MapReduce et du calcul distribué!

Le Wordcount permet de calculer le nombre de mots dans un fichier donné, en décomposant le calcul en deux étapes:

- L'étape de Mapping, qui permet de découper le texte en mots et de délivrer en sortie un flux textuel, où chaque ligne contient le mot trouvé, suivi de la valeur 1 (pour dire que le mot a été trouvé une fois)

- L'étape de Reducing, qui permet de faire la somme des 1 pour chaque mot, pour trouver le nombre total d'occurrences de ce mot dans le texte.

* Tester Map Reduce En local
1- Ecrire votre programme mapper.py qui permet d’assurer le parsing de cette collection de mots et qui retourne un affichage comme suit:
```
echo "Hello Big Data, Hello Hadoop" |python.exe .\mapper.py
```
2- Ecrire votre programme reducer.py; la suite de l’algorithme Map/Reduce vu en cours.. vous aurez un affichage comme suit
```
echo "Hello BigData, Hello Hadoop" |python.exe .\mapper.py |sort |python.exe .\reduce.py
```


* Tester Map Reduce sur le cluseter HDFS:

Premiers pas avec Hadoop

Toutes les commandes interagissant avec le système Hadoop commencent par hdfs fs.
Ensuite, les options rajoutées sont très largement inspirées des commandes Unix standard.

- Créer un répertoire dans HDFS, appelé input. Pour cela, taper:
```
hdfs dfs -mkdir -p /input
```

- Copier le fichier à tester file1.txt dans ce nouveau dossier input crée dans votre HDFS
RQ: on suppose que vous avez stocké la collection de mots utilisée en local dans un fichier file1.txt
```
hdfs dfs -put C:/yourPath/file1.txt /input
```
ou aussi:
```
hdfs dfs -copyFromLocal C:/yourPath/file1.txt /input
```

- Verifier que votre fichier est bien copié dans le nouveau dossier /input
```
hdfs dfs -ls /input/
```

- pour afficher le contenu de votre fichier:
```
hdfs dfs -cat /input/file1.txt
```

- hadoop streaming
lancer le job sur le fichier file1.txt que vous avez chargé dans le répertoire /input de
HDFS. Une fois le Job terminé, un répertoire output sera :
```
hadoop jar hadoop-streaming.jar -input [fichier entree HDFS] \
-output [fichier sortie HDFS] \
-mapper [programme MAP] \
-reducer [programme REDUCE]
```

- Verifier l’output généré.
```
hdfs dfs -cat /output/*
```

Interfaces web pour Hadoop

Hadoop offre plusieurs interfaces web pour pouvoir observer le comportement de ses différentes composantes.
- http://localhost:9870 : permet d'afficher les informations de votre NameNode.
- http://localhost:8088 : permet d'afficher les informations du resource manager de Yarn et visualiser le comportement des différents jobs

Il vous est possible de monitorer vos Jobs Map Reduce, en allant à la page: http://localhost:8088.
