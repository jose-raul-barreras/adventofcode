import click
from traitlets import default
from loader import load_level_input

MODULES = {
    1: "one"
}

@click.command()
@click.option('--level', default=1, type=click.INT, help="The level to solve") 
#@click.option('--test', is_flag=True, help="Run the tests", default=False)

def main(level):
    print("Solving level {}".format(level))

    # if test:
    #     for level in MODULES:
    #         print("Testing {}".format(level))
    #         module = __import__(MODULES[level])
    #         

    if level in MODULES:
        input = load_level_input(level)
        module = __import__(MODULES[level])
        module.test_solution()
        solution = module.solve(input)
        print("Solution: {}".format(solution))
    else:
        print("Level not found")
       
if __name__ == '__main__':
    main()