import commands
import croniter


# (status, output) = commands.getstatusoutput('/Users/huan/software/datax/bin/datax.py /Users/huan/software/datax/job/94853791-f6ce-11e8-8271-4a0001c796d0.json')
#
# print status
#
# print output
from apscheduler.triggers.cron import CronTrigger

cron = CronTrigger.from_crontab(' */5 * * * *')
print cron
print type(cron)