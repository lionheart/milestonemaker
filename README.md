milestonemaker
==============

What Does This Do
-----------------

This simple utility creates weekly milestones in GitHub issues. See https://github.com/lionheart/milestonemaker/milestones for an example.

How Do You Use It
-----------------

```
pip install milestonemaker
```

Once installed, just follow the useful CLI prompts.

```
$ milestonemaker -h
usage: milestonemaker [-h] {create,delete} ...

positional arguments:
  {create,delete}
    create         Creates all milestones
    delete         Deletes all milestones with 'week' in the name and no
                   issues assigned to them.

optional arguments:
  -h, --help       show this help message and exit
```
