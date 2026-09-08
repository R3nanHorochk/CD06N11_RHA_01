#!/bin/bash

RANK=$OMPI_COMM_WORLD_RANK

case $RANK in
    0)
        figlet "$RANK - Ola"
        ;;
    1)
        figlet "$RANK -Mack,"
        ;;
    2)
        figlet "$RANK -sou"
        ;;
    3)
        figlet "$RANK -o"
        ;;
    4)
        figlet "$RANK -Renan Horochk de Andrade"
        ;;
esac
