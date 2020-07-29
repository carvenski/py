#!/bin/sh

num=`ps -ef | grep "/home/dev/data/itom/flink/conf" | wc -l`
echo `date`
echo $num 
# if num < 3, flink already stopped.
if [ $num -lt 3 ]; then
   echo "flink fail ! restart..."
   /home/dev/data/itom/flink/bin/stop-cluster.sh
   sleep 5
   /home/dev/data/itom/flink/bin/start-cluster.sh
else
   echo "flink ok."
fi
echo $num
echo "----"

# check flink cronjob setting
*/5 * * * * /home/dev/data/itom/flink/check_flink.sh >> /home/dev/data/itom/flink/check_flink.log

