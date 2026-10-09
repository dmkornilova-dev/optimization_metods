def make_logger(verbose):
    def log(msg):
        if verbose:
            print(msg)
    return log