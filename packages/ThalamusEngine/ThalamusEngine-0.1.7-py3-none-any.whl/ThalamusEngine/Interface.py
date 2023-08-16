import os
import ctypes
import threading
import numpy as np
import ctypes
import platform
import time

ShowText = True


def OnMsgText():
    global ShowText
    ShowText = True


def OffMsgText():
    global ShowText
    ShowText = False


def threadtest1(AsmFileName, SimWindowText):
    p1 = ctypes.c_char_p()
    p1.value = AsmFileName
    p2 = ctypes.c_char_p()
    p2.value = SimWindowText
    Simul3DFunc(0, p1, p2)


def InitSimulation(AsmFileName, SimWindowText):
    DllPath = ""
    OSName = platform.system()
    print("OS:", OSName)
    if OSName == "Linux":
        DllPath = os.path.dirname(__file__) + '/Lib/thalamus.so'
        print("DllPath:", DllPath)
        TestDLL = ctypes.cdll.LoadLibrary(DllPath)  # ctypes.WinDLL(DllPath)
    elif OSName == "Windows":
        DllPath = os.path.dirname(__file__) + '\\Lib\\thalamus.dll'
        print("DLL Paht:", DllPath)
        TestDLL = ctypes.WinDLL(DllPath)

    global Simul3DFunc
    Simul3DFunc = TestDLL['Simul3DStart']
    Simul3DFunc.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)

    t1 = threading.Thread(target=threadtest1, args=(AsmFileName, SimWindowText))
    t1.start()

    global GetColorImageFunc
    GetColorImageFunc = TestDLL['GetColorImage']
    GetColorImageFunc.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_int)
    GetColorImageFunc.restype = ctypes.c_int

    global GetDepthMapFunc
    GetDepthMapFunc = TestDLL['GetDepthMap']
    GetDepthMapFunc.argtypes = (
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, ctypes.c_int)
    GetDepthMapFunc.restype = ctypes.c_int

    global GetColorImageNoShadeFunc
    GetColorImageNoShadeFunc = TestDLL['GetColorImageNoShade']
    GetColorImageNoShadeFunc.argtypes = (ctypes.c_void_p, ctypes.c_void_p,
                                         ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                         ctypes.c_int, ctypes.c_int)
    GetColorImageNoShadeFunc.restype = ctypes.c_int

    global GetShadeImageFunc
    GetShadeImageFunc = TestDLL['GetShadeImage']
    GetShadeImageFunc.argtypes = (
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, ctypes.c_int)
    GetShadeImageFunc.restype = ctypes.c_int

    global SetObjectFunc
    SetObjectFunc = TestDLL['SetObject']
    SetObjectFunc.argtypes = (ctypes.c_int, ctypes.c_int,
                              ctypes.c_double, ctypes.c_double, ctypes.c_double,
                              ctypes.c_double, ctypes.c_double, ctypes.c_double,
                              ctypes.c_double, ctypes.c_double, ctypes.c_double,
                              ctypes.c_double, ctypes.c_double, ctypes.c_double)
    SetObjectFunc.restype = ctypes.c_int

    global GetBoundBoxFunc
    GetBoundBoxFunc = TestDLL['GetBoundBox']
    GetBoundBoxFunc.argtypes = (ctypes.c_void_p,)
    GetBoundBoxFunc.restype = ctypes.c_int

    global SetGlobalPositionFunc
    SetGlobalPositionFunc = TestDLL['SetGlobalPosition']
    SetGlobalPositionFunc.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double)

    global SetGlobalAttitudeFunc
    SetGlobalAttitudeFunc = TestDLL['SetGlobalAttitude']
    SetGlobalAttitudeFunc.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double)

    global GetSeableObjMaskFunc
    GetSeableObjMaskFunc = TestDLL['GetSeableObjMask']
    GetSeableObjMaskFunc.argtypes = (ctypes.c_void_p,)
    GetSeableObjMaskFunc.restype = ctypes.c_int

    global SetObjectTypeFunc
    SetObjectTypeFunc = TestDLL['SetObjectType']
    SetObjectTypeFunc.argtypes = (ctypes.c_int, ctypes.c_int,)
    SetObjectTypeFunc.restype = ctypes.c_int

    global SetObjPosFunc
    SetObjPosFunc = TestDLL['SetObjectPos']
    SetObjPosFunc.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    SetObjPosFunc.restype = ctypes.c_int

    global SetObjAttFunc
    SetObjAttFunc = TestDLL['SetObjectAtt']
    SetObjAttFunc.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    SetObjAttFunc.restype = ctypes.c_int

    global SetObjAmpFunc
    SetObjAmpFunc = TestDLL['SetObjectAmp']
    SetObjAmpFunc.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    SetObjAmpFunc.restype = ctypes.c_int

    global SetObjClrFunc
    SetObjClrFunc = TestDLL['SetObjectClr']
    SetObjClrFunc.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double)
    SetObjClrFunc.restype = ctypes.c_int

    global SetObjNameFunc
    SetObjNameFunc = TestDLL['SetObjName']
    SetObjNameFunc.argtypes = (ctypes.c_int, ctypes.c_char_p)

    global GetObjNameFunc
    GetObjNameFunc = TestDLL['GetObjName']
    GetObjNameFunc.argtypes = (ctypes.c_int, ctypes.c_char_p)

    global GetHighLightedObjFunc
    GetHighLightedObjFunc = TestDLL['GetHighLightedObj']
    GetHighLightedObjFunc.restype = ctypes.c_int

    global GetObjectParamFunc
    GetObjectParamFunc = TestDLL['GetObjectParam']
    GetObjectParamFunc.argtypes = (ctypes.c_int, ctypes.c_void_p)
    GetObjectParamFunc.restype = ctypes.c_int

    global GetGlobalPositionAttitudeFunc
    GetGlobalPositionAttitudeFunc = TestDLL['GetGlobalPositionAttitude']
    GetGlobalPositionAttitudeFunc.argtypes = (ctypes.c_void_p,)

    global ReturnDistanceFunc
    ReturnDistanceFunc = TestDLL['ReturnDistance']
    ReturnDistanceFunc.argtypes = (
    ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,)
    ReturnDistanceFunc.restype = ctypes.c_double

    global ReturnBrightnessFunc
    ReturnBrightnessFunc = TestDLL['ReturnBrightness']
    ReturnBrightnessFunc.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,)
    ReturnBrightnessFunc.restype = ctypes.c_double

    global Convert3DtoPixelFunc
    Convert3DtoPixelFunc = TestDLL['Convert3DtoPixel']
    Convert3DtoPixelFunc.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_void_p,)

    global Pixelto3DFunc
    Pixelto3DFunc = TestDLL['Pixelto3D']
    Pixelto3DFunc.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_void_p,)

    global GetVisibleFacetPntFunc
    GetVisibleFacetPntFunc = TestDLL['GetVisibleFacetPnt']
    GetVisibleFacetPntFunc.argtypes = (
    ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
    GetVisibleFacetPntFunc.restype = ctypes.c_int

    global LoadBinDepthMapPntFunc
    LoadBinDepthMapPntFunc = TestDLL['LoadBinDepthMap']
    LoadBinDepthMapPntFunc.argtypes = (
    ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_void_p, ctypes.c_void_p)
    LoadBinDepthMapPntFunc.restype = ctypes.c_int

    global MeshUpDepthMapFunc
    MeshUpDepthMapFunc = TestDLL['MeshUpDepthMap']
    MeshUpDepthMapFunc.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    MeshUpDepthMapFunc.restype = ctypes.c_int

    global TexureOverayFunc
    TexureOverayFunc = TestDLL['TexureOveray']
    TexureOverayFunc.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
    TexureOverayFunc.restype = ctypes.c_int

    global TextureInterpolationFunc
    TextureInterpolationFunc = TestDLL['TextureInterpolation']
    TextureInterpolationFunc.argtypes = (ctypes.c_int,)

    global getTextureImgFunc
    getTextureImgFunc = TestDLL['getTextureImg']
    getTextureImgFunc.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,)
    getTextureImgFunc.restype = ctypes.c_int

    global SetFacetVertexFunc
    SetFacetVertexFunc = TestDLL['SetFacetVertex']
    SetFacetVertexFunc.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)

    global InitializeRenderFacetFunc
    InitializeRenderFacetFunc = TestDLL['InitializeRenderFacet']
    InitializeRenderFacetFunc.argtypes = (ctypes.c_int, ctypes.c_int)

    global setModelPosRotFunc
    setModelPosRotFunc = TestDLL['setModelPosRot']
    setModelPosRotFunc.argtypes = (
    ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)

    global getModelListFunc
    getModelListFunc = TestDLL['getModelList']
    getModelListFunc.argtypes = (ctypes.c_int, ctypes.c_void_p)

    global getModelIDByObjIDFunc
    getModelIDByObjIDFunc = TestDLL['getModelIDByObjID']
    getModelIDByObjIDFunc.argtypes = (ctypes.c_int, )
    getModelIDByObjIDFunc.restype = ctypes.c_int

    global getModelPosRotFunc
    getModelPosRotFunc = TestDLL['getModelPosRot']
    getModelPosRotFunc.argtypes = (ctypes.c_int, ctypes.c_void_p,)
    getModelPosRotFunc.restype = ctypes.c_int

    global getLocalFrameFunc
    getLocalFrameFunc = TestDLL['getLocalFrame']
    getLocalFrameFunc.argtypes = (ctypes.c_int, ctypes.c_void_p)

    global setTextureDataFunc
    setTextureDataFunc = TestDLL['setTextureData']
    setTextureDataFunc.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_int)

    global GetAnalysisFacetFunc
    GetAnalysisFacetFunc = TestDLL['GetAnalysisFacet']
    GetAnalysisFacetFunc.argtypes = (ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    GetAnalysisFacetFunc.restype = ctypes.c_int

    global SetAFacetColorFunc
    SetAFacetColorFunc = TestDLL['SetAFacetColor']
    SetAFacetColorFunc.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float)
    SetAFacetColorFunc.restype = ctypes.c_int


