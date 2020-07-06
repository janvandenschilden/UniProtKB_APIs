#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jan Van den Schilden
"""
import time

import urllib.parse
import urllib.request


def UniProtKB_Mapping(
        query, 
        fileName=None,
        From="ACC",
        To="ACC",
        Format="fasta",
        Columns="",
        ):
    """Implementation of the UniProtKB mapping REST api.
    
    UniProtKB provides an REST API to map one database to another, 
    similar to the webservice (https://www.uniprot.org/uploadlists/).  
    More information about the working of the API can be found on:
    https://www.uniprot.org/help/api_idmapping
    
    Parameters
    ----------
    query : str
        The query parameter accepts a sequence of identifiers separated 
        by a space or newline character.  The format of the identifiers 
        depends on the database which is mapped from.
    fileName : str (Default=None)
        The destination path of the file that is downloaded.  If just a
        name is specified, the file is stored in the directory from 
        which the function was executed.  Additionaly the relative or 
        absolute path can be specified.
    From : str (Default='ACC')
        The database from which the identifiers are mapped. The 
        available databases are listed on: 
        https://www.uniprot.org/help/api_idmapping
    To : str (Default='ACC')
        The database to which the identifiers are mapped. The 
        available databases are listed on: 
        https://www.uniprot.org/help/api_idmapping
    Format : str (Default='fasta')
        The file format of the mapped identifiers.  The available format 
        are: 
        html | tab | xls | fasta | gff | txt | xml | rdf | list | rss
    Columns : str (Default="")
        The column information to be downloaded for each entry when the 
        format is tab or xls.
    
    Returns
    -------
    response : str
        The content of the downloaded file in string format
    """
    
    """ The Download of the file is tried 10 times.  Each time the 
    function waits a bit longer.   Sometimes remote servers are busy and
    repeating a failed request helps.
    """
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
            if fileName:
                # Write content to file
                with open(fileName,"w") as f:
                    f.write(response)
            return response
        except:
            print(
                    "request failed, wait for", 
                    i*5,
                    "seconds and try again",
                    )
            time.sleep(i*5)

"""Test
print(
      UniProtKB_Mapping(
              query="P0AFL3",
              fileName="test.fasta",
              ),
      )
"""