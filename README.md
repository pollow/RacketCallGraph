# RacketCallGraph
A simple Python script that generate Call Graph of simple Racket program by generating dot language scripts. 

It uses naive approach that basically traverse the program and maintain a state machine regardless of context.

Currently it only maintain a FSM so advance features of Racket, like lambda-function is not support, will improve if needed in the future.

This simple script is developed for PDP course in Northeastern University.


## Usage

This script will only generate dot language script, please install Graphviz(http://www.graphviz.org/) or other compiler to generate readable graph.

The dot script is not optimized, please use `unflatten`, provided by Graphviz, to minimize the size of graph.

One line command usage:

```sh
>> python3 call_graph.py your_proram.rkt && unflatten -l3 callgraph.dot | dot -Tjpg -o graph.jpg
```

## Contribution

Contribution is welcomed.
