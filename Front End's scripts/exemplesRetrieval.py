import xml.etree.cElementTree as et
from  xml.etree.cElementTree import parse
from py4j.java_gateway import *
from py4j.java_gateway import JavaGateway, GatewayParameters
import zipfile
import unicodedata
import pickle

def initializingJar():
    port = launch_gateway()
    gateway = JavaGateway(
        gateway_parameters=GatewayParameters(port=port),
        callback_server_parameters=CallbackServerParameters(port=0))
    # with zipfile.ZipFile("FarasaSegmenterJar.jar") as z:
    # z.extractall()
    # gateway = JavaGateway(gateway_parameters=GatewayParameters( port=3005),start_callback_server=True)
    object = gateway.jvm.com.qcri.farasa.segmenter.Farasa()
    return object

def lemmatize(object,text):

    data = object.lemmatizeLine(text)
    # object = gateway.entry_point.Farasa()
    # gateway.shutdown_callback_server()
    # gateway.shutdown()
    return data
