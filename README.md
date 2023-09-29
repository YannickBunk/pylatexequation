# pylatexequation
A python tool to generate equation images for Medium articles using latex

The tool generates images for Medium articles in a format that works well on all devices (Desktop, table, phone). 
The code was developed with `python 3.11.3` but should work with all python version which support the modules listed in `requirements.txt`.

Equations are supplied to the script via an input file (Default `equation.eqs`), where each line in the input file defines a single equation.
Equations are defined using the latex syntax. An example input file is shown below

```
a=b
k(x_i,x_j)=\exp{\Big(-\frac{d(x_i,x_j)^2}{2 l^2} \Big)}
\mathcal{L} \lbrace f(t)\rbrace = \int_{t=0}^\infty e^{-st} f(t)\,dt
```

The script may be executed via

```
python run.py
```

Command arguments can be supplied for more control over the output. A full list of command line arguments can be displayed via

```
python run.py --help
```


