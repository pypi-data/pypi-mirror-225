#!/bin/sh
echo "Setting,Type,Description" > settings_phyddle_all.csv
tail -n+2 -q settings_simulate.csv >> settings_phyddle_all.csv
tail -n+2 -q settings_format.csv >> settings_phyddle_all.csv
tail -n+2 -q settings_train.csv >> settings_phyddle_all.csv
tail -n+2 -q settings_estimate.csv >> settings_phyddle_all.csv
tail -n+2 -q settings_plot.csv >> settings_phyddle_all.csv
cat settings_phyddle_all.csv | sort | uniq
