from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import yaml

class YamlGenerator:

    def __init__(self, input_file, output_file):
        service_def=open("../services_definition/turtle/{}".format(input_file)).read()

        g = Graph().parse(data=service_def, format='turtle')

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
       
        parameters = []
        for row in qres_inputparams:
            name = row[0][:]
            description = row[1][:]
            if row[2] == 'optional':
                required = False
            else:
                required = True
            default = row[3][:]
            parameters.append({'name':name, 'description':description, 'required':required, 'default':default})
        print (yaml.dump(parameters, default_flow_style=False, indent=2)) 
       # stream = open('document.yaml', 'w')
       # yaml.dump(parameters, stream, default_flow_style=False, indent=2)
YamlGenerator("lr.ttl", "asd")