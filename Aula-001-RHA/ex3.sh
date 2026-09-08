#!/bin/bash
RANK=$OMPI_COMM_WORLD_RANK

ASCII_CODE=$((65 + RANK))

LETRA=$(printf "\x$(printf %x $ASCII_CODE)")

echo "------------------------------------------"
echo " Rank: $RANK  - Letra: $LETRA"
echo "------------------------------------------"