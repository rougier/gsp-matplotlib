# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
from __future__ import annotations # Solve circular references with typing
import numpy as np


class Buffer:

    def __init__(self, count : int,
                       dtype : str,
                       data : Data | Buffer = None,
                       offset : int = None,
                       key : str = None):
        """
        Buffer represents a structured view on some
        [Data][gsp.core.Data] or [Buffer][gsp.core.Buffer]. Buffer can be
        a partial or whole view on the underlying source.

        Examples:

        ```pycon
        >>> data = Data(struct = [(3, np.float32), (2, np.byte)])
        >>> print(data[0])
        Buffer(3, float32) # Buffer does not own data
        
        >>> buffer = Buffer(3, np.float32)
        Buffer(3, float32) # Buffer owns data
        ```
        
        Parameters:

          count:

            Number of item

          dtype:

            Type of the item

          data:

            Data or Buffer this buffer is a view of

          offset:

            Offset in bytes in the Data source.

          key:

            When data is a structured buffer, name of the subfield to
            access.
        """
        
        self._count = count
        self._dtype = dtype
        self._data = data
        self._offset = offset
        self._array = None
        self._key = key
        self._buffers = {}

        if dtype.names is not None:
            for name in dtype.names:
                buffer = Buffer(count, dtype[name], self, 0, name)
                self._buffers[name] = buffer

    def set_data(self, offset: int,
                       data : bytes):

        """Update buffer content at given offset with new data.
        
        Parameters:

         offset:
        
            Offset in bytes where to start update

         data:
        
            Content to update with.
        """

        buffer = np.asanyarray(self).view(np.ubyte)
        buffer[offset:offset+len(data)] = np.frombuffer(data, np.ubyte)
        

    def __getitem__(self, key):
        """
        If buffer is structured, this give access to underlying buffers.
        """
        
        return self._buffers[key]

    def __array__(self):
        """
        Get the underlying array holding the data (just in time creation).
        """
        
        if self._array is None:
            # This buffer is a view on Data or Buffer
            if self._data is not None:

                # Buffer is a structured buffer
                if self._key is not None:
                    self._array = np.asanyarray(self._data)[self._key]

                # Buffer is a plain buffer
                else:
                    start = self._offset
                    stop = start + self._count * self._dtype.itemsize
                    self._array = np.asanyarray(self._data)[start:stop].view(self._dtype)
                    
            # This buffer owns its own data
            else:
                self._array[...] = np.empty(self._count, self._dtype)
                
        return self._array

    def __repr__(self):
        return f"Buffer({self._count}, {self._dtype})"
