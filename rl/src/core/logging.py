import logging

logging.basicConfig(filename='run_logs.txt',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


def log(*args, **kwargs):

    if isinstance(args, dict):
        msg = str(args)
    else:
        msg = "".join(list(args))
    # msg = str(args)
    print(msg)
    logging.info(msg)