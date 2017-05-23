.. OpenCCML documentation master file, created by
   sphinx-quickstart on Tue May 23 00:45:48 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Open Cloud Computing Machine Learning
=====================================
 *Created by Manuel Parra, May 2017*


What's OpenCCML
---------------

ToDo.


General Schema
--------------------


The general scheme of OpenCCML is as follows:

.. image:: images/generalschema.png
   :width: 800 px
   :alt: General schema
   :align: center
   
The units are as follows:

* ML Service Catalog: is a service or tool that allows you to consult the catalog of data mining services available in the system and that are directly consumable. The catalog service reads the definitions of services installed and available in OpenCCML and publishes the catalog of consumable services by end users or other entities. The catalog service allows defining data mining services in two formats: Turtle and JSON-LD.

* MLServices Execution and Management: This service within OpenCCML allows execution of on-demand data mining services requested by end users. The service is responsible for the execution and management of the executions that are performed in OpenCCML. It offers all the necessary characteristics to be able to manage the execution of algorithms.

* ML Dynamic Infrastructure Discovery: This module is in charge of orchestrating the  infrastructure for the execution of services. It also includes tools for discovering OpenCCML services such as availability of R backends, Scala backends, etc.

* High Performance WebServer (Falcon). This is the OpenCCML server that offers all the necessary APIs to be able to consume the catalog of services of  data mining.
   

Service Catalog Schema
----------------------

Translation from Services Definition to OpenAPI: 

.. image:: images/turtletoopenapi.png
   :width: 800 px
   :alt: General schema
   :align: center
   
* ML Service Catalog: is a service or tool that allows you to consult the catalog of data mining services available in the system and that are directly consumable. The catalog service reads the definitions of services installed and available in OpenCCML and publishes the catalog of consumable services by end users or other entities. The catalog service allows defining data mining services in two formats: Turtle and JSON-LD.

* Services Catalog JSONLD / TURTLE is the infrastructure that hosts the Turtle and JSON-LD format definitions. All definitions are available and are published in the catalog if they are stored in this structure.

* JSONLD / TURTLE SPARQL Parser. It is the Processor of Services Definitions. It is in charge of validating and extracting the data and structure of the services to be published. To do this use the SPARQL engine, from where you get all the information of the services, which is directly consumable by the high performance server.

* YAML generator. It is the module in charge of transforming the result of the queries to the services in SPARQL to an format compatible with OpenAPI v2.

* CatalogYAML OpenAPI. YAML processing of the services to be compatible with OpenAPI generates all the information for the catalog of mining services that will be published and executed.

* High Performance WebServer (Falcon). In this segment the server acts as the end user's entry point that wants to consume the OpenCCML-provided API, which has been generated automatically from the Turtle service definition to an RESTFul type API.


OpenAPI Entry Points Implementation Schema
------------------------------------------

Simple execution from the API to the R Wrapper: 

.. image:: images/openapi_to_wrapper.png
   :width: 800 px
   :alt: OpenApi to XWrapper Schema
   :align: center
   
* CatalogYAML OpenAPI. Provides a RESTful API that can be consumed by entities that require it. This API contains the services specified in the catalog. The services contain an EntryPoint.

* EntryPoint: This is defined as the entry point of a service for execution. It is the name of the function or functions that will be executed when making the call to the particular service.

* RWrapper. It is the module able to execute the service since it knows the EntryPoint, the method to execute and all the parameters.

   A. In this case an example is being used for the diagram of a BackEnd which provides an implementation of R to execute code.