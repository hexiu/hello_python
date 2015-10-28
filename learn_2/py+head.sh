#!/bin/bash
#
touch $1
echo "#!/bin/bash/env python3" >> $1
echo "# -*- coding:utf-8 -*-" >> $1
echo "" >> $1
