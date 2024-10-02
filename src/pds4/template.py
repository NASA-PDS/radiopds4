#!/usr/bin/python3
# Copyright (c) 2023, California Institute of Technology ("Caltech").
# U.S. Government sponsorship acknowledged. Any commercial use must be 
# negotiated with the Office of Technology Transfer at the California 
# Institute of Technology.
# 
# This software may be subject to U.S. export control laws. By accepting this 
# software, the user agrees to comply with all applicable U.S. export laws 
# and regulations. User has the responsibility to obtain export licenses, or 
# other export authority as may be required before exporting such information 
# to foreign countries or providing access to foreign persons.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions must reproduce the above copyright notice, this list of
#   conditions and the following disclaimer in the documentation and/or other
#   materials provided with the distribution.
# * Neither the name of Caltech nor its operating division, the Jet Propulsion
#   Laboratory, nor the names of its contributors may be used to endorse or
#   promote products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""

template: a basic module to use templates to create XML labels for PDS4


Author: Dustin Buccino
Email: dustin.r.buccino@jpl.nasa.gov
Affiliation: Planetary Radar and Radio Sciences, Group 332K
             Jet Propulsion Laboratory, California Institute of Technology
Date Created: 13-MAR-2015
Last Modified: 14-SEP-2023

"""

# ---------------------------------------------------------------------------
class XML_Template:
   """
   XML Template class, providing an interface that you can load and modify an XML file
   """

   def __init__(self, filename):
      """ class constructor. read the template file """
      # Load the label template
      f = open( filename, 'r' )
      self.data = f.readlines()
      f.close()

   def __str__(self):
      """ convert this class to a string for printing """
      return ''.join( self.data )

   def replace(self, xml_string, replace_string, replace_one=False):
      """ replace the key of an XML entry matching xml_string that is
          contained in the self.data list. this function will only
          replace it if the entire key-value pair is on a single line """

      # Loop through each line
      for (index, line) in enumerate(self.data):

         # If the XML string exists, replace the value
         if xml_string in line:

            # Determine start and stop index
            start = line.find('>')
            stop = line.rfind('<')

            # Construct the new string
            new = line[:start+1] + replace_string + line[stop:]

            # Replace it in template
            self.data[index] = new

            # Exit out of loop (replace only the first instance)
            if replace_one:
               break

   def insert(self, xml_after, insert_string, location):
      """ insert something after an element that exists in the list."""

      # x[index:index] = ['some','list']

      # Loop through data and find index of matches
      ind = []
      for i, line in enumerate(self.data):
         if xml_after in line:
            ind.append(i)

      # if no index found, ignore
      if len(ind) == 0:
         return

      # Pick the appropriate index
      if location == 'last':
         ind = ind[-1]
      elif location == 'first':
         ind = ind[0]
      else:
         SyntaxError('Invalid "location" input into XML_Template.insert')

      # Insert
      if type(insert_string) is list:
         self.data[ind+1:ind+1] = insert_string
      elif type(insert_string) is str:
         self.data[ind+1:ind+1] = [ insert_string ]

   def read(self, xml_string, searchtype='first'):
      """ read a value from a key-value pair that exists on a single line
          in the XML file """

      val = []

      # Loop through each line
      for (index, line) in enumerate(self.data):

         # If the XML string exists, replace the value
         if xml_string in line:

            # Determine start and stop index
            start = line.find('>')
            stop = line.rfind('<')

            # Return the value
            found_value = line[start+1:stop]
            if searchtype=='first':
               return found_value
            else:
               val.append( found_value )

      if searchtype=='all':
         return val
      elif searchtype=='last':
         return val[-1]
      else:
         IOError('invalid argument `searchtype` into XML_Template.read, must be "first", "last", or "all"')

   def write(self, out_filename):
      """ write the template to file """
      
      fid = open(out_filename, 'w')

      for line in self.data:
         fid.write( line )

      fid.close()

# ---------------------------------------------------------------------------
