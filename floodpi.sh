#! /bin/sh
# /etc/init.d/floodpi 

### BEGIN INIT INFO
# Provides:          floodpi
# Required-Start:    $network
# Required-Stop:     $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start FloodPi at boot
# Description:       FloodPi script will start / stop a program a boot / shutdown.
### END INIT INFO

case "$1" in
  start)
    echo "Starting FloodPi"
    python /home/pi/flood-pi/floodpi.py -n bustardcelly@gmail.com
    ;;
  stop)
    echo "Stopping FloodPi"
    kill `pgrep -f floodpi.py`
    ;;
  *)
    echo "Usage: /etc/init.d/floodpi {start|stop}"
    exit 1
    ;;
esac

exit 0