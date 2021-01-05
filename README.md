# Artificial_Vision-Unisa-_2021_group4
Repository github da allegare alla consegna del progetto di visione artificiale dell'appello di gennaio per l'anno 2020/2021

# Spiegazione degli script
* 1_augcsv_prepare divide un csv in csv da non modificare e uno sulle cui immagini indicate effettuare augmentation
* 2_csv_divider divide un csv in n parti uguali
* 3_aug_creation dato un csv prende tutte le immagini indicate, le cerca dalla root del dataset, le apre le modifica e le stampa in una cartella extra chiamata "augment" inoltre stampa un csv relativo a queste
* 4_aug_suddivision spalma in maniera equa le righe relative al csv con le immagini modificate in ogni csv indicato
* 5_tfrecord_generator dati i csv di input (si augura non tutti in una volta in quanto su macchine normali è lento) e la root del dataset crea tanti tfrecord tanti erano i csv in input
