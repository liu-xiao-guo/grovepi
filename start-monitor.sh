export PYTHON_SERVER_HOME="$SNAP"
export PATH="$SNAP/usr/sbin:$SNAP/usr/bin:$SNAP/sbin:$SNAP/bin:$PATH"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$SNAP/lib:$SNAP/usr/lib:$SNAP/lib/arm-linux-gnueabihf:$SNAP/usr/lib/arm-linux-gnueabihf"
export PYTHONUSERBASE=$SNAP
export PYTHONHOME=$SNAP/usr
export PYTHONPATH=$SNAP/usr/lib/python2.7/site-packages/
export LD_LIBRARY_PATH="$SNAP/usr/lib/arm-linux-gnueabihf:$LD_LIBRARY_PATH"
LD_LIBRARY_PATH=$SNAP_LIBRARY_PATH:$LD_LIBRARY_PATH
PYTHON_EGG_CACHE=$SNAP_DATA/.python-eggs $PYTHON_SERVER_HOME/usr/bin/python2.7 $PYTHON_SERVER_HOME/bin/monitor.py