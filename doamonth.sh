#!/bin/bash

ls -1 /var/www/html/weather/raw/calib/$1/$1-$2 | while read i
do 
	 perl LoadMySql.pl /var/www/html/weather/raw/calib/$1/$1-$2/$i	
done

