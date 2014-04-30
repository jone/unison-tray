from croniter import croniter
from datetime import datetime
from threading import Thread
from utray.config import CONFIG
from utray.utils import app
import time


def setup_syncing_cronjobs():
    crons = []
    for cron_definition in CONFIG.sync_crons:
        cron = SyncingCronjob(cron_definition)
        cron.start()
        crons.append(cron)
    return crons


class SyncingCronjob(Thread):

    def __init__(self, cron_definition):
        super(SyncingCronjob, self).__init__()
        self.iter = croniter(cron_definition)

    def run(self):
        self.running = True
        now = datetime.now()
        next = self.iter.get_next()

        timeout = next - time.mktime(now.timetuple())
        for sec in range(int(timeout)):
            time.sleep(1)
            if self.running == False:
                return

        app.get().sync()

    def stop(self):
        self.running = False
