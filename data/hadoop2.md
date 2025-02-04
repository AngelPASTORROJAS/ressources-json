## Prérequis
Installer l'image docker : 
```bash
liliasfaxi/hadoop-cluster:latest
```

Commande de base hdfs:

```bash
# Créer un dossier
hdfs dfs -mkdir <chemin du nouveau répertoire>
# exemple: hdfs dfs -mkdir /user/output
```

```bash
# Lister le contenu d'un dossier
hdfs dfs -ls <chemin du répertoire>
# exemple: hdfs dfs -ls /user
```

```bash
# Supprimer un fichier
hdfs dfs -rm <chemin du fichier sur HDFS>
```

```bash
# Supprimer un dossier vide
hdfs dfs -rmdir <chemin du répertoire vide>
```

```bash
# Supprimer un dossier contenant des fichiers
hdfs dfs -rm -r <chemin du répertoire>
```

```bash
# Créer (copier) un fichier dans HDFS
hdfs dfs -put <chemin du fichier source> <chemin du fichier destination sur HDFS>
```

```bash
# Déplacer un fichier
hdfs dfs -mv <chemin du fichier source sur HDFS> <chemin du fichier destination sur HDFS>
```


## Déployer HADOOP avec container - 04/02/2025

```bash
# 
docker network create --driver=bridge hadoop
docker run -itd --net=hadoop -p 9870:9870 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest

# On lance le worker1
docker run -itd -p 8040:8042 --net=hadoop --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest

# On lance le worker2
docker run -itd -p 8041:8042 --net=hadoop --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest

# On lance le hadoop-master
docker exec -it hadoop-master bash
```

```bash
# On lance : start-dfs.sh et start-yarn.sh
#            qui sont executé dans ./start-hadoop.sh 
./start-hadoop.sh

# On vérifie que les services sont lancé
jps
# 193 NameNode
# 1057 ResourceManager
# 1685 Jps
# 421 SecondaryNameNode
```

Dans un terminal cmd:
```bash
docker ps

# CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS          PORTS                                                                                              NAMES
# 96d6b55a9290   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   13 minutes ago   Up 13 minutes   0.0.0.0:8041->8042/tcp                                                                             hadoop-worker2
# d1ce459e5464   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   13 minutes ago   Up 13 minutes   0.0.0.0:8040->8042/tcp                                                                             hadoop-worker1
# 70f0d030f8ed   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   13 minutes ago   Up 13 minutes   0.0.0.0:7077->7077/tcp, 0.0.0.0:8088->8088/tcp, 0.0.0.0:9870->9870/tcp, 0.0.0.0:16010->16010/tcp   hadoop-master

docker cp C:\Users\pasto\Downloads\input2\. 70f0d030f8ed:root
```
Test dans hadoop-master:
```bash
echo "Hello Big Data, Hello Hadoop" |python3 mapper.py
# Hello   1
# Big     1
# Data,   1
# Hello   1
# Hadoop  1
echo "Hello BigData, Hello Hadoop" |python3 mapper.py |sort |python3 reduce.py
# BigData,        1
# Hadoop  1
# Hello   2
```

Dans le hadoop-master:
```bash
# On crée le dossier
hdfs dfs -mkdir /input2

# On migre les fichiers
hdfs dfs -put /root/reduce.py /input2
hdfs dfs -put /root/mapper.py /input2

# On vérifie que les fichiers on été copier
hdfs dfs -ls /input2
# Found 2 items
# -rw-r--r--   2 root supergroup        243 2025-02-04 11:03 /input2/mapper.py
# -rw-r--r--   2 root supergroup        853 2025-02-04 11:02 /input2/reduce.py
```
