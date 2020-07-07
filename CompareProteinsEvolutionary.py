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
        # UniProtKb IDs
        self.idA = self._retrieve_id(UniProtKB_idA)
        self.idB = self._retrieve_id(UniProtKB_idB)
        # UniRef50 IDs
        self.UniRef50_idA = self._retrieve_UniRef50_id(self.idA)
        self.UniRef50_idB = self._retrieve_UniRef50_id(self.idB)
        # UniRef50 members and protein sequences
        self.UniRef50_membersA_fasta = \
            self._retrieve_UniRef50_members_fasta(self.UniRef50_idA)
        self.UniRef50_membersB_fasta = \
            self._retrieve_UniRef50_members_fasta(self.UniRef50_idB)
        
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
    
    def _parse_fasta(
            self,
            fasta_string,
            ):
        """ Parse fasta string into dictionary.
        
        This function parses the fasta file (in string format) into a 
        dictionary of protein sequences.  
        
        Parameters
        ----------
        fasta_string : str
            A fasta file in string format.  
        
        Returns
        -------
        fasta_dictionary : dict
            The fasta file in dictionary format.  
                key : ID
                value : protein sequence
        """
        fasta_dictionary = dict()
        fasta_lines = (line for line in fasta_string.split("\n"))
        for line in fasta_lines:
            if line.startswith(">"):
                Id = line.replace(">","")\
                    .split("|")[1]
                fasta_dictionary[Id] = ""
            else:
                fasta_dictionary[Id] += line.strip()
        return fasta_dictionary
    
    def _retrieve_UniRef50_members_fasta(
            self,
            UniRef50_id,
            ):
        """Retrieve fasta file of UniRef50 members.
        
        All members of an UniRef50 cluster have a sequence identity of 
        50% or more.  This means they are homologues to each other.  
        The UniProtKB mapping API is used to retrieve those members in 
        fasta format.  The resulting string is subsequently parsed to a 
        dictionary.
        
        Parameters
        ----------
        UniRef50_id : str
            The UniRef50 identifier.
        
        Returns
        -------
        UniRef50_members_fasta : dict
            Returns a dictionary of the members and their protein 
            sequence.  
                key : UniProtKB ID 
                value : protein sequence
        """
        # Retrieve fasta string with UniProtKB mapping service
        UniRef50_members_fasta_str = UniProtKB_Mapping(
                UniRef50_id,
                From="NF50",
                To="ACC",
                Format="fasta",
                )
        # Parse string into dictionary of protein sequences
        UniRef50_members_fasta = \
            self._parse_fasta(UniRef50_members_fasta_str)
        return UniRef50_members_fasta
        
    
    
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
print(
      C.UniRef50_membersA_fasta,
      C.UniRef50_membersB_fasta,
      )
      