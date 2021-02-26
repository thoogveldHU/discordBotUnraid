#! /bin/sh
#Not using a restart option, since maps can crash because of it.
docker stop -t 10 Valheim
docker start Valheim
