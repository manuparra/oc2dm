from rdflib import Graph, plugin
from rdflib.serializer import Serializer


jsonld=open("../../occml/catalog/servicesdefinition/turtle/lr.ttl").read()

g = Graph().parse(data=jsonld, format='turtle')


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


for row in qres_base:
    print("MLService: %s\n" \
          "MLDescription: %s\n" \
          "MLCreator: %s\n" \
          "MLCreated: %s\n" \
          "MLAuthType: %s\n" \
          "MLInputDescription: %s\n" \
          "MLDataSetDescription %s\n" \
          "MLDataSetMandatory: %s\n" % row)

for row in qres_inputparams:
    print("MLInputParameters_%s:" % row[0].split('#')[-1])  
    print(" - name: %s\n - id: %s\n - mandatory: %s\n - defaultvalue: %s" % row) 


#from rdflib import Namespace
#n = Namespace("http://dicits.ugr.es/dmmlcc#")
#print n
                        #Subj  Pred  Object
#for s,p,o in g.triples( (None, None, n.MLService) ):
#        print "%s is a Service"%s


