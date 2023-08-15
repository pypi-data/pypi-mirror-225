#!/usr/bin/env bash
g++ -Wall -Werror -std=gnu++11 CppRDFoxDemo.cpp -o CppRDFoxStaticDemo -I../../include ../../lib/libRDFox-static.a -Wl,-all_load
cp ../data/* .
./CppRDFoxStaticDemo
        