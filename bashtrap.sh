#!/bin/bash
# bash trap command
trap bashtrap INT
# bash clear screen command
clear;
# bash trap function is executed with CTRL-C is pressed:
# bash prings message => Executing bash trap subroutine!
bashtrap()
{
    echo "CTRL+C Detected !...executing bash trap!"
    `exit`
}
# for loop from 1/10 to 10/10
for a in `seq 1 10`; do
    echo "$a/10 to Exit."
    sleep 1;
done
echo "Exit bash trap example!"