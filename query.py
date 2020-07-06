#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jan
"""

import os

import requests


def downloadFile(
        url,
        fileName,
        ):
    """Uses get request to download file from given url.
    
    This function downloads a file from the internet with a given url.  
    When a file with the given name already exists, it is deleted before
    the download starts. The file is downloaded in chunks, so that files
    larger than RAM memory can be downloaded.
    
    Parameters
    ----------
    url : str
        The url from which the file is downloaded. 
    fileName : str
        The name of the new file.
    
    Returns
    -------
    fileName : str
        The name of the new file.
    """
    try:
        # Delete existing files with filename
        os.remove(fileName) 
    except:
        pass
    
    """ Use requests to download file. 
    Works with streams to be able large files without having the need of 
    a large memory.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)
    return fileName


def UniProtKB_Query(
        fileName, 
        query="",
        format="list",
        columns="",
        include="no",
        compress="no",
        limit=0,
        offset=0,
        ):
    """Implementation of the UniProtKB query retrieval REST api.
    
    UniProtKB provides an API to retrieve data by reading a query that 
    is encoded inside the url.  This function accepts queries similar to
    those accepted by the UniProtKB web interface.  In fact, the query 
    builder (https://www.uniprot.org/help/text-search) can be used to 
    construct the query accepted by this function.  If no query is 
    specified, a list of all protein ID's is downloaded. 
    
    More information about the REST API is found on: 
    https://www.uniprot.org/help/api%5Fqueries
    
    Parameters
    ----------
    fileName : str
        The destination path of the file that is downloaded.  If just a
        name is specified, the file is stored in the directory from 
        which the function was executed.  Additionaly the relative or 
        absolute path can be specified.
    query : str (Default='')
        The query that describes the data to be downloaded.  The format 
        is the same as contructed by the query builder available on the 
        UniProtKB webinterface.  
    format : str (Default='list')
        The available format are: 
        html | tab | xls | fasta | gff | txt | xml | rdf | list | rss
    columns : str (Default='')
        The column information to be downloaded for each entry when the 
        format is tab or xls.
    include : str (Default='no')
        Include isoform sequences when the format is fasta.  Include 
        description of referenced data when the format is rdf.  This 
        parameter is ignored for all other formats.
    compress : str (Default='no')
        Download the file as a gzipped compression format when 'yes'.
    limit : int (Default=0)
        Limit the amount of results that is given. 0 means you download 
        all.
    offset : int (Default=0)
        When you limit the amount of results, offset determines where to
        start.
        
    Returns
    -------
    fileName : str
        The name of the downloaeded file.
    """
    def generateURL(
            baseURL, 
            query="",
            format="list",
            columns="",
            include="no",
            compress="no",
            limit="0",
            offset="0",
            ):
        
        """Generate URL with given parameters"""
        def glueParameters(**kwargs):
            gluedParameters = ""
            for parameter, value in kwargs.items():
                gluedParameters+=parameter + "=" + str(value) + "&"
            #Last "&" is removed and spaces are replaced by "+"
            return gluedParameters.replace(" ","+")[:-1] 
        
        return (baseURL 
                + glueParameters(
                        query=query,
                        format=format,
                        columns=columns,
                        include=include,
                        compress=compress,                
                        limit=limit,
                        offset=offset,
                        )
                )
                
    URL = generateURL(
            "https://www.uniprot.org/uniprot/?",
            query=query,
            format=format,
            columns=columns,
            include=include,
            compress=compress,
            limit=limit,
            offset=offset,
            )
    return downloadFile(URL, fileName)
