#!/bin/bash
#
filename=`echo $1".py"`

if [ -f $filename -o -f $1 ];then
    echo "file exists."
    exit 2;
fi
touch $filename
echo "#!/bin/bash/env python3" >> $filename
echo "# -*- coding:utf-8 -*-" >> $filename
echo "" >> $filename
