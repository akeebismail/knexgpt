from chunkr import Chunkr

class TextChunker:
    """Class for chunking text using Chunkr."""
    
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.chunkr = Chunkr(chunk_size=self.chunk_size)
    
    def chunk_text(self, text: str) -> list:
        """Chunk the given text into smaller pieces.
        
        Args:
            text: The text to chunk.
        
        Returns:
            A list of text chunks.
        """
        return self.chunkr.chunk(text) 