def SetAFacetColor(p1, p2, p3, p4, p5):
    return SetAFacetColorFunc(p1, p2, p3, p4, p5)


def setTextureData(TextureID, TextureData, TextureSize):
    return setTextureDataFunc(TextureID, TextureData.ctypes, TextureSize)


def getLocalFrame(ModelID):
    Buffer = np.zeros(12, np.float32)
    getLocalFrameFunc(ModelID, Buffer.ctypes)

    frame = []
    frame.append(np.array([Buffer[0], Buffer[1], Buffer[2]]))
    frame.append(np.array([Buffer[3], Buffer[4], Buffer[5]]))
    frame.append(np.array([Buffer[6], Buffer[7], Buffer[8]]))
    frame.append(np.array([Buffer[9], Buffer[10], Buffer[11]]))

    return frame

def getModelIDByObjID(ObjID):
    return getModelIDByObjIDFunc(ObjID)

def getModelPosRot(ModelID):
    Buffer = np.zeros(6, np.float32)
    res = getModelPosRotFunc(ModelID, Buffer.ctypes)
    return res, Buffer

def getModelList(MaxModel):
    Buffer = np.zeros(MaxModel * 64, np.uint8)
    len = getModelListFunc(MaxModel, Buffer.ctypes)

    # print(modelList.astype(np.byte))

    tempList = []
    maxModelNameLen = 64
    for i in range(len):
        for k in range(maxModelNameLen):
            if Buffer[i * maxModelNameLen + k] == 0:
                # print()
                tempList.append("".join(map(chr, Buffer[i * maxModelNameLen:i * maxModelNameLen + k])))
                break

    return len, tempList


