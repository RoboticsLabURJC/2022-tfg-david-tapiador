from multiprocessing import shared_memory

import numpy as np
from lib.exceptions import InvalidOutputNameException
from lib.utils import create_ndbuffer


class Outputs:
    def __init__(self, output_data) -> None:
        self.created_bool = False
        self.outputs = output_data
        self.shms = []


    def _create_wire(self, name, size):
        shm = shared_memory.SharedMemory(name=name, create=True, size=size)
        self.shms.append(shm)
        return shm

    def check_type(self, typestr):
        # Data types are of the form "<U6", "|u1", "<i8", etc.
        # Isolates numbers at the end of the data type
        chars = int(typestr[2:])
        # In case of float and integer data types, default to 64 bit
        if typestr[1] == 'i' or typestr[1] == 'f':
            suffix_no = chars if chars > 8 else 8
        # In case of Unicode String (U) or String (S) default to 64 chars
        elif typestr[1] == 'U' or typestr[1] == 'S':
            suffix_no = chars if chars > 64 else 64
        # Otherwise simply let the original number be
        else:
            suffix_no = chars
        # Combine with the type with the appropriate suffix
        final_type = typestr[:2] + str(suffix_no)
        return (final_type)

    def share(self, name, data):
        if self.outputs.get(name) is None:
            raise InvalidOutputNameException(f"{name} is not declared in outputs")

        # Store the array data in the appropriate variables
        data = np.array(data)
        shape = np.array(data.shape)
        dim = np.array([len(shape)])
        # Check if the data type needs modifications, get the modified type after calling the function
        final_type = self.check_type(data.dtype.str)
        type = np.array([final_type], dtype='<U6')
        
        if self.outputs[name].get("created", False):
            # Do this if wire has been created
            # Populate SHM buffers with new data on each cycle
            self.outputs[name]["shape"][:] = shape[:]
            self.outputs[name]["type"][:] = type[:]
            self.outputs[name]["data"][:] = data[:]

        else:
            # Create the wires(SHM Objects) to hold the different types 
            # of info that will be passed to the read function





            wires = ''.join(list(self.outputs[name].keys())).count('wire')
            for i in range(wires):
                if i == 0:
                    wire_name = self.outputs[name]["wire"]
                else:
                    wire_name = self.outputs[name][str("wire" + str(i-1) )]





                shape_wire = self._create_wire(wire_name + "_shape", shape.nbytes)
                dim_wire = self._create_wire(wire_name + "_dim", dim.nbytes) 
                type_wire = self._create_wire(wire_name + "_type", type.nbytes)
                # By default allocate 256 bytes to the SHM Object, if the space needed is more then allocate that much space
                data_size = data.nbytes if data.nbytes > 256 else 256 
                data_wire = self._create_wire(self.outputs[name]["wire"], data_size)

                # Create array that accesses SHM Object's buffer to store the dimensions of the data being passed
                self.outputs[name]["dim"] = create_ndbuffer((1,), np.int64, dim_wire.buf)
                self.outputs[name]["dim"][:] = dim[:]
                # Create array that accesses SHM Object's buffer to store the type of the data being passed
                self.outputs[name]["type"] = create_ndbuffer((1,), '<U6', type_wire.buf)            
                self.outputs[name]["type"][:] = type
                # Create array that accesses SHM Object's buffer to store the shape of the data being passed
                self.outputs[name]["shape"] = create_ndbuffer(shape.shape, shape.dtype, shape_wire.buf)
                self.outputs[name]["shape"][:] = shape[:]
                # Create array that accesses SHM Object's buffer to store the actual data being passed
                self.outputs[name]["data"] = create_ndbuffer(shape, type[0], data_wire.buf)
                self.outputs[name]["data"][:] = data
                # Mark output as created
                self.outputs[name]["created"] = True

    def _share_npy_matrix(self, name, matrix, shape):
        dim = np.array([len(matrix.shape)], dtype=np.int64)


        for key in list(self.outputs[name].keys()):
            if(key[0] != "w"):
                continue
            wire_name = self.outputs[name][key]

            
            if self.created_bool:
                self.outputs[name]["shape"][:] = shape[:]
                self.outputs[name]["data"][:] = matrix[:]
            else:







                data_wire = self._create_wire(wire_name, matrix.nbytes)
                shape_wire = self._create_wire(wire_name + "_shape", shape.nbytes)
                dim_wire = self._create_wire(wire_name + "_dim", dim.nbytes)
                self.outputs[name]["dim"] = create_ndbuffer((1,), np.int64, dim_wire.buf)
                self.outputs[name]["dim"][:] = dim[:]
                self.outputs[name]["shape"] = create_ndbuffer(
                    shape.shape, shape.dtype, shape_wire.buf
                )
                self.outputs[name]["shape"][:] = shape[:]
                self.outputs[name]["data"] = create_ndbuffer(
                    shape, matrix.dtype, data_wire.buf
                )
                self.outputs[name]["data"][:] = matrix[:]
                self.outputs[name]["created"] = True
        self.created_bool = True

    def share_image(self, name, image):
        if self.outputs.get(name) is None:
            raise InvalidOutputNameException(f"{name} is not declared in outputs")

        image = np.array(image, dtype=np.uint8)
        if len(image.shape) != 2 and len(image.shape) != 3:
            raise ValueError("Image must be 2D or 3D")

        shape = (
            image.shape
            if len(image.shape) == 3
            else (image.shape[0], image.shape[1], 1)
        )
        shape = np.array(shape, dtype=np.int64)
        self._share_npy_matrix(name, image, shape)

    def share_number(self, name, number):
        # wires = ''.join(list(self.outputs[name].keys())).count('wire')
        # print("CABLES -> "+ str(wires))
        # print("KEYSES -> " + str(self.outputs[name].keys()))
        
        for key in list(self.outputs[name].keys()):
            if(key[0] != "w"):
                continue
            wire_name = self.outputs[name][key]
            if self.outputs.get(name) is None:
                raise InvalidOutputNameException(f"{name} is not declared in outputs")

            if self.created_bool:
                    self.outputs[name][str("data" + key.split("e")[1])][:] = number
                # print("UWU")
            else:





                # wires = ''.join(list(self.outputs[name].keys())).count('wire')
                # for i in range(wires):
                #     # if i == 0:
                #     #     wire_name = self.outputs[name]["wire1"]
                #     # else:
                #     #     # print("ELNOMBRE -> " + str("wire" + str(i)))
                #     wire_name = self.outputs[name][str("wire" + str(i) )]




                data_wire = self._create_wire(
                    wire_name, np.array([1], dtype=np.float64).nbytes
                )
                # if(counter == 0):
                self.outputs[name][str("data" + key.split("e")[1])] = create_ndbuffer(
                    (1,), np.float64, data_wire.buf
                )
                self.outputs[name][str("data" + key.split("e")[1])][:] = number
                self.outputs[name]["created"] = True
            print("NAMES -> " + str(self.outputs[name]))
        self.created_bool = True

    def share_string(self, name, string):
        if self.outputs.get(name) is None:
            raise InvalidOutputNameException(f"{name} is not declared in outputs")

        if self.outputs[name].get("created", False):
            self.outputs[name]["data"][:] = string
        else:






            wires = ''.join(list(self.outputs[name].keys())).count('wire')
            for i in range(wires):
                if i == 0:
                    wire_name = self.outputs[name]["wire"]
                else:
                    wire_name = self.outputs[name][str("wire" + str(i-1) )]




                    

                data_wire = self._create_wire(
                    wire_name, np.array(string, dtype='<U64').nbytes
                )
                self.outputs[name]["data"] = create_ndbuffer(
                    (1,), '<U64', data_wire.buf
                )
                self.outputs[name]["data"][:] = string
                self.outputs[name]["created"] = True

    def share_array(self, name, array):
        if self.outputs.get(name) is None:
            raise InvalidOutputNameException(f"{name} is not declared in outputs")
        array = np.array(array, dtype=np.float64)
        self._share_npy_matrix(name, array, np.array(array.shape, dtype=np.int64))
