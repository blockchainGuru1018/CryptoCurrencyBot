"""
Bitcoin arbitrage mixins.
"""

import logging
import os
import psutil
import sys

from django.conf import settings

logger = logging.getLogger(__name__)


class MonitorMixin(object):


    def get_file(self, username, filename):
        """ Helper to get a file to deposit the process id of the monitor. """
        path = settings.BASE_DIR / "monitor_ref" / username

        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass

        file_path = path / filename

        if not os.path.exists(file_path):
            os.system(f"touch {file_path}")

        return file_path


    def start_monitor(self, **kwargs):
        """ Start a monitor """
        try:

            username = kwargs["user"]
            monitor = kwargs["monitor"]
            file_name = kwargs["file"]

            file = self.get_file(username, file_name)

            args = [sys.executable,
                    'manage.py',
                    'startmonitor',
                    monitor]

            with open(file, "r") as ts:
                try:
                    pid = ts.readlines()[0]
                    pid = psutil.Process(pid=int(pid))
                    pid.terminate()
                except psutil.NoSuchProcess:
                    pass
                except Exception as error:
                    logger.exception(str(error))
                    pass

            with open(file, "w") as ts:
                proc = psutil.Popen(args)
                ts.write(str(proc.pid))

        except Exception as error:
            logger.exception(str(error))
            return False

        return True


    def stop_monitor(self, username, file):
        try:

            file = self.get_file(username, file)

            with open(file, "r") as ts:
                pid = ts.readlines()[0]
                pid = int(pid)

            proc = psutil.Process(pid=pid)
            logger.info(msg=f"Shutting down monitor process {proc.pid}")
            proc.terminate()

        except Exception as error:
            logger.exception(str(error))
            return False

        return True
