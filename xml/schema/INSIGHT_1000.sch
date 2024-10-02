<?xml version="1.0" encoding="UTF-8"?>
  <!-- PDS4 Schematron for Name Space Id:insight  Version:0.5.1.0 - Wed Oct 07 10:51:55 CDT 2015 -->
  <!-- Generated from the PDS4 Information Model Version 1.4.0.1 - System Build 5b -->
  <!-- *** This PDS4 schematron file is an operational deliverable. *** -->
  <!-- This file was copied from ingest_ldd_insight_0510.sch on 10/07/15. -->
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">

  <sch:title>Schematron using XPath 2.0</sch:title>

  <sch:ns uri="http://pds.nasa.gov/pds4/pds/v1" prefix="pds"/>
  <sch:ns uri="http://pds.nasa.gov/pds4/insight/v1" prefix="insight"/>

		   <!-- ================================================ -->
		   <!-- NOTE:  There are two types of schematron rules.  -->
		   <!--        One type includes rules written for       -->
		   <!--        specific situations. The other type are   -->
		   <!--        generated to validate enumerated value    -->
		   <!--        lists. These two types of rules have been -->
		   <!--        merged together in the rules below.       -->
		   <!-- ================================================ -->
  <sch:pattern>
    <sch:rule context="insight:Observation_Information/insight:mission_phase_name">
      <sch:assert test=". = ('Cruise', 'EDL', 'Extended', 'Launch', 'Pre-launch', 'Primary')">
        The attribute insight:mission_phase_name must be equal to one of the following values 'Cruise', 'EDL', 'Extended', 'Launch', 'Pre-launch', 'Primary'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="insight:Observation_Information/insight:product_type">
      <sch:assert test=". = ('EDR', 'ION', 'RAD-raw', 'RDR', 'STATIL-raw', 'TEM-raw', 'TLM-raw', 'TNF', 'TRO', 'WEA')">
        The attribute insight:product_type must be equal to one of the following values 'EDR', 'ION', 'RAD-raw', 'RDR', 'STATIL-raw', 'TEM-raw', 'TLM-raw', 'TNF', 'TRO', 'WEA'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="insight:Observation_Information/insight:start_solar_longitude">
      <sch:assert test="@unit = ('arcmin', 'arcsec', 'deg', 'hr', 'mrad', 'rad')">
        The attribute @unit must be equal to one of the following values 'arcmin', 'arcsec', 'deg', 'hr', 'mrad', 'rad'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="insight:Observation_Information/insight:stop_solar_longitude">
      <sch:assert test="@unit = ('arcmin', 'arcsec', 'deg', 'hr', 'mrad', 'rad')">
        The attribute @unit must be equal to one of the following values 'arcmin', 'arcsec', 'deg', 'hr', 'mrad', 'rad'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="insight:SEIS_Instrument_Parameters/insight:channel_name">
      <sch:assert test=". = ('SP_1', 'SP_2', 'SP_3', 'VBB_1_Position', 'VBB_1_Temperature', 'VBB_1_Velocity', 'VBB_2_Position', 'VBB_2_Temperature', 'VBB_2_Velocity', 'VBB_3_Position', 'VBB_3_Temperature', 'VBB_3_Velocity')">
        The attribute insight:channel_name must be equal to one of the following values 'SP_1', 'SP_2', 'SP_3', 'VBB_1_Position', 'VBB_1_Temperature', 'VBB_1_Velocity', 'VBB_2_Position', 'VBB_2_Temperature', 'VBB_2_Velocity', 'VBB_3_Position', 'VBB_3_Temperature', 'VBB_3_Velocity'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="insight:SEIS_Instrument_Parameters/insight:measurement_type">
      <sch:assert test=". = ('SP_Event', 'VBB_Continuous', 'VBB_Event')">
        The attribute insight:measurement_type must be equal to one of the following values 'SP_Event', 'VBB_Continuous', 'VBB_Event'.</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
