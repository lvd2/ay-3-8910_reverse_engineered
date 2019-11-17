#!/bin/bash

rm -rf ./work/
vlib work

vlog -sv -vopt -incr +define+PSG_FILE="\"$1\"" +define+DUMP_FILES="\"$2\"" psg.v savechan.v render.v aytab.v ../ay_model.v

vsim -c -vopt work.render -do "run -all; exit"

