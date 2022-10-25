## skpyproj

Dette repoet inneheld pythonscript ved bruk i transformasjon. Pythonpakka *pyproj* er brukt som transformasjonsbibliotek i scripta.

Scripta som fylgjer med repoet kan ha referanse til pakker som ikkje er standard i python. Pakkene kan installast ved med *pip*.

### Installasjon av *pip*

#### Installasjon av pip i Windows:
Start *Command Prompt* i Windows.

#### Nedlasting av get-pip.py:
``curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py``

#### Installer pip:
``python get-pip.py``

#### Oppgrader pip til siste versjon:
``python -m pip install --upgrade pip``

#### Klone dette repoet:

Gå til ei mappe kor repoet skal klonast. Klon repoet:		
``git clone https://github.com/himsve/skpyproj.git``

#### Installer pythonpakker som ikkje er standard:

``pip install -r requirements.txt``

### skpyproj.py

Med python-scriptet *sklastrans.py* kan ein transformere enkeltpunkter med utgangspunkt i EPSG-kodane på inn- og utgåande referenserammer og datum. 
Scriptet har også høve til å transformere koordinatar på kolonneseparert format.

#### Argumenter og opsjonar i skpyproj.py:

```
>python src/skpyproj.py --help
usage: skpyproj.py [-h] [--input InputFile] [--output OutputFile] [--area Area] [-d D] SourceCrs TargetCrs

Transforms coordinates from csv files at format ID(pointname) x y z epoch).

positional arguments:
  SourceCrs            EPSG code or proj string of source crs
  TargetCrs            EPSG code or proj string of target crs

optional arguments:
  -h, --help           show this help message and exit
  --input InputFile    Path to input csv file
  --output OutputFile  Path to output csv file
  --area Area          EPSG code area extent
  -d D                 Number of decimals
```

#### Eksempel køyring av sklastrans.py med transformasjon av enkeltpunkt:

```
>python src/skpyproj.py -d 4 25832 25833
Enter input coordinates (X Y Z Epoch): 500000 6700000
['170060.37027450086 6715046.924547676']
```

#### Eksempel køyring av sklastrans.py med transformasjon av kolonneseparert fil:

```
>python src/skpyproj.py -d 4 --input inputfil.txt --output outputfil.txt 25832 25833
```

### sklastrans.py

Python-scriptet *sklastrans.py* transformerer LAS-filer med transformasjonspakka *pyproj*. Innlesing av LAS-filene er gjort med pythonpakka *laspy*.

#### Argumenter og opsjonar i sklastrans.py:

```
> python src/sklastrans.py --help
usage: sklastrans.py [-h] [--input InputFile] [--output OutputFile] SourceCrs TargetCrs

Transforms data in LAS-files based on EPSG-kodes.

positional arguments:
  SourceCrs            EPSG code or proj string of source crs
  TargetCrs            EPSG code or proj string of target crs

optional arguments:
  -h, --help           show this help message and exit
  --input InputFile    Path to input LAS file
  --output OutputFile  Path to output LAS file
```

#### Eksempel køyring av sklastrans.py:

```
python src/sklastrans.py --input input.las --output output.las 25832 5105
```

Denne kommandoen vil importere fila *input.las*, transformere frå EUREF89 UTM32 til EUREF89 NTM05 og eksportere til fila *output.las*.
