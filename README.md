web.py ModelThing
===

(c) 2014 Gatlin Johnson <gatlin@niltag.net>

See the `LICENSE` file for licensing information.

0. So what is it?
---

I wanted a simple ORM / model thing for web.py. If you have a schema such as

```sql
CREATE TABLE people (
    id integer not null
  , name text
  , age integer
);
```

then you can use ModelThing like so:

```python
from modelthing import ModelThing

class Person (ModelThing):
    _table = "people"

    def __unicode__(self):
        print "Hello, my name is %s" % (self.name,)
```

and VOILA you can do stuff like so:

```python
ahmed = Person(name="ahmed",age=24)
ahmed.save()

alice = Person(name="alice",age=24)
alice.save()

for person in Person.list(age=24):
    print person
```

and so on and so forth.

1. Run the example
---

Ensuring that you have `pip`,`virtualenv`, and sqlite installed, run:

    make example
    ve/bin/python example.py

You can clean up with:

    make cleanexample

2. Bugs / comments / etc
---

File bugs [on GitHub](https://github.com/gatlin/webpy-modelthing/issues).
