# Copyright 2017 DiCITS UGR
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


"""Example of Parse and Query JSON-LD and TURTLE Services Definition"""


# Install rdflib and rdflib-jsonld package
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

# Open Turtle file with Service description 
service_def=open("../../occml/catalog/servicesdefinition/turtle/lr.ttl").read()

# Parse Turtle data
g = Graph().parse(data=service_def, format='turtle')


# Query to the service about the next general service data:
#
# - MLService: Internal Name of the service
# - MLdescription: Service Long description
# - MLCreator: Service Creator
# - MLAuthtype: Authentication for the service and type
# - MLInputDescr: Descripcion of te input
# - MLDataSetDescr: Description of the DataSet
# - MLDataFileNameMandatory: Is Mandatory this field
qres_base = g.query(
    """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
       PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
       PREFIX mls: <http://www.w3.org/ns/mls> 
       SELECT  ?mlservice ?mldescription ?mlcreator ?mlcreated ?mlauthtype ?descrinput ?descrdataset ?datafilenamemandatory
        WHERE { 
            ?mlservice dmmlcc:hasOperation ?b .
            ?mlservice dcterms:description ?mldescription .
            ?mlservice dcterms:creator ?mlcreator .
            ?mlservice dcterms:created ?mlcreated .            
            ?mlservice dmmlcc:hasAuthentication ?c .
            ?c waa:requiresAuthentication ?mlauthtype .
            ?b mls:hasInput ?input .
            ?input dcterms:description ?descrinput .
            ?input dmmlcc:contains ?contains .
            ?contains mls:Data ?data .
            ?data mls:DataSet ?dataset . 
            ?dataset dcterms:description ?descrdataset .
            ?dataset dmmlcc:datafilename ?datafilename .
            ?dataset dmmlcc:mandatory ?datafilenamemandatory .
        }
    """)

# Query to the service about the input parameters
#
# - MLParam: Internal name of the param 
# - MLParamDescription: Long description of the param
# - MLParamMandatory; Is the Param Mandatory
# - MLParamDefaultValue: Default value for the param

qres_inputparams = g.query(
    """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
       PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
       PREFIX mls: <http://www.w3.org/ns/mls> 
       SELECT  ?params  ?description ?mandatory ?defaultvalue
       WHERE { 
            ?mlservice dmmlcc:hasInputParameters ?mlserviceinputparameters .
            ?mlserviceinputparameters dmmlcc:Parameters ?params .
            ?params dmmlcc:mandatory ?mandatory .
            ?params dcterms:description ?description .
            ?params dmmlcc:defaultvalue ?defaultvalue .
        }
    """)



# Build the results in a YML string

#First: General Data of the service
for row in qres_base:
    print("MLService: %s\n" \
          "MLDescription: %s\n" \
          "MLCreator: %s\n" \
          "MLCreated: %s\n" \
          "MLAuthType: %s\n" \
          "MLInputDescription: %s\n" \
          "MLDataSetDescription %s\n" \
          "MLDataSetMandatory: %s\n" % row)

#Second: Input Parameter Data
for row in qres_inputparams:
    print("MLInputParameters_%s:" % row[0].split('#')[-1])  
    print(" - name: %s\n - id: %s\n - mandatory: %s\n - defaultvalue: %s" % row) 

