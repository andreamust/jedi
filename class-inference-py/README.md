# Empirical Ontology Inference

## TODOs

- **RDFlib** to:
  - fetch labels (Human) for classes/properties (Q5) from wikidata
  - fetch supplementary information from linked graphs
- **Parallelization** of:
  - tree construction (recursive constructor)
  - reading of large mapping files
- **Inference/Deduction** of:
  - classes from tree structure
  - class disjointness
  - identify (non-)/discriminating properties
  - identify and merge identical properties
  - identify and merge direct/direct-normalized/indirect properties
  - property cardinality: min/max required/optional
  - property domain restrictions
  - property range restrictions
- **Evaluation**:
  - develop approach
  - compare to existing formal ontologies
  - compare to [subsymbolic approaches](https://scholar.google.at/scholar_url?url=https://books.google.at/books%3Fhl%3Den%26lr%3Dlang_en%26id%3D18B8EAAAQBAJ%26oi%3Dfnd%26pg%3DPA47%26ots%3Db5AdaAl_8j%26sig%3DVCgXYYJR4rMB4osMtDnEIc5xLIU&hl=en&sa=X&d=16877927513923858388&ei=WXjhYtKECYeymgHbw4vIDg&scisig=AAGBfm1mqXC7yRDo9ghowZMbAYM5RPFuUA&oi=scholaralrt&hist=_ZG20kAAAAAJ:15879895029840466074:AAGBfm1ylym01b_AA29dRrdk0iCCuEtOLw&html=&pos=8&folt=rel)
  - apply to increasingly large KG subsets

## Cheatsheet

In the following we have the components for common KG vocabularies to aid in the process of what we might be able to infer.

Optimally, we can somehow determine procedures to infer all of this.

### RDF vocabulary

Classes:
- `rdf:XMLLiteral` the class of XML literal values
- `rdf:Property` the class of properties
- `rdf:Statement` the class of RDF statements
- `rdf:Alt, rdf:Bag, rdf:Seq` containers of alternatives, unordered containers, and ordered containers (rdfs:Container is a super-class of the three)
- `rdf:List` the class of RDF Lists
- `rdf:nil` an instance of rdf:List representing the empty list

Properties:

- `rdf:type` an instance of rdf:Property used to state that a resource is an instance of a class
- `rdf:first` the first item in the subject RDF list
- `rdf:rest` the rest of the subject RDF list after rdf:first
- `rdf:value` idiomatic property used for structured values
- `rdf:subject` the subject of the RDF statement
- `rdf:predicate` the predicate of the RDF statement
- `rdf:object` the object of the RDF statement
- `rdf:Statement, rdf:subject, rdf:predicate, rdf:object` are used for reification.

### RDFS vocabulary

Classes:

- `rdfs:Resource` the class resource, everything
- `rdfs:Literal` the class of literal values, e.g. strings and integers
- `rdfs:Class` the class of classes
- `rdfs:Datatype` the class of RDF datatypes
- `rdfs:Container` the class of RDF containers
- `rdfs:ContainerMembershipProperty` the class of container membership properties, `rdf:_1`, `rdf:_2`, ..., all of which are sub-properties of rdfs:member

Properties:

- `rdfs:subClassOf` the subject is a subclass of a class
- `rdfs:subPropertyOf` the subject is a subproperty of a property
- `rdfs:domain` a domain of the subject property
- `rdfs:range` a range of the subject property
- `rdfs:label` a human-readable name for the subject
- `rdfs:comment` a description of the subject resource
- `rdfs:member` a member of the subject resource
- `rdfs:seeAlso` further information about the subject resource
- `rdfs:isDefinedBy` the definition of the subject resource

### OWL vocabulary

Classes:

- [`owl:Class`](https://www.w3.org/TR/owl-ref/#Class)
- [`owl:Thing`](http://www.w3.org/TR/2004/REC-owl-semantics-20040210/#owl_Thing)
- [`owl:Nothing`](http://www.w3.org/TR/2004/REC-owl-semantics-20040210/#owl_Nothing)
- `owl:Restriction`
- ...
