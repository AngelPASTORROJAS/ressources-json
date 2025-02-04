```bash
# Vérifier qu'il y est plus les docker
docker ps
# CONTAINER ID   IMAGE                              COMMAND                  CREATED       STATUS       PORTS
#                                  NAMES
# 96d6b55a9290   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   3 hours ago   Up 3 hours   0.0.0.0:8041->8042/tcp
#                                  hadoop-worker2
# d1ce459e5464   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   3 hours ago   Up 3 hours   0.0.0.0:8040->8042/tcp
#                                  hadoop-worker1
# 70f0d030f8ed   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   3 hours ago   Up 3 hours   0.0.0.0:7077->7077/tcp, 0.0.0.0:8088->8088/tcp, 0.0.0.0:9870->9870/tcp, 0.0.0.0:16010->16010/tcp   hadoop-master

docker stop <container_id>

# C:\Users\pasto>docker stop 96d6b55a9290
# 96d6b55a9290

# C:\Users\pasto>docker stop d1ce459e5464
# d1ce459e5464

# C:\Users\pasto>docker stop 70f0d030f8ed
# 70f0d030f8ed
```

```bash
docker pull liliasfaxi/spark-hadoop:hv-2.7.2

docker network create --driver=bridge hadoop

docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/spark-hadoop:hv-2.7.2

docker run -itd -p 8040:8042 --net=hadoop --name hadoop-slave1 --hostname hadoop-slave1 liliasfaxi/spark-hadoop:hv-2.7.2

docker run -itd -p 8041:8042 --net=hadoop --name hadoop-slave2 --hostname hadoop-slave2 liliasfaxi/spark-hadoop:hv-2.7.2

docker exec -it hadoop-master bash
```

// On peut utiliser la même image de hadoop-master de cluster
sur un terminal lance 
```bash
./start-hadoop.sh
./start-kafka-zookeeper.sh
jps
# 193 NameNode
# 421 SecondaryNameNode
# 1878 Jps
# 972 QuorumPeerMain
# 973 Kafka
# 654 ResourceManager
```

On modifie le nom "meta.properties" en "meta.properties_old"
```bash
cd /tmp/kafka-logs/
ls
mv meta.properties meta.properties_old
cd
```
```bash
# creation de topic
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic Hello-Kafka
```
```bash
# liste des topics
kafka-topics.sh --list --bootstrap-server localhost:9092
```

Dans un nouveau terminal pour le producer:
```bash
docker exec -it hadoop-master bash

# le producer
kafka-console-producer.sh --broker-list localhost:9092 --topic Hello-Kafka
```

Dans un nouveau terminal pour le consommateur (consumer):
```bash
docker exec -it hadoop-master bash

# le consumer
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic Hello-Kafka --from-beginning
```

Le fichier `producer.py`
```python
from confluent_kafka import Producer
import time

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def produce_messages(producer, topic, num_messages=10):
    for i in range(num_messages):
        key = 'key{}'.format(i)
        value = 'message{}'.format(i)
        producer.produce(topic, key=key, value=value, callback=delivery_report)

    producer.flush()

def main_producer():
    # Configuration du producteur
    producer_config = {
        'bootstrap.servers': 'localhost:9092',  # Remplacez par votre configuration Kafka
        'acks': 'all',
    }

    producer = Producer(producer_config)
    topic_name = 'example_topic'  # Remplacez par le nom du topic Kafka que vous utilisez

    try:
        produce_messages(producer, topic_name)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main_producer()
```

Le fichier Consumer.py:
```python
from confluent_kafka import Consumer, KafkaError

def consume_messages(consumer, topic):
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            print('Received message: key={}, value={}'.format(msg.key(), msg.value()))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def main_consumer():
    # Configuration du consommateur
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',  # Remplacez par votre configuration Kafka
        'group.id': 'example_group',
        'auto.offset.reset': 'earliest',
    }

    consumer = Consumer(consumer_config)
    topic_name = 'example_topic'  # Remplacez par le nom du topic Kafka que vous utilisez

    try:
        consume_messages(consumer, topic_name)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main_consumer()
```

Déplacer les fichier dans `root`:
```bash
docker ps
# CONTAINER ID   IMAGE                              COMMAND                  CREATED          STATUS          PORTS                                                                                              NAMES
# bef7e027c2bb   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   36 minutes ago   Up 36 minutes   0.0.0.0:8041->8042/tcp                                                                             hadoop-worker2
# e0a8ccbe6511   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   36 minutes ago   Up 36 minutes   0.0.0.0:8040->8042/tcp                                                                             hadoop-worker1
# 6f63aeed8cfa   liliasfaxi/hadoop-cluster:latest   "sh -c 'service ssh …"   36 minutes ago   Up 36 minutes   0.0.0.0:7077->7077/tcp, 0.0.0.0:8088->8088/tcp, 0.0.0.0:9870->9870/tcp, 0.0.0.0:16010->16010/tcp   hadoop-master

docker cp C:\Users\pasto\Downloads\kafka\. 6f63aeed8cfa:/root
# Successfully copied 5.63kB to 6f63aeed8cfa:/root
```

