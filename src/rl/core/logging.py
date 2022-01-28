import logging

logging.basicConfig(filename='run_logs.txt',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


def log(*args, **kwargs):
    msg = "".join(list(args))
    print(msg)
    logging.info(msg)