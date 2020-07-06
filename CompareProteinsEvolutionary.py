#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jan Van den Schilden
"""
from mapping import UniProtKB_Mapping


class CompareProteinsEvolutionary:
    def __init__(
            self,
            UniProtKB_idA,
            UniProtKB_idB,
            ):
        self.idA = self._retrieve_id(UniProtKB_idA)
        self.idB = self._retrieve_id(UniProtKB_idB)
        self.UniRef50_idA = self._retrieve_UniRef50_id(self.idA)
        self.UniRef50_idB = self._retrieve_UniRef50_id(self.idB)
        
    def _retrieve_id(
            self,
            UniProtKB_id,
            ):
        """ Retrieve the UniProtKB id.
        
        Sometimes, UniProtKB updates identifiers.  This method maps the 
        a UniProtKB identifier to its own database to retrieve the 
        latest version of this identifier.
        
        Parameters
        ----------
        UniProtKB_id : str
            The UniProtKB_id identifier (can be outdated).
            
        Returns
        -------
        new_UniProtKB_id : str
            When the UniProtKB_id is outdated, the up to date identifier
            is returned instead.  Otherwise, the original identifier 
            is returned.
        """
        new_UniProtKB_id = UniProtKB_Mapping(
                UniProtKB_id,
                Format="list",
                ).strip()
        return new_UniProtKB_id
    
    def _retrieve_UniRef50_id(
            self,
            UniProtKB_id,
            ):
        """ Retrieve the UniRef50 identifier.
        
        UniProtKB clusters all of the protein sequences by sequence 
        identity, called UniRef groups.  All members of a UniRef50 group
        will have at most 50 percent sequence identity.
        
        Parameters
        ----------
        UniProtKB_id : str
            The UniProtKB_id identifier (can be outdated).
            
        Returns
        -------
        UniRef50_id : str
            The UniRef50 identifier.
        """
        UniRef50_id = UniProtKB_Mapping(
                UniProtKB_id,
                From="ACC",
                To="NF50",
                Format="list",
                ).strip()
        return UniRef50_id
        
    
    
PPIA_ID = "P0AFL3"
PPIB_ID = "P23869" 
C = CompareProteinsEvolutionary(PPIA_ID,PPIB_ID)
print(
      C.idA,
      C.idB,
      )
print(
      C.UniRef50_idA,
      C.UniRef50_idB,
      )
      