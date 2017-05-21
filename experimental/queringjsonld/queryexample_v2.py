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

def turtle_query(turtle_file):
    # Open Turtle file with Service description 
    service_def=open("{}".format(turtle_file)).read()

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
        SELECT  ?mlservice ?mldescription ?mlcreator ?mlcreated ?mlauthtype ?descrinput ?features ?datafilenamemandatory
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
                ?data mls:Feature ?features . 
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

    return qres_base, qres_inputparams
    """    
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
    """
    
base,params=turtle_query("../../services_definition/turtle/cor.ttl")

for b in base:
    print("MLService: %s\n" \
        "MLDescription: %s\n" \
        "MLCreator: %s\n" \
        "MLCreated: %s\n" \
        "MLAuthType: %s\n" \
        "MLInputDescription: %s\n" \
        "MLDataSetDescription %s\n" \
        "MLDataSetMandatory: %s\n" % b)
        
        
class SPARQL_driver:
    
    def __init__(self,turtle_file=None):
        
        self.service_file=open("{}".format(turtle_file)).read()
        self.graph = Graph().parse(data=self.service_file, format='turtle')
        self.base=None
        self.auth=None
        self.input=None
        self.inputparameters=None
        self.output=None
        self.implementation=None
                
    def _extract_base(self):
        
        query_results = self.graph.query(
            """ PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                PREFIX mls: <http://www.w3.org/ns/mls> 
                SELECT  ?mlservice  ?mldescription ?mlcreator ?mlmodified ?mlpublisher ?mltitle ?mlcomments 
                    WHERE { 
                        ?mlservice dmmlcc:hasOperation ?b .
                        ?mlservice dcterms:description ?mldescription .
                        ?mlservice dcterms:creator ?mlcreator .
                        ?mlservice dcterms:created ?mlcreated .
                        ?mlservice dcterms:modified ?mlmodified .
                        ?mlservice dcterms:publisher ?mlpublisher .
                        ?mlservice dcterms:title ?mltitle .
                        ?mlservice rdfs:comments ?mlcomments .
                    }
            """)
        
        self.base=query_results.serialize(format="json")
          
    def _extract_authentication(self):
        
        query_results = self.graph.query(
            """ PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                PREFIX mls: <http://www.w3.org/ns/mls> 
                SELECT  ?mlservice ?mlauthentication ?mlauthtype ?mlauthdescription
                    WHERE { 
                        ?mlservice dmmlcc:hasAuthentication ?mlauthentication .
                        ?mlauthentication waa:requiresAuthentication ?mlauthtype .
                        ?mlauthentication dcterms:description ?mlauthdescription .
                    }
            """)
        
        self.auth=query_results.serialize(format="json")
        
    def _extract_input(self):
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 SELECT  ?data ?datasettittle ?datasetdescription ?mlformat ?mlformatdescription
                     WHERE { 
                         ?mlservice dmmlcc:hasOperation ?b .
                         ?b mls:hasInput ?input .
                         ?input dmmlcc:contains ?contains .
                         ?contains mls:Data ?data .
                         ?data dcterms:title ?datasettittle .
                         ?data dcterms:description ?datasetdescription .
                         ?data dmmlcc:format ?mlformat .
                         ?mlformat dcterms:description ?mlformatdescription .

                        }
            """)
        
        self.input=query_results.serialize(format="json")
        print self.input
    def _extract_inputparameters(self):
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 SELECT  ?mlinputparameter ?mlinputtitle ?mlinputdescription ?mlinputmandatory ?mlinputdefault 
                     WHERE { 
                         ?mlservice dmmlcc:hasOperation ?b .
                         ?b dmmlcc:hasInputParameters ?inputparameters .
                         ?inputparameters dmmlcc:Parameters ?mlinputparameter .
                         ?mlinputparameter dcterms:title ?mlinputtitle .
                         ?mlinputparameter dcterms:description ?mlinputdescription .
                         ?mlinputparameter dmmlcc:mandatory ?mlinputmandatory .
                         ?mlinputparameter dmmlcc:defaultvalue ?mlinputdefault .
                        }
            """)
        
        self.inputparameters=query_results.serialize(format="json")
        
    def _extract_output(self):
        
        #Check if definition contains Model
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 ASK  { ?x  rdf:type  dmmlcc:PMML_Model }
            """)
        
        _contains_model=query_results.serialize(format="json")
        
        #Check if definition contains ModelEvaluation
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 ASK  { ?x  rdf:type  dmmlcc:ModelEvaluation. }
            """)
        _contains_modelevaluation=query_results.serialize(format="json")
        
        
        #Check if definition contains (in Output) dataSet
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 ASK  { ?x  mls:hasOutput ?output .
                        ?output mls:Data ?mlmodel .                        
                 }
            """)
        _contains_modeldataset=query_results.serialize(format="json")

        self.output=query_results.serialize(format="json")
        
        # Extract Output Segments
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 SELECT ?mlmodel ?mlmodeltitle  ?mlmodeldescription ?mlstoragebucket 
                     WHERE { 
                         ?mlservice dmmlcc:hasOperation ?b .
                         ?b mls:hasOutput ?mloutput .
                         ?mloutput mls:Model ?mlmodel .
                         ?mlmodel dcterms:title ?mlmodeltitle .
                         ?mlmodel dcterms:description ?mlmodeldescription .
                         ?mlmodel dmmlcc:storagebucket ?mlstoragebucket .
                        }
            """)
        
        model=query_results.serialize(format="json")
        print model
        
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 SELECT ?mlmodelevaluation ?mlmodeltitle  ?mlmodeldescription ?mlstoragebucket 
                     WHERE { 
                         ?mlservice dmmlcc:hasOperation ?b .
                         ?b mls:hasOutput ?mloutput .
                         ?mloutput mls:ModelEvaluation ?mlmodelevaluation .
                         ?mlmodelevaluation dcterms:title ?mlmodeltitle .
                         ?mlmodelevaluation dcterms:description ?mlmodeldescription .
                         ?mlmodelevaluation dmmlcc:storagebucket ?mlstoragebucket .
                        }
            """)
        
        modelevaluation=query_results.serialize(format="json")
        print modelevaluation
        
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 SELECT ?mldata ?mltitle ?mldescription ?mlstoragebucket ?mlformat ?mlformatdescription
                     WHERE { 
                         ?mlservice dmmlcc:hasOperation ?b .
                         ?b mls:hasOutput ?mloutput .
                         ?mloutput mls:Data ?mldata .
                         ?mldata dmmlcc:storagebucket ?mlstoragebucket .
                         ?mldata dcterms:description ?mldescription .
                         ?mldata dcterms:title ?mltitle .
                         ?mldata dmmlcc:format ?mlformat .
                         ?mlformat dcterms:description ?mlformatdescription .
                        }
            """)
        
        dataset=query_results.serialize(format="json")
        print dataset
        
    def _extract_implementation(self):
        query_results = self.graph.query(
                 """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                 PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                 PREFIX mls: <http://www.w3.org/ns/mls> 
                 SELECT ?mldescription ?mlimplementationsource ?mlpackage ?mlfunctions
                     WHERE { 
                         ?mlservice dmmlcc:hasOperation ?b .
                         ?b mls:executes ?mlexecute .
                         ?mlexecute dmmlcc:implements ?mlimplements .
                         ?mlimplements dcterms:description ?mldescription .
                         ?mlimplements dmmlcc:ImplementationSource ?mlimplementationsource .
                         ?mlimplements dmmlcc:package ?mlpackage .
                         ?mlimplements dmmlcc:functions ?mlfunctions .
                        }
            """)
        
        self.implementation=query_results.serialize(format="json")

for row in params:
        print("MLInputParameters_%s:" % row[0].split('#')[-1])  
        print(" - name: %s\n - id: %s\n - mandatory: %s\n - defaultvalue: %s" % row) 


sparQL=SPARQL_driver(turtle_file="../../services_definition/turtle/lr.ttl")

sparQL._extract_input()
        
