# Come usare la pipeline
Attenzione: per rendere la pipeline modificabile e ogni sua fase indipendente (per via di ogni test effettuato su metologie diverse provate e per ottimizzare i tempi) gli script generano automaticamente directory di input e di output ma è necessario accertarsi che i path, per ogni ulteriore risorsa necessaria (es. csv originale o root del dataset), siano corretti
* Scaricare la pipeline
* Scaricare il csv, inserirlo nella directory e rinominarlo "train.age_detected" se presenta un nome diverso
* Scaricare il GenderRecognitionFramework del Mivia Lab e inserirlo nella cartella di pipeline assicurandosi che gli import funzionino correttamtente
* Controllare le prime 4 o 5 righe di ogni script e modificare le costanti se si riferiscono a risorse quali il csv originale o la root del dataset
* Se si vuole effettuare tutta la pipeline occorre fare in sequenza ogni script
