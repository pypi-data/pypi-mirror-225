#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : gunicorn_logger
# @Time         : 2023/8/15 14:12
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/pahntanapat/Unified-FastAPI-Gunicorn-Log/blob/main/example_inherited.py

import logging
from gunicorn.glogging import Logger
from signal import SIGINT
from gunicorn.app.base import BaseApplication
from gunicorn.arbiter import Arbiter
from sys import stderr, exit

from threading import Thread


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        self.loglevel = self.LOG_LEVELS.get(cfg.loglevel.lower(), logging.INFO)

        handler = logging.NullHandler()

        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)

        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)

        self.error_logger.setLevel(self.loglevel)
        self.access_logger.setLevel(self.loglevel)


class MainProcess(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None, usage=None, prog=None):
        self.options = options or {}

        # Override Logging configuration
        self.options.update({
            "accesslog": "-",
            "errorlog": "-",
            "worker_class": "uvicorn.workers.UvicornWorker",
            "logger_class": StubbedGunicornLogger
        })

        self.application = app
        self.arbiter = None
        super().__init__(usage, prog)

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if ((key in self.cfg.settings) and (value is not None))
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self):
        try:
            self.arbiter = Arbiter(self)
            self.arbiter.run()
        except RuntimeError as e:
            self.logger("Error: %s" % e)
            stderr.flush()
            exit(1)

    def restart(self):
        restart_thr = Thread(target=self.__restart)
        restart_thr.start()
        return restart_thr

    def __restart(self):
        BaseApplication.reload(self)
        if self.arbiter is not None:
            self.arbiter.reload()

    def end(self):
        if self.arbiter is not None:
            self.arbiter.signal(SIGINT, None)

    def terminate(self):
        if self.arbiter is not None:
            self.arbiter.signal(SIGINT, None)


class InThread(Thread, MainProcess):
    def __init__(self,
                 app,
                 gunicorn_options=None,
                 usage=None,
                 prog=None,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs=None,
                 *,
                 daemon=None):
        if target is None:
            target = self.__run_and_end
        Thread.__init__(self,
                        group=group,
                        target=target,
                        name=name,
                        args=args,
                        kwargs=kwargs,
                        daemon=daemon)
        MainProcess.__init__(self,
                             app,
                             gunicorn_options,
                             usage=usage,
                             prog=prog)

    def __run_and_end(self):
        self.run_to_end()
        self.end()

    def start(self):
        super().start()
        MainProcess.run(self)

    def run_to_end(self):
        raise NotImplementedError(
            'Run to End is not implemented. Please override run_to_end or run method, or set target parameter in constructor.'
        )