def setModelPosRot(p1, p2, p3, p4, p5, p6, p7):
    setModelPosRotFunc(p1, p2, p3, p4, p5, p6, p7)


def InitializeRenderFacet(p1, p2):
    InitializeRenderFacetFunc(p1, p2)


def SetFacetVertex(p1, p2, p3, p4):
    VertexNum = p3
    Vertex = np.zeros(VertexNum * 3, np.float32)
    v = 0
    for i in range(VertexNum):
        Vertex[v] = p4[i][0]
        v += 1
        Vertex[v] = p4[i][1]
        v += 1
        Vertex[v] = p4[i][2]
        v += 1
    SetFacetVertexFunc(p1, p2, p3, Vertex.ctypes)


def ObjMeshUp(p1, p2, p3, p4):
    return MeshUpDepthMapFunc(p1, p2, p3, p4)

def TexureOveray(p1, p2, p3, p4, p5, p6):
    return TexureOverayFunc(p1, p2, p3, p4, p5, p6)

def TextureInterpolation(p1):
    return TextureInterpolationFunc(p1)

def getTextureImg(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    return getTextureImgFunc(p1, p2, p3, p4, p5, p6, p7, p8, p9)

def LoadBinDepthMapPnt(p1, p2, p3, p4, p5, p6, p7):
    filename = ctypes.c_char_p()
    filename.value = p1.encode('utf-8')
    return LoadBinDepthMapPntFunc(filename, p2, p3, p4, p5, p6, p7)


def GetVisibleFacetPnt(p1, p2):
    VertexNum = np.zeros(102400, np.int32)
    ID = np.zeros(102400, np.int32)
    AID = np.zeros(102400, np.int32)
    Vertex = np.zeros(102400 * 3, np.float32)
    FacetNum = GetVisibleFacetPntFunc(p1, p2, VertexNum.ctypes, ID.ctypes, AID.ctypes, Vertex.ctypes)

    return FacetNum, ID, AID, VertexNum, Vertex


def Convert3DtoPixel(p1, p2, p3):  # input(3D pos x,y,z) output(pixel posX, Y)
    objparam = np.zeros(2, np.int32)
    Convert3DtoPixelFunc(p1, p2, p3, objparam.ctypes)
    return objparam[0], objparam[1]


def Pixelto3D(p1, p2, p3):  # input(pixel posX, Y, depth) output(3D pos x,y,z)
    p1 = int(p1)
    p2 = int(p2)
    p3 = int(p3)

    objparam = np.zeros(3, np.float32)
    Pixelto3DFunc(p1, p2, p3, objparam.ctypes)
    return objparam[0], objparam[1], objparam[2]


def GetColorImage(p1, p2, p3):
    GetColorImageFunc(p1, p2, p3)


def GetDepthMap(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10=-1):
    t0 = time.monotonic()
    GetDepthMapFunc(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
    t1 = time.monotonic() - t0
    if ShowText:
        print("Time GetDepthMap elapsed: ", t1)


def GetColorImageNoShade(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    t0 = time.monotonic()
    GetColorImageNoShadeFunc(p1, p2, p3, p4, p5, p6, p7, p8, p9)
    t1 = time.monotonic() - t0
    if ShowText:
        print("Time GetDepthMap elapsed: ", t1)


def GetShadeImage(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10=-1):
    t0 = time.monotonic()
    GetShadeImageFunc(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
    t1 = time.monotonic() - t0
    if ShowText:
        print("Time GetShadeImage elapsed: ", t1)


def SetObject(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14):
    SetObjectFunc(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14)


def GetBoundBox(p1):
    return GetBoundBoxFunc(p1)


def GetBoundBoxbyID(ID):
    MaxBoundBoxNum = 128
    BoundBox = np.zeros(MaxBoundBoxNum * 4, np.int32)
    BoundBoxNum = GetBoundBox(BoundBox.ctypes)

    x1 = BoundBox[4 * ID + 0]
    y1 = BoundBox[4 * ID + 1]
    x2 = BoundBox[4 * ID + 2]
    y2 = BoundBox[4 * ID + 3]

    return x1, y1, x2, y2


def SetGlobalPosition(p1, p2, p3):
    SetGlobalPositionFunc(p1, p2, p3)


def SetGlobalAttitude(p1, p2, p3):
    SetGlobalAttitudeFunc(p1, p2, p3)


def GetSeableObjMask(p1):
    return GetSeableObjMaskFunc(p1)


def SetObjectType(p1, p2):
    SetObjectTypeFunc(p1, p2)


def SetObjAtt(p1, p2, p3, p4):
    SetObjAttFunc(p1, p2, p3, p4)


def SetObjPos(p1, p2, p3, p4):
    SetObjPosFunc(p1, p2, p3, p4)


def SetObjAmp(p1, p2, p3, p4):
    SetObjAmpFunc(p1, p2, p3, p4)


def SetObjClr(p1, p2, p3, p4):
    SetObjClrFunc(p1, p2, p3, p4)

def SetObjName(p1, p2):
    p2Temp = ctypes.c_char_p()
    p2Temp.value = p2.encode('utf-8')
    SetObjNameFunc(p1, p2Temp)

def GetObjName(p1):
    p2 = ctypes.create_string_buffer(64)
    GetObjNameFunc(p1, p2)
    return str(p2.value.decode('utf-8'))

def GetHighLightedObj():
    return GetHighLightedObjFunc()


def GetObjectParam(p1, p2):
    return GetObjectParamFunc(p1, p2)


def GetObjType(p1):
    objparam = np.zeros(13, np.float32)
    GetObjectParam(p1, objparam.ctypes)
    return int(objparam[0])


def GetObjAtt(p1):
    objparam = np.zeros(13, np.float32)
    GetObjectParam(p1, objparam.ctypes)
    return objparam[1], objparam[2], objparam[3]


def GetObjClr(p1):
    objparam = np.zeros(13, np.float32)
    GetObjectParam(p1, objparam.ctypes)
    return objparam[4], objparam[5], objparam[6]


def GetObjAmp(p1):
    objparam = np.zeros(13, np.float32)
    GetObjectParam(p1, objparam.ctypes)
    return objparam[7], objparam[8], objparam[9]


def GetObjPos(p1):
    objparam = np.zeros(13, np.float32)
    GetObjectParam(p1, objparam.ctypes)
    return objparam[10], objparam[11], objparam[12]


def GetGlobalPositionAttitude(p1):
    GetGlobalPositionAttitudeFunc(p1)


def GetGlobalPos():
    p1 = np.zeros(6, np.float32)
    GetGlobalPositionAttitudeFunc(p1.ctypes)
    return p1[0], p1[1], p1[2]


def GetGlobalAtt():
    p1 = np.zeros(6, np.float32)
    GetGlobalPositionAttitudeFunc(p1.ctypes)
    return p1[3], p1[4], p1[5]


def ReturnDistance(PosX, PosY, Initalize=True):
    p1 = np.zeros(1, np.int32)
    p2 = np.zeros(1, np.int32)

    if Initalize == False:
        p1[0] = -1
        p2[0] = -1

    p3 = np.zeros(1, np.int32)
    p4 = np.zeros(1, np.float32)
    p5 = np.zeros(1, np.float32)
    range = ReturnDistanceFunc(int(PosX), int(PosY), p1.ctypes, p2.ctypes, p3.ctypes, p4.ctypes, p5.ctypes)
    return range, p1[0], p2[0], p3[0], p4[0], p5[0]


def ModelReinit():
    ReturnDistance(0, 0)


def ReturnBrightness(PosX, PosY):
    p1 = np.zeros(1, np.int32)
    p2 = np.zeros(1, np.int32)
    Brightness = ReturnBrightnessFunc(int(PosX), int(PosY), p1.ctypes, p2.ctypes)
    return Brightness, p1[0], p2[0]


class cFacet:
    def __init__(self):
        self.Vertex = []
        self.Pixel = []
        self.FacetID = 0


def GetAnalysisFacet(ID):
    Vertex = np.zeros(12, np.float32)
    Normal = np.zeros(3, np.float32)
    VertexNum = GetAnalysisFacetFunc(ID, Vertex.ctypes, Normal.ctypes)
    return VertexNum, Vertex, Normal


def RetrunVisibleFacet(ID):
    Result = []
    v = 0
    FacetNum, FacetID, VertexNum, Vertex = GetVisibleFacetPnt(ID, 1)
    for f in range(FacetNum):
        Facet = cFacet()
        Facet.FacetID = FacetID[f]

        for k in range(VertexNum[f]):
            Facet.Vertex.append([Vertex[3 * v + 0], Vertex[3 * v + 1], Vertex[3 * v + 2]])
            px, py = Convert3DtoPixel(Vertex[3 * v + 0], Vertex[3 * v + 1], Vertex[3 * v + 2])
            Facet.Pixel.append([px, py])
            v += 1

        Result.append(Facet)
    return Result


def RetrunAllFacet(ID):
    Result = []
    v = 0
    FacetNum, FacetID, VertexNum, Vertex = GetVisibleFacetPnt(ID, 0)
    for f in range(FacetNum):
        Facet = cFacet()
        Facet.FacetID = FacetID[f]

        for k in range(VertexNum[f]):
            Facet.Vertex.append([Vertex[3 * v + 0], Vertex[3 * v + 1], Vertex[3 * v + 2]])
            px, py = Convert3DtoPixel(Vertex[3 * v + 0], Vertex[3 * v + 1], Vertex[3 * v + 2])
            Facet.Pixel.append([px, py])
            v += 1

        Result.append(Facet)

    return Result