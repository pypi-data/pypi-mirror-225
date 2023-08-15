#!/usr/bin/env bash
gcc -Wall -Werror CRDFoxDemo.c -o CRDFoxStaticDemo -I../../include  -Wl,--whole-archive ../../lib/libRDFox-static.a -Wl,--no-whole-archive -lstdc++ -ldl -lpthread -lm
cp ../data/* .
./CRDFoxStaticDemo
        