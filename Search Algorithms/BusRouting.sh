#!/bin/bash


if [ $1 = "-h" ]
then
    printf "\nUsage: ./BusRouting.sh [PROBLEM_FILE] [HEURISTIC]

HEURISTIC VALUES:\n
  no:\tNo heuristic (heuristic function always returns 0) simple Dijkstra
  MP:\tMinimum Pick-up (Details in heuristics.py)
  MCAC:\tMinimum Cost to Access Children (Details in heuristics.py)\n\n"




  exit 1
fi


if [ "$#" -ne 2 ]; then
  echo "Incorrect number of arguments. Please use the following structure: ./BusRouting.sh [PROBLEM_FILE] [HEURISTIC] " 
  exit 1
fi


python3 route.py $1 $2

