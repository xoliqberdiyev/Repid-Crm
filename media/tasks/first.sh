#!bin/bash

echo  "MyApp started" | systemd-cat -t MyApp -p info
sleep 5
echo "MyApp creashed" | systemd-cat -t MyApp -p err

