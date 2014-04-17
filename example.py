from modelthing import ModelThing

class Person (ModelThing):
    _table = "people"

    def __unicode__(self):
        return "Hello, I am %s" % (self.name,)

if __name__=="__main__":

    for person in Person.list():
        person.delete()

    p1 = Person(name="ahmed")
    p1.save()

    p2 = Person(name="barnabus")
    p2.save()

    for person in Person.list():
        print person
        print "And here I am in JSON:"
        print person.tojson()
        print "***"
