"""
Base ontology module for managing RDF/OWL schemas and relationships.
"""
from typing import Optional, Dict, List, Any
from pathlib import Path
import logging

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
from owlready2 import get_ontology, World

logger = logging.getLogger(__name__)

class OntologyManager:
    """Manages ontology creation, updates, and validation."""
    
    def __init__(self, base_uri: str, storage_path: Optional[Path] = None):
        """Initialize the ontology manager.
        
        Args:
            base_uri: Base URI for the ontology
            storage_path: Optional path to store ontology files
        """
        self.base_uri = base_uri
        self.storage_path = storage_path or Path("./ontologies")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize RDF graph
        self.graph = Graph()
        self.ns = Namespace(base_uri)
        
        # Initialize OWL ontology
        self.world = World()
        self.onto = get_ontology(base_uri)
        
        # Bind common namespaces
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        self.graph.bind("ns", self.ns)
    
    def add_class(self, class_name: str, parent_class: Optional[str] = None) -> URIRef:
        """Add a new class to the ontology.
        
        Args:
            class_name: Name of the class to add
            parent_class: Optional parent class name
            
        Returns:
            URIRef of the created class
        """
        class_uri = self.ns[class_name]
        self.graph.add((class_uri, RDF.type, OWL.Class))
        
        if parent_class:
            parent_uri = self.ns[parent_class]
            self.graph.add((class_uri, RDFS.subClassOf, parent_uri))
        
        return class_uri
    
    def add_property(
        self,
        prop_name: str,
        domain: Optional[str] = None,
        range_: Optional[str] = None,
        prop_type: str = "ObjectProperty"
    ) -> URIRef:
        """Add a new property to the ontology.
        
        Args:
            prop_name: Name of the property
            domain: Optional domain class name
            range_: Optional range class name
            prop_type: Type of property (ObjectProperty or DatatypeProperty)
            
        Returns:
            URIRef of the created property
        """
        prop_uri = self.ns[prop_name]
        
        if prop_type == "ObjectProperty":
            self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
        else:
            self.graph.add((prop_uri, RDF.type, OWL.DatatypeProperty))
            
        if domain:
            domain_uri = self.ns[domain]
            self.graph.add((prop_uri, RDFS.domain, domain_uri))
            
        if range_:
            range_uri = self.ns[range_] if prop_type == "ObjectProperty" else range_
            self.graph.add((prop_uri, RDFS.range, range_uri))
            
        return prop_uri
    
    def save(self, format: str = "turtle") -> None:
        """Save the ontology to file.
        
        Args:
            format: Format to save in (turtle, xml, etc.)
        """
        file_path = self.storage_path / f"ontology.{format}"
        self.graph.serialize(destination=str(file_path), format=format)
        logger.info(f"Saved ontology to {file_path}")
    
    def load(self, file_path: Path, format: str = "turtle") -> None:
        """Load ontology from file.
        
        Args:
            file_path: Path to ontology file
            format: Format of the file
        """
        self.graph.parse(str(file_path), format=format)
        logger.info(f"Loaded ontology from {file_path}")
    
    def validate(self) -> List[str]:
        """Validate the ontology for consistency.
        
        Returns:
            List of validation messages
        """
        # TODO: Implement validation rules
        return [] 