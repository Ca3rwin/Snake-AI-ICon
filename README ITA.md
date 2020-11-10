# Serpente
> Reti neurali che giocano a snake addestrati da algoritmi genetici

<p align = "center">
   <img src = "./animation.gif">
</p>


Un progetto personale fatto da Antonio Scardavilli e Ivan Valluzzi, consistente nell'addestrare reti neurali per giocare al gioco "Snake"

Questo progetto contiene:
- Lo stesso gioco di Snake
- Un modulo di algoritmo genetico
- Un modulo di rete neurale
- Un file principale con esempi

Abbiamo cronometrato la maggior parte delle funzioni per essere sicuri di migliorare la velocità e abbiamo usato numba jit per compilare alcune funzioni.
L'algoritmo genetico è parallelizzato per la sua parte principale (valutazione dei serpenti) usando multiprocessing e joblib.

## Installazione

E' stato utilizzato Phyton 3 per questo progetto e non possiamo essere sicuri che le versioni precedenti siano compatibili

Librerie di cui avrai bisogno per eseguire il progetto:

{`` joblib``, `` numpy``, `` numba``, `` pygame``}

## Utilizzo

Troverai alcuni esempi pronti per l'esecuzione nel file `` main.py``.

Puoi provare a:
- Giocare a Snake
- Addestrare le tue reti neurali (può volerci del tempo per ottenere buoni risultati)
- Mostrare un gioco giocato da reti neurali che abbiamo addestrato e selezionato perchè più interessanti.

Tutto è spiegato nel file, basta decommentare le parti che vuoi eseguire, quindi vai al terminale e esegui:
```sh
python main.py
```

