# Copyright 2017 DiCITS UGR
# Created by: Manuel Parra manuelparra@ugr.es
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


"""Parse and Query JSON-LD and TURTLE Services Definition"""

import json
from os import path
from rdflib import Graph

# Config Parameters
from config.config import turtle_folder


class SPARQL_driver:
    """SPARQL_driver allows to access to the TURTLE and JSON-LD Services 
    definitions and extract information about base, auth, input, inputparameters, 
    output and implementation. 
    
    """
    def __init__(self, turtle_file=None, test=False):
        """Query to SPARQL engine.
        
        All information about the service are stored in the following:
        - ``self.base``: contains the base information of the service
        - ``self.auth``: contains authentication properties 
        - ``self.input``: contains input
        - ``self.inputparameters``: contains additional input params
        - ``self.output``: contains the output of the service
        - ``self.implementation``: contanins details of the implementation

        :arg str turtle_file: Filename TTL (turtle extension) 
             to the Service Definition in Turtle
        :arg boolean test: Enable UnitTest for this Class. If ``True`` 
            bypass can be used to execute on arbitrary Services definition. 
            If ``False`` (default) regular method is used.
        
        """
        # Enabled UnitTest, working
        self.service_file = open(path.join(".." if test==False else "", turtle_folder, turtle_file)).read()
        self.graph = Graph().parse(data=self.service_file, format='turtle')
        
        self.base = None
        self.auth = None
        self.input = None
        self.inputparameters = None
        self.output = None
        self.implementation = None
        
        # Extract all function
        self.__extract_all()
        
        
    def __extract_all(self):
        """
        Base Extract All
        """
        self.__extract_base()
        self.__extract_authentication()
        self.__extract_input()
        self.__extract_inputparameters()
        self.__extract_output
        self.__extract_implementation()

    def __extract_base(self):
        """Extract Base Information about the service.
        
        """
        query_results = self.graph.query(
            """ PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                PREFIX mls: <http://www.w3.org/ns/mls#> 
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

        self.base = query_results.serialize(format="json")

    def __extract_authentication(self):
        """Extract Authentication properties about the service.
        
        """
        
        query_results = self.graph.query(
            """ PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
                PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
                PREFIX mls: <http://www.w3.org/ns/mls#> 
                SELECT  ?mlservice ?mlauthentication ?mlauthtype ?mlauthdescription
                    WHERE { 
                        ?mlservice dmmlcc:hasAuthentication ?mlauthentication .
                        ?mlauthentication waa:requiresAuthentication ?mlauthtype .
                        ?mlauthentication dcterms:description ?mlauthdescription .
                    }
            """)

        self.auth = query_results.serialize(format="json")

    def __extract_input(self):
        """Extract Input properties about the service.
        
        Includes DataSet or a Set of Features
        
        """
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX mls: <http://www.w3.org/ns/mls#> 
            SELECT   ?mldatasetdescr ?mldatasettitle ?mlstoragebucket ?mlmandatory ?typeformat ?formatdescr
                WHERE { 
                    ?mlservice dmmlcc:hasOperation ?operation .
					?operation mls:hasInput ?inputparameters .
					?inputparameters dmmlcc:contains ?mlinputparams .
					?mlinputparams mls:Data ?datasetinfo .
					?datasetinfo dcterms:description ?mldatasetdescr . 
					?datasetinfo dcterms:title ?mldatasettitle .
					?datasetinfo dmmlcc:storagebucket ?mlstoragebucket .
					?datasetinfo dmmlcc:mandatory ?mlmandatory .		
					?datasetinfo dmmlcc:format ?format .
					?format rdf:type ?typeformat .
					?format dcterms:description ?formatdescr
                   }
       """)

        self.input = query_results.serialize(format="json")

    def __extract_inputparameters(self):
        """Extract Input Parameters about the service.
        
        Includes all aditional parameters
        
        """
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
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

        self.inputparameters = query_results.serialize(format="json")

    def __extract_output(self):
        """Extract Output about the service.
        
        Model, ModelEvaluation and Dataset can be extracted
        
        """
        # Check if definition contains Model
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
            ASK  { ?x  rdf:type  dmmlcc:PMML_Model }
       """)

        _contains_model = query_results.serialize(format="json")

        # Check if definition contains ModelEvaluation
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
            ASK  { ?x  rdf:type  dmmlcc:ModelEvaluation. }
       """)
        _contains_modelevaluation = query_results.serialize(format="json")

        # Check if definition contains (in Output) dataSet
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
            ASK  { ?x  mls:hasOutput ?output .
                   ?output mls:Data ?mlmodel .                        
            }
       """)
        _contains_dataset = query_results.serialize(format="json")


        # Extract Output Segments: Model
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
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

        model = query_results.serialize(format="json")

        # Extract Output Segments: ModelEvaluation
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
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

        modelevaluation = query_results.serialize(format="json")

        # Extract Output Segments: DataSet
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
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

        dataset = query_results.serialize(format="json")

        self.output=json.dumps({'model':json.loads(model),
                     'modelevaluation':json.loads(modelevaluation),
                     'dataset':json.loads(dataset)})

    def __extract_implementation(self):
        """Extract Implementation about the service.
        
        Implementation Source, Package and function of the service enabled 
        in the BackEnd.
        
        """
        query_results = self.graph.query(
            """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
            PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
            PREFIX mls: <http://www.w3.org/ns/mls#> 
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

        self.implementation = query_results.serialize(format="json")

