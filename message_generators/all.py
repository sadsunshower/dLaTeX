from message_generators.autosize import GeneratorAutosize
from message_generators.generator import GeneratorLookup
from message_generators.operators import GeneratorOperators
from message_generators.overfull import GeneratorOverfull
from message_generators.powers import GeneratorPowers

'''
Export all generators in a convenient list
'''
all_generators = [
    GeneratorLookup(),
    GeneratorAutosize(),
    GeneratorOperators(),
    GeneratorOverfull(),
    GeneratorPowers()
]