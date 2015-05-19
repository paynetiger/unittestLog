#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

class pipeRewrite:
    def __init__(self, name):
        stdout_backup = os.dup(1)
        stderr_backup = os.dup(2)

        stream = open('./%s.txt' % name, 'w')
        os.dup2(stream.fileno(), 1)
        os.dup2(stream.fileno(), 2)
        stream.close()