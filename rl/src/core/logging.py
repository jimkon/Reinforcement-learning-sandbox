from functools import wraps
import time
from os.path import join

import numpy as np
import pandas as pd
import cv2

from rl.src.core.configs.log_configs import *
from rl.src.core.configs.general_configs import EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH
from rl.src.core.utilities.file_utils import create_path, generate_markdown_from_logs, markdown_to_html
from rl.src.core.utilities.timestamp import timestamp_long_str, timestamp_unique_str


def _time():
    if GENERAL_LOG_TIMINGS_FLAG:
        return time.time_ns()
    else:
        return .0


class Logger:

    instances = []

    def __init__(self, name, directory=None):
        Logger.instances.append(self)

        self.name = name
        self.directory = directory if directory else ''
        self.path = join(EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH, self.directory)

        create_path(self.path)

        self.log_path = join(self.path, LOG_CSV_DIR_PATH)
        create_path(self.log_path)

        self.html_path = join(self.path, LOG_HTML_DIR_PATH)
        create_path(self.html_path)

        self.perf_mon_path = join(self.path, PERFORMANCE_MONITORING_DIR_PATH)
        create_path(self.perf_mon_path)

        self.imgs_path = join(self.path, LOG_IMAGES_DIR_PATH)
        create_path(self.imgs_path)

        self.__log_dict = {
            "timestamp": [],
            'message': [],
            'tags': []
        }
        self.__img_dict = {
            "timestamp": [],
            'path': [],
            'image': []
        }

    def log(self, msg, tags=None):
        if not GENERAL_LOG_FLAG:
            return

        tags = [] if not tags else tags if isinstance(tags, list) else [tags]

        if GENERAL_LOG_STDOUT_FLAG:
            print(msg, 'tags:', tags)

        self.__log_dict['timestamp'].append(timestamp_long_str())
        self.__log_dict['message'].append(msg)
        self.__log_dict['tags'].append('|'.join(tags))

    def log_image(self, img, title=None, store_directly_on_disk=False, tags=None):
        assert isinstance(img, np.ndarray), f"Image must be in numpy array format. Given {type(img)}"

        if not tags:
            tags = ['log_plt']
        else:
            tags.append('log_plt')

        if not title:
            title = timestamp_unique_str()
        else:
            title = f"{title}_{timestamp_unique_str()}"

        title += '.png'

        path = join(self.imgs_path, title)

        self.__img_dict['timestamp'].append(timestamp_long_str())
        self.__img_dict['path'].append(path)
        self.log(f"![]({path})", tags='image')

        if store_directly_on_disk:
            self.__save_image(img, path)
            self.__img_dict['image'].append(None)
            # self.log(f"Image {title} saved as {path}", tags=tags)
        else:
            self.__img_dict['image'].append(img)
            self.log(f"Image {title} saved temporarily in RAM", tags=tags)

    def save(self):
        df = pd.DataFrame(self.__log_dict)
        df.to_csv(join(self.log_path, f"{self.name}_{CSV_FILENAME_EXTENSION_LOGS_CSV}.csv"), index=False)

        for i in range(len(self.__img_dict['image'])):
            path = self.__img_dict['path'][i]
            img = self.__img_dict['image'][i]
            self.__save_image(img, path)

        fpath = generate_markdown_from_logs()
        markdown_to_html(fpath)

    def __save_image(self, image, path):
        if image is None:
            return

        if image.max() <= 1.:
            image = (255 * image).astype(int)
        cv2.imwrite(path, image)
        self.log(f"Image saved as {path}")

    # https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
    def log_func_call(self, tags=None):
        TAG = "func_call"
        if not tags:
            tags = [TAG]
        elif isinstance(tags, list):
            tags.append(TAG)
        elif isinstance(tags, str):
            tags = [tags, TAG]
        else:
            tags = [TAG]

        def log_tags(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                args_repr = [repr(a) for a in args]  # 1
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
                signature = ", ".join(args_repr + kwargs_repr)  # 3
                start_time = _time()

                result = func(*args, **kwargs)
                end_time = _time()
                run_time = (end_time - start_time)/1000000
                result_str = repr(result).replace('\n', '')
                self.log(f"Called: {func.__name__}( {signature} ) -> |{result_str!r}| in {run_time:.3f} ms", tags=tags)
                self.log(f"Function:{func.__name__} Time:{run_time}", tags="run_time")  #

                return result

            return wrapper

        return log_tags


def save_loggers():
    for _logger in Logger.instances:
        _logger.save()


logger = Logger('general')
log = logger.log
