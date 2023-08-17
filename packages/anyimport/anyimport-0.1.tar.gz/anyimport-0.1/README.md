# anyimport

This is a tool to enable importing from relative or absolute path across your python project

for example, in such a structure of project:

project/
├── module1/
│   └── /
│       ├── __init__.py
│       └── mod1.py
│		└── mod2.py
├── module2/
│   └── /
│       ├── __init__.py
│       └── mod3.py
│		└── mod4.py
└── app.py

In mod1.py, you can do
```
import mod2
from module1 import mod2

```


In app.py, you can do
```
import mod3
from module2 import mod4

```

## How to install this module and setup

``pip install -U anyimport``

Then in your entry python code, do

```
import anyimport

anyimport.init()


# or you can define the excluding path by folder name only

anyimport.init(excludes=["lib", "libs"])
```