# ampCountPy
Some python functions to count the expected amplifications for genomic regions given a set of primer binding locations for a [multiple displacement amplification](http://en.wikipedia.org/wiki/Multiple_displacement_amplification) reaction. See [ampCountR](https://github.com/sherrillmix/ampCountR) for more details.
 
##Installation

 To install, clone the repository to a local directory using something like:
```
git clone https://github.com/sherrillmix/ampcountpy.git
```
and run `setup.py` from the resulting directory (the `--user` installs it locally and doesn't require root access):
```
cd ampcountpy
python setup.py test
python setup.py install --user
```

## Run directly
The module can be called directly using something like:
```
python -m ampcountpy -f forward.txt -r reverse.txt
```
where `forward.txt` is a text file containing position of primer landing sites on the forward strand and `reverse.txt` is primer landing sites on the reverse strand. By default, amplification predictions are output to out.csv. The full details on options and arguments is available with:
```
python -m ampcountpy --help
```

## Using function in python
The main function is `predictAmplifications` which can be used like:
```
from ampcountpy import predictAmplifications
forwards=[1,2,3]
reverses=[5,6,7]
predictions=predictAmplifications(forwards,reverses)
```
where `forwards` are the 5'-most base of primer landing sites on the forward strand and `reverses` are the 3'-most base of primers landing on the reverse strand.