Vérifier la présence des fichiers copier:
```bash
# Dans le cmd
docker exec -it hadoop-master bash
```
```bash
# dans le hadoop-master
ls
```

Assurez-vous d'installer la bibliothèque confluent_kafka avant d'exécuter ces programmes dans le hadoop-master :
```bash
apt update
apt install -y python3-pip
python3 -m pip install --upgrade pip # si possible
pip install confluent-kafka
```

sur le terminal `producer` lance:
```bash
pip install requests
pip install bs4
pip install pandas
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.8 producer.py
```

sur le terminal `consumer` lance:
```bash
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.8 Consumer.py
```

--
Maintenant avec du scrapping

Le fichier `producer-scrapt.py`:
```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
job_elements = soup.find_all("div", class_="card-content")
liste = []
for i in range(0,len(job_elements)):  
        title = job_elements[i].find("h2").contents[0].strip()
        company = job_elements[i].find("h3").contents[0].strip()
        location = job_elements[i].find("p", {"class":"location"}).contents[0].strip()
        liste.append((title, company, location))
       
df = pd.DataFrame(liste, columns=["title", "company", "location"])
df
```

On copie dans root le nouveau fichier:
```bash
docker cp C:\Users\pasto\Downloads\kafka\producer-scrapt.py 6f63aeed8cfa:/root
# Successfully copied 2.56kB to 6f63aeed8cfa:/root
```

Le producer:
```bash
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.8 producer-scrapt.py
```

Le consumer:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic Hello-Kafka
```


---

# Le Hbase
```bash
docker exec -it hadoop-master bash
```

```bash
start-all.sh
start-hbase.sh
jps
hbase shell
```

```bash
# hbase:001:0>

# Lister le nombre de serveurs hbase utilisés
status



# La version Hbase utilisée
version

# Avoir des informations sur l’utilisateur actuel
whoiam

# Commande help sous hbase pour connaitre toutes les commandes disponibles et leurs explications
table_help

# --- Manipulation de tables sous HBASE

# Lister les tables créées sous Hbase
list

# Créer une table Hbase : pour le faire, il faut donner le nom de table et les noms des "column families".
## create 'tableName','Column1Name','Column2Name'
# Dans notre exemple, le nom de la table est costumer et les noms des colonnes families sont : address et order .
create 'costumer', 'address', 'order'

# Vérifier la création de la table costumer
list

# Afficher le contenu de la table costumer
scan 'costumer'

# Désactiver la table costumer
disable 'costumer'

# Afficher le contenu de la table désactivée
scan 'costumer'

# Vérifier si la table costumer est désactivée
is_disabled 'costumer'

# Vérifier si la table costumer existe
exists 'costumer'

# Description de la table costumer
describe 'costumer'

# Activer la table costumer
enable 'costumer'

# Description de la table costumer
describe 'costumer'

# Ajouter une colonne famille à la table costumer
alter 'costumer', {NAME=>'personal data'}

# Supprimer une colonne famille de la table costumer
alter 'costumer', 'delete'=>'personal data'

# Ajouter un client à la table costumer
put 'costumer', '1', 'address:city','Paris' put 'costumer', '1', 'address:state','France' put 'costumer', '1', 'address:street','Bailly' put 'costumer', '1', 'order:number','ORD-15' put 'costumer', '1', 'order:amount','15'

# Afficher le contenu de la table costumer
scan 'costumer'

# Ajouter un deuxième client à la table costumer
put 'costumer', '2', 'address:city','Nancy' put 'costumer', '2', 'address:state','France' put 'costumer', '2', 'address:street','Belfort' put 'costumer', '2', 'order:number','ORD-16' put 'costumer', '2', 'order:amount','15'

# Lecture des données de la table costumer
get 'costumer', '1' 
get 'costumer', '1', 'address'
get 'costumer', '1', 'address:city' 
get 'costumer', '1', {COLUMN=>'address:city'} 
get 'costumer', '1', {COLUMN=>['address:city','address:street']} 
scan 'costumer',{COLUMNS=>['address:city']} 
scan 'costumer',{COLUMNS=>['address:city'], LIMIT=>1}

# Retourner le nombre de clients dans la table costumer
count 'costumer'

# Supprimer la colonne city pour le client 1
delete 'costumer' , '1', 'address:city'

# Supprimer toutes les cases du client 2
deleteall 'costumer', '2'

# Ajouter l’historique des versions à une colonne
alter 'costumer',{NAME=>'address',VERSIONS=>5}

# Afin de tester le résultat de VERSIONS, on insère 3 valeurs différentes pour un client 3 et on affiche la deuxième version.
put 'costumer', '3', 'address:city','Paris' 
put 'costumer', '3', 'address:city','Lyon' 
put 'costumer', '3', 'address:city','Nantes'
scan 'costumer',{COLUMN=>'address:city',VERSIONS=>2}

# Supprimer la table costumer (il faut la désactiver avant de la supprimer)
disable 'costumer'
drop 'costumer'
```

[documentation happybase](https://happybase.readthedocs.io/en/latest/user.html#establishing-a-connection)
