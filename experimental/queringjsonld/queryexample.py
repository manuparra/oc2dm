from rdflib import Graph, plugin
from rdflib.serializer import Serializer


jsonld=open("../../occml/catalog/servicesdefinition/turtle/lr.ttl").read()

g = Graph().parse(data=jsonld, format='turtle')

#print( g.serialize(format='n3') )

#for s, p, o in g:
#    print((s, p, o))

#qres = g.query(
#    """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
#       PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
#       SELECT   ?a 
#        WHERE { 
#            ?a a dmmlcc:MLService .
#        }
#    """)

#for row in qres:
#    print("%s" % row)

qres = g.query(
    """PREFIX dmmlcc: <http://dicits.ugr.es/dmmlcc#>
       PREFIX waa: <http://purl.oclc.org/NET/WebAuthentication> 
       PREFIX mls: <http://www.w3.org/ns/mls> 
       SELECT  ?mlservice ?mldescription ?mlcreator ?mlcreated ?mlauthtype ?inputA
        WHERE { 
            ?mlservice dmmlcc:hasOperation ?b .
            ?mlservice dcterms:description ?mldescription .
            ?mlservice dcterms:creator ?mlcreator .
            ?mlservice dcterms:created ?mlcreated .            
            ?mlservice dmmlcc:hasAuthentication ?c .
            ?c waa:requiresAuthentication ?mlauthtype .
            ?b mls:hasInput ?inputs .
            ?inputs a dmmlcc:MLServiceInput .
            
        }
    """)


for row in qres:
    print("%s %s %s %s %s %s" % row)


#from rdflib import Namespace
#n = Namespace("http://dicits.ugr.es/dmmlcc#")
#print n
                        #Subj  Pred  Object
#for s,p,o in g.triples( (None, None, n.MLService) ):
#        print "%s is a Service"%s


