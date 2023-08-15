#!/usr/bin/env bash
gcc -Wall -Werror CRDFoxDemo.c -o CRDFoxStaticDemo -I../../include  -Wl,-all_load ../../lib/libRDFox-static.a -lstdc++
cp ../data/* .
./CRDFoxStaticDemo
        