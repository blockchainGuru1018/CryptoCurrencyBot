"""
~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
Monitor commands.
~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+
"""

import logging

from django.core.management.base import BaseCommand, CommandError

from bitcoin_arbitrage.monitor.monitor import Monitor


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Starting monitor thread.'
    output_transaction = False
    stop_threads = False


    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="start | stop monitor")
        self.monitor = Monitor()


    def handle(self, *args, **options):
        if options.get("action") == "start_tri":
            flag = self.start_tri()
        elif options.get("action") == "start_inter":
            flag = self.start_inter()


    def start_tri(self):
        try:
            self.monitor.update_tri()
        except Exception as error:
            logger.exception(str(error))
            return False
        self.stdout.write(self.style.SUCCESS('Successfully start monitor!'))


    def start_inter(self):
        try:
            self.monitor.update_inter()
        except Exception as error:
            logger.exception(str(error))
            return False
        self.stdout.write(self.style.SUCCESS('Successfully start monitor!'))


    def start_monitor_thread(self):
        logger.info("Starting monitor thread.")
        try:
            self.monitor.update()
            print('Monitor updating ... in startmonitor.')
        except Exception as error:
            logger.exception(str(error))
        return True
