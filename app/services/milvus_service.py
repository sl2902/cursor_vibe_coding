from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from typing import List, Dict, Any, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class MilvusService:
    def __init__(self):
        self.collection_name = settings.milvus_collection_name
        self.dimension = settings.openai_embedding_dimension
        self._connected = False
        self._connect()
    
    def _connect(self) -> None:
        """Connect to Milvus cloud instance"""
        try:
            # Connect to cloud Milvus with authentication
            connections.connect(
                alias="default",
                host=settings.milvus_host,
                port=settings.milvus_port,
                user=settings.milvus_username,
                password=settings.milvus_password,
                secure=True  # Use SSL for cloud connection
            )
            self._connected = True
            logger.info(f"Connected to Milvus cloud at {settings.milvus_host}")
        except Exception as e:
            self._connected = False
            logger.warning(f"Failed to connect to Milvus: {e}")
            logger.warning("App will start without Milvus connection. Some features may be limited.")
    
    def create_collection(self) -> None:
        """Create the document collection if it doesn't exist"""
        if not self._connected:
            logger.warning("Cannot create collection: Milvus not connected")
            return
            
        if utility.has_collection(self.collection_name):
            logger.info(f"Collection {self.collection_name} already exists")
            return
        
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension),
            FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=65535)
        ]
        
        schema = CollectionSchema(fields=fields, description="Document embeddings for chatbot")
        collection = Collection(name=self.collection_name, schema=schema)
        
        # Create index for vector search
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        logger.info(f"Created collection {self.collection_name} with index")
    
    def insert_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Insert documents with their embeddings into Milvus"""
        if not self._connected:
            logger.warning("Cannot insert documents: Milvus not connected")
            return
            
        if not utility.has_collection(self.collection_name):
            self.create_collection()
        
        collection = Collection(self.collection_name)
        collection.load()
        
        try:
            collection.insert(documents)
            collection.flush()
            logger.info(f"Inserted {len(documents)} documents into Milvus")
        except Exception as e:
            logger.error(f"Failed to insert documents: {e}")
            raise
        finally:
            collection.release()
    
    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents based on embedding"""
        if not self._connected:
            logger.warning("Cannot search documents: Milvus not connected")
            return []
            
        if not utility.has_collection(self.collection_name):
            return []
        
        collection = Collection(self.collection_name)
        collection.load()
        
        try:
            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 10}
            }
            
            results = collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                output_fields=["content", "metadata"]
            )
            
            documents = []
            # Handle the search results properly - results is a list of SearchResult objects
            for search_result in results:  # type: ignore
                for hit in search_result:
                    documents.append({
                        "id": hit.id,
                        "content": hit.entity.get("content"),
                        "metadata": hit.entity.get("metadata"),
                        "score": hit.score
                    })
            
            return documents
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            return []
        finally:
            collection.release()
    
    def is_connected(self) -> bool:
        """Check if Milvus connection is active"""
        return self._connected and connections.has_connection("default")


milvus_service = MilvusService() 