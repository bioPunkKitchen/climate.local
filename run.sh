#!/bin/bash

if [ -f ./log.txt ]; then
	if [ ! -d ./oldlogs ]; then
	mkdir oldlogs
	fi
	mv ./log.txt ./oldlogs/log__$(date +%Y-%m-%d_%A_%H-%M-%S).txt
	mv ./data/data.log ./oldlogs/data__$(date +%Y-%m-%d_%A_%H-%M-%S).log
fi

echo "*** Climate cahmber Log ***" > ./log.txt
echo "run.sh executed at" >> ./log.txt
date >> ./log.txt

if [ ! -d ./data ]; then
	mkdir data
	echo "data file directory created" >> ./log.txt
fi

if [ ! -f ./data/data.log ]; then
	touch ./data/data.log
	echo "data.log created" >> ./log.txt
fi

if [ ! -f ./data/state.json ]; then
	touch ./data/state.json
	echo "state.json created" >> ./log.txt
fi

if [ ! -f ./data/config.json ]; then
	touch ./data/config.json
	echo "config.json created" >> ./log.txt
fi


if [ ! -f ./static/data_log.png ]; then
	touch ./static/data_log.png >> ./log.txt
	echo "data_log.png created"
fi

printf "Timestamp; Temp; State_onoff; State_light; State_cooling; State_heating\n" > ./data/data.log
printf "Timestamp; Temp; State_onoff; State_light; State_cooling; State_heating\n" > ./static/data.log

echo "{\"timestamp_measurement\" :  \"2018-12-22_Sat_20:07:28.290691\", \"temp_measured\" : \"none\", \"state_onoff\" : \"off\", \"state_light\" : \"off\", \"state_cooling\" : \"off\", \"state_heating\" : \"off\", \"alert_msg\" : \"-\"}" > ./data/state.json

echo "{\"timestamp_request\" : \"2018-12-22_Sat_20:07:28.290691\", \"temp_desired\" : \"20.0\", \"light_on_time\" : \"07:00\", \"light_off_time\" : \"19:30\"}" > ./data/config.json

echo " " >> ./log.txt
echo "---CONFIG------------------------">> ./log.txt
cat ./data/config.json >> ./log.txt
echo " " >> ./log.txt
echo "---STATE-------------------------">> ./log.txt
cat ./data/state.json >> ./log.txt
echo " " >> ./log.txt
echo "---------------------------------" >> ./log.txt

# stdbuf -o 0 = dont't buffer the terminal; python3 -u = = dont't buffer python; tee -a = append  
python3 -u ./gpio_cleanup.py |& tee log.txt -a &

sleep 2
stdbuf -o 0 python3 -u ./climate_chamber.py |& tee log.txt -a &
ps axo pid,args | grep ./climate_chamber.py >> ./log.txt

sleep 5
touch ./data/firstrun >> ./log.txt
stdbuf -o 0 python3 -u ./server.py |& tee log.txt -a &
ps axo pid,args | grep ./server.py >> ./log.txt
