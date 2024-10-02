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

=====================
pds4.inventory_update
=====================

Update an already-created PDS4 inventory collection CSV with more data

Author: Dustin Buccino
Email: dustin.r.buccino@jpl.nasa.gov
Affiliation: Planetary Radar and Radio Sciences, Group 332K
             Jet Propulsion Laboratory, California Institute of Technology
Date Created: 30-JAN-2019
Last Modified: 14-SEP-2023

Synopsis::

   pds4.inventory_update -c <csv file> <list_of_files...>

Options::

   Required:
      -m: modification history string update
      -c: collection csv file

"""

import os
import sys
from argparse import ArgumentParser
from datetime import datetime
from pds4.template import XML_Template
import pds4.util as util

MOD_HISTORY_TEMPLATE = """            <Modification_Detail>
                <modification_date>{modification_date}</modification_date>
                <version_id>{version_id}</version_id>
                <description>{description}</description>
            </Modification_Detail>
"""

def main( args ):
   """ Main program function. This is the first executed code,
       and contains the necessary argument parsing and dump functions """

   # ------------------------------------------------------------------------
   # Get a list of logicial identifiers

   identifiers = []
   for filename in args.Input:
      # Read the logicial identifier
      Template = XML_Template( filename )
      lid = Template.read('<logical_identifier>')
      version = Template.read('<version_id>','first')
      identifiers.append(lid+'::'+version)
   print( "Found a total of %d logical identifiers in the provided files." % len(identifiers) )

   # Get the current number of records in the csv file
   collection_filename = args.collection
   collection_label_filename = util.label_filename( collection_filename )
   Template = XML_Template( collection_label_filename )
   n = int( Template.read('<records>') ) 
   version = Template.read('<version_id>', 'all')
   if len(version) < 2:
      IOError("ERROR: This collection is missing entries to <version_id>")
   current_version = version[0]
   version = [ float(v) for v in version[1:] ]
   mod_date = Template.read('<modification_date>', 'all')
   if len(mod_date) != len(version):
      IOError("ERROR: Invalid syntax in <Modification_History>, check the collection xml label...")
   num_modifications = len(version)
   print( "This file has been modified %d times" % num_modifications )
   print( "The last modification date was %s with version id %.1f" % (mod_date[-1], version[-1]) )
   print( "The label says there are currently %s records in the collection." % str(n) )

   # Write the new records to CSV file
   fid = open( collection_filename, 'w' )
   if args.keep:
      fid.write( ''.join(data) )
      count = n + len(identifiers)
   else:
      count = len(identifiers)
   for lid in identifiers:
      outstr = "P,%s\r\n" % lid
      fid.write(outstr)
   fid.close()

   # Add new modification History
   next_version = max(version) + 1
   mod_detail = MOD_HISTORY_TEMPLATE.format( modification_date = datetime.now().strftime('%Y-%m-%d'),
                                             version_id = '%.1f' % next_version,
                                             description = args.message )
   print( "The version number has been incremented to %.1f" % next_version )
   Template.insert('<Modification_History>', mod_detail, 'first')

   # Update the label
   print( "There are now %d records in the collection." % count )
   Template.replace( '<records>', str(count) )
   Template.write( collection_label_filename )

# If called as a script, go to the main() function immediately
if __name__ == "__main__":

   # Setup the parser
   parser = ArgumentParser( prog='pds4.inventory_update',
                            description='Update the inventory for a collection' )

   # Add arguments
   parser.add_argument( 'Input', type=str, nargs='+',
                        help='List of XML labels to add to the collection' )
   parser.add_argument( '-c', '--collection', dest='collection', type=str, required=True,
                        help='the CSV collection to update' )
   parser.add_argument( '-m', '--message', dest='message', type=str, required=True,
                        help='modification history update message' )
   parser.add_argument( '-k', '--keep', dest='keep', default=False, action='store_true',
                        help='keep current records in the collection instead of overwriting' )

   # Parse the command line automatically
   args = parser.parse_args()

   # Error checking
   if not os.path.exists( args.collection ):
      parser.error( 'Template file %s does not exist' % args.template )

   main( args )
