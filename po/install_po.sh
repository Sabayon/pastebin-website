#!/bin/sh
make update-po && make && make DESTDIR=$PWD/../i18n install && rm *.mo
