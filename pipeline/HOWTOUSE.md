# Come usare la pipeline
Attenzione: per rendere la pipeline modificabile e ogni sua fase indipendente (per via di ogni test effettuato su metologie diverse provate e per ottimizzare i tempi) gli script non generano automaticamente directory ma bisogna garantire almeno una cartella di input e di output e di collegare correttamente i path per ogni ulteriore risorsa necessaria (es. csv originale o root del dataset)
* Scaricare la pipeline
* Scaricare il GenderRecognitionFramework del Mivia Lab e inserirlo nella cartella di pipeline assicurandosi che gli import funzionino correttamtente
* Controllare le prime 4 o 5 righe di ogni script e modificare le costanti, creando dove serve delle cartelle
* Creare una subdirectory vuota di nome "augment" nella cartella root del dataset
* Se si vuole effettuare tutta la pipeline occorre fare in sequenza ogni script