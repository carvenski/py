

# pip install pycallgraph


'''
You can either use the command-line interface for a quick visualization of your Python script, 
or the pycallgraph module for more fine-grained settings.
The following examples specify graphviz as the outputter, so it's required to be installed. 
They will generate a file called pycallgraph.png.
'''

# The command-line method of running pycallgraph is:
#	$ pycallgraph graphviz -- ./mypythonscript.py


# A simple use of the API is:
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

with PyCallGraph(output=GraphvizOutput()):
    code_to_profile()

# ------------------------------------------------------------------------------------------------------------------- #

#!/usr/bin/env python
'''
This example demonstrates a simple use of pycallgraph.
'''
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


class Banana:

    def eat(self):
        pass


class Person:

    def __init__(self):
        self.no_bananas()

    def no_bananas(self):
        self.bananas = []

    def add_banana(self, banana):
        self.bananas.append(banana)

    def eat_bananas(self):
        [banana.eat() for banana in self.bananas]
        self.no_bananas()


def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'basic.png'

    with PyCallGraph(output=graphviz):
        person = Person()
        for a in xrange(10):
            person.add_banana(Banana())
        person.eat_bananas()


if __name__ == '__main__':
    main()