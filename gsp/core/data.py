# -----------------------------------------------------------------------------
# Graphic Server Protocol (GSP)
# Copyright 2023 Vispy Development Team - BSD 2 Clauses licence
# -----------------------------------------------------------------------------
import numpy as np
from . buffer import Buffer
from .. glm import ndarray

class Data:
    
    def __init__(self, uri    : str  = None,
                       nbytes : int  = None,
                       struct : list[tuple[int,type],...] = None):
        """
        Data represents a block of raw binary data, with an
        optional structure. This data is built using the provided uri
        that may either point to an external file, or be a data URI
        that encodes the binary data directly in the JSON file. When
        an uri is provided, data will is fetched just in time and
        stored locally. If no uri has been provided, aempty data will
        be created ex-nihilo just in time. Data can be modified and
        is tracked for any modification.
        
        Examples:

        ```pycon
        >>> data = Data(struct = [(3, np.float32), (2, np.byte)])
        >>> print(len(data))
        2       
        >>> print(np.asarray(data))
        [0 0 0 0 0 0 0 0 0 0 0 0 0 0]
        >>> print(np.asarray(data[0]))
        [0. 0. 0.]
        >>> print(np.asarray(data[1]))
        [0 0]        
        ```

        Parameters:

          uri:
        
            Uniform Resource Identifier from where to fetch data.

          nbytes:
        
            Number of bytes in the data. This is used to create data
            ex-nihilo if no uri has been provided. If a struct is
            provided, the nbytes is discarded in favor of the size of
            the provided structure.

          struct:

            Description of the internal structure of the data as a
            list of (count, dtype) items.


         with `ctype` one of:

         Type       | Data type      | Signed                    | Bits
         ---------- | -------------- | ------------------------- | ----
         np.int8    | signed byte    | signed, two's complement  | 8
         np.uint8   | unsigned byte  | unsigned                  | 8
         np.int16   | signed short   | signed, two's complement  | 16
         np.uint16  | unsigned short | unsigned                  | 16
         np.int32   | signed int     | signed                    | 32
         np.uint32  | unsigned int   | unsigned                  | 32
         np.int64   | signed long    | signed                    | 64
         np.uint64  | unsigned long  | unsigned                  | 64
         np.float32 | float          | signed                    | 32
         np.float64 | double         | signed                    | 64
        """
        
        self._uri = uri
        self._nbytes = nbytes
        self._struct = struct

        if uri is None and nbytes is None and struct is None:
            raise ValueError("One of uri, nbytes or struct needs to be specified")
        
        self._array = None
        self._buffers = []

        if struct is not None:
            self._nbytes = sum([count*np.dtype(dt).itemsize for (count,dt) in struct])
            offset = 0
            for (count, dt) in struct:
                dt = np.dtype(dt)
                nbytes = count*dt.itemsize
                buffer = Buffer(count, dt, self, offset)
                self._buffers.append(buffer)
                offset += nbytes

    def set_data(self, offset: int,
                       data : bytes):

        """Update data content at given offset with new data.
        
        Parameters:

         offset:
        
            Offset in bytes where to start update

         data:
        
            Content to update with.
        """

        buffer = np.asanyarray(self).view(np.ubyte)
        buffer[offset:offset+len(data)] = np.frombuffer(data, np.ubyte)

    def __getitem__(self, index):
        """
        If data is structured, this give access to underlying buffers.
        """
        
        return self._buffers[index]

    def __len__(self):
        """
        If data is structured, this is gives the number of buffers.
        """
        return len(self._buffers)

    def __array__(self):
        """
        Get the underlying array holding the data (just in time creation).
        """
        
        if self._array is None:
            self._array = ndarray.tracked(self._nbytes, np.ubyte)
            if self._uri is not None:
                data = urllib.request.urlopen(uri)
                bytes = data.read()
                self._array[...] = np.frombuffer(bytes, np.ubyte)
        return self._array
