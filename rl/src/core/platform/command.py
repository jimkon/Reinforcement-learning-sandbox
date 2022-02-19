

# task decorator (celery or aws)
class AbstractCommand:

    alias = None

    def __init__(self, input_dir, output_dir):
        # TODO instantiate on-demand file loaders
        pass

    # @property
    # def alias(self):
    #     raise NotImplementedError
        # return self.__alias()

    # def __alias(self):
    #     raise NotImplementedError

    def __input(self):
        #TODO read input files
        pass

    def __run(self):
        pass

    def __output(self):
        #TODO write output to files
        pass

    def __repr__(self):
        return str(self.__class__)