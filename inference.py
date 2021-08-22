#!/usr/bin/env python3
"""
 Copyright (c) 2018 Intel Corporation.

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import logging as log
from openvino.inference_engine import IENetwork, IECore


class Network:
    """
    Load and configure inference plugins for the specified target devices 
    and performs synchronous and asynchronous modes for the specified infer requests.
    """

    def __init__(self):
        
        ### TODO: Initialize any class variables desired ###
        self.plugin = None
        self.network = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request = None

    def load_model(self, model, CPU_EXTENSION, DEVICE, console_output = False):
        ### TODO: Load the model ###
        model_xml = model
        model_bin = os.path.splitext(model_xml)[0] + ".bin"
        self.plugin = IECore()
        self.network = IENetwork(model=model_xml, weights=model_bin)
        
        ### TODO: Check for supported layers ###
        if not all_layers_supported(self.plugin, self.network, console_output=console_output):
            self.plugin.add_extension(CPU_EXTENSION, DEVICE)
            self.exec_network = self.plugin.load_network(self.network, DEVICE)
        ### TODO: Add any necessary extensions ###
                    ###input layer ###
        self.input_blob = next(iter(self.network.inputs))
        self.output_blob = next(iter(self.network.outputs))
        
        ### TODO: Return the loaded inference plugin ###
        ###return
        ### Note: You may need to update the function parameters. ###
        return

    def get_input_shape(self):
        ### TODO: Return the shape of the input layer ###
        input_shapes = {}
        for inp in self.network.inputs:
            input_shapes[inp] = (self.network.inputs[inp].shape)
        return input_shapes

    def exec_net(self, net_input, request_id):
        ### TODO: Start an asynchronous request ###
        ### TODO: Return any necessary information ###
        
        self.infer_request_handle = self.exec_network.start_async(request_id, inputs=net_input)
        
        ### Note: You may need to update the function parameters. ###
        return

    def wait(self):
        ### TODO: Wait for the request to be complete. ###
        ### TODO: Return any necessary information ###
        ### Note: You may need to update the function parameters. ###
        status = self.infer_request_handle.wait()
        return

    def get_output(self):
        ### TODO: Extract and return the output results
        ### Note: You may need to update the function parameters. ###
        out = self.infer_request_handle.outputs[self.output_blob]
        return out

    
def all_layers_supported(engine, network, console_output=False):
    ### TODO check if all layers are supported
    ### returns True if all supported, else returns False 
    
    layers_supported = engine.query_network(network, device_name='CPU')
    layers = network.layers.keys()

    all_supported = True
    for layer in layers:
        if layer not in layers_supported:
            all_supported = False
        #added log changes as required to unsupported layers
            not_supported_layer = \
                [layer for layer in layers if layer not in layers_supported]
            if len(not_supported_layer) != 0:
                log.error ("Following layers are not supported by "
                          "the plugin for specified device {}:\n {}".
                          format(self.plugin.device,
                                 ', '.join(not_supported_layer)))
                log.error("Please specify CPU extensions library path"
                          " in command line parameters using -l "
                          "or --cpu_extension command line argument")
                sys.exit(1)

    return all_supported
