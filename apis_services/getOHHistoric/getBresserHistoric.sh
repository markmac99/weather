#!/bin/bash

influx -database openhab -pretty -precision rcf3339 -execute \
"select * from windavg_b,windmax_b,winddir_b,rain_b,Hum1,BresserWS_temp where time >= '2024-08-29T00:00:00Z' and time < '2024-09-23T13:02:00Z'" > /tmp/histdata.csv
