

# task decorator (celery or aws)
class AbstractCommand:

    def __init__(self, input_dir, output_dir):
        # TODO instantiate on-demand file loaders
        pass

    def __input(self):
        #TODO read input files
        pass

    def __run(self):
        pass

    def __output(self):
        #TODO write output to files
        pass