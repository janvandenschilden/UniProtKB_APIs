#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jan
"""

import os
import time

import urllib.parse
import urllib.request


def UniProtKB_Mapping(fileName,query, From="ACC",To="ACC",Format="fasta",Columns="",outputDir=""):
    for i in range(10):
        try:
            url = 'https://www.uniprot.org/uploadlists/'
            params={
                "query":query,
                "from":From,
                "to":To,
                "format":Format,
                "columns":Columns,
            }
            data = urllib.parse.urlencode(params)
            data = data.encode('utf-8')
            req = urllib.request.Request(url, data)
            with urllib.request.urlopen(req) as f:
                response = str(f.read(),encoding="utf-8")
            outputPath="{}{}".format(outputDir,fileName)
            if outputDir and not os.path.exists(outputDir):
                os.makedirs(outputDir)
            with open(outputPath,"w") as f:
                f.write(response)
            return fileName
        except:
            print("request failed, wait for", i*5,"seconds and try again")
            time.sleep(i*5)
            

UniProtKB_Mapping(
        "test.fasta",
        "P62937",
        )