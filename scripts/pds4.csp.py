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

========
pds4.csp
========

Create a PDS4-style XML label for a TRK 2-23 (DSN media interface) file

Works on both Ionosphere (ION) and Troposphere (TRO) files

This program requires a template file of an XML label, usually mission-specific

Author: Dustin Buccino
Email: dustin.r.buccino@jpl.nasa.gov
Affiliation: Planetary Radar and Radio Sciences, Group 332K
             Jet Propulsion Laboratory, California Institute of Technology
Date Created: 13-MAR-2015
Last Modified: 14-SEP-2023

Synopsis::

   pds4.csp.py -t <XML_template> [options] <csp_file>

Options::

Required:
   -t <XML_template>, the XML label template for the TRK 2-23 file. this file
                      will be mission-specific

Optional:
   -r <filename>, rename the TRK-2-24 weather file to this convention for the label
                     {start_year} = starting year of the file
                      {start_doy} = starting day of year of the file
                     {start_time} = starting time of file (UTC)
                       {end_year} = ending year of the file
                        {end_doy} = ending day of year of the file
                  for example, "dawnvegr_{start_year}_{start_doy}.csp"

"""

import os
import sys
from argparse import ArgumentParser
from datetime import datetime
import shutil
from pds4.template import XML_Template
import pds4.util as util

def main( args ):
   """ Main program function. This is the first executed code,
       and contains the necessary argument parsing and dump functions """

   # Get the WEA file we're working with
   csp_file = args.Input

   # Loop through and parse the records
   # Load file line by line
   data = []
   n_records = 0
   first = False
   with open(csp_file, 'r') as f:
      for line in f:
         if 'FROM' in line and not first:
            s = line.find('FROM(')
            e = s + line[s:].find(')')
            tstr = line[s+5:e]
            if len(tstr) == 14: 
               fmt = '%y/%m/%d,%H:%M'
            elif len(tstr) == 17:
               fmt = '%y/%m/%d,%H:%M:%S'
            else: 
               fmt = '%y/%m/%d,%H:%M:%S.%f'
            start_time = datetime.strptime( tstr, fmt )
            first = True
         if 'TO' in line:
            s = line.find('TO(')
            e = s + line[s:].find(')')
            tstr = line[s+3:e]
            if len(tstr) == 14: 
               fmt = '%y/%m/%d,%H:%M'
            elif len(tstr) == 17:
               fmt = '%y/%m/%d,%H:%M:%S'
            else: 
               fmt = '%y/%m/%d,%H:%M:%S.%f'
            end_time = datetime.strptime( tstr, fmt )
         n_records = n_records + 1

   # Rename the CSP file if necessary, and change the name of the TNF file in the label
   if args.rename is not None:
      csp_new_name = args.rename.format( start_year = start_time.strftime('%Y'),
                                            start_doy = start_time.strftime('%j'),
                                            start_time = start_time.strftime('%H%M'),
                                            end_year = end_time.strftime('%Y'),
                                            end_doy = end_time.strftime('%j') )
      os.rename( csp_file, csp_new_name )
      csp_file = csp_new_name

   # Read template
   Template = XML_Template( args.template )

   # form new logical identifier
   file_base = os.path.basename( csp_file ).split('.')[0]
   lid = Template.read('<logical_identifier>').rsplit(':',1)[0] + ':' + file_base

   # Fill the label with information
   Template.replace( '<logical_identifier>', lid )
   Template.replace( '<modification_date>', datetime.now().strftime('%Y-%m-%d') )
   Template.replace( '<start_date_time>', start_time.strftime('%Y-%m-%dT%H:%M:%SZ') )
   Template.replace( '<stop_date_time>', end_time.strftime('%Y-%m-%dT%H:%M:%SZ') )
   Template.replace( '<file_name>', csp_file )
   Template.replace( '<local_identifier>', file_base )
   Template.replace( '<creation_date_time>', end_time.strftime('%Y-%m-%dT%H:%M:%SZ') )
   Template.replace( '<md5_checksum>', util.md5hashfile(csp_file) )
   Template.replace( '<file_size unit="byte">', str(os.path.getsize(csp_file)) )
   Template.replace( '<records>', str(n_records), True )
   
   # Write label
   out_filename = util.label_filename( csp_file )
   Template.write( out_filename )

# If called as a script, go to the main() function immediately
if __name__ == "__main__":

   # Setup the parser
   parser = ArgumentParser( prog='pds4.csp',
                            description='Label a DSN TRK-2-23 file with a PDS4 XML label' )

   # Add arguments
   parser.add_argument( 'Input', type=str,
                        help='the name of the CSP file to label' )
   parser.add_argument( '-t', '--template', dest='template', type=str, required=True,
                        help='the XML label template' )
   parser.add_argument( '-r', '--rename', dest='rename', default=None,
                        help='rename the input tnf_file to this naming convention  ' + \
                             'example: "MROMAGR_{start_year}_{start_doy}.CSP       ' + \
                             'List of naming options:                              ' + \
                             ' {start_year} = starting year of the file            ' + \
                             ' {start_doy} = starting day of year of the file      ' + \
                             ' {start_time} = starting time of file (UTC)          ' + \
                             ' {end_year} = ending year of the file                ' + \
                             ' {end_doy} = ending day of year of the file          ' )

   # Parse the command line automatically
   args = parser.parse_args()

   # Error checking - does the file exist
   if not os.path.exists( args.Input ):
      parser.error( 'File %s does not exist' % args.Input )
   if not os.path.exists( args.template ):
      parser.error( 'Template file %s does not exist' % args.template )

   # Run program
   main( args )
