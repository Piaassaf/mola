#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

__code=""

'''display variables'''
__showAxis=True
__showEdges=False
__edgesWidth=1.0
__showWireframe=False
__showPointsCloud=False
__showPointsNumbers=False
__backgroundColor = (0,0,0)
__pointColor = (1,1,1)
__pointSize = 10
__canvasWidth = "100%"
__canvasHeight = "56.25vw"

def displayMesh(mesh,canvasWidth=None,canvasHeight=None,showAxis=True,showEdges=False,edgesWidth=1.0,showWireframe=False,showPointsCloud=False,showPointsNumbers=False,backgroundColor=(0,0,0),pointColor=(1,1,1),pointSize=10):
  """
  Displays Mesh.
  Arguments:
  ----------
  mesh : mola.core.Mesh
         The mesh to be displayed
  ----------
  Optional Arguments:
  ----------
  canvasWidth : float
  canvasHeight : float
  showAxis : Boolean
  showEdges : Boolean
  showWireframe : Boolean
  showPointsCloud : Boolean
  showPointsNumbers : Boolean
  edgesWidth : float
  backgroundColor : tuple (r,g,b)
                    r,g,b values, 0.0 to 1.0
  pointColor : tuple (r,g,b)
                r,g,b values, 0.0 to 1.0
  pointSize : float
  """
  global __canvasWidth, __canvasHeight, __showAxis,__showEdges,__edgesWidth,__showWireframe,__showPointsCloud,__showPointsNumbers,__backgroundColor,__pointColor,__pointSize
  if(canvasWidth):
    __canvasWidth = str(canvasWidth) + "px"
  if(canvasHeight):
    __canvasHeight = str(canvasHeight) + "px"
  __showAxis=showAxis
  __showEdges=showEdges
  __edgesWidth=edgesWidth
  __showWireframe=showWireframe
  __showPointsCloud = showPointsCloud
  __showPointsNumbers = showPointsNumbers
  __backgroundColor = backgroundColor
  __pointColor = pointColor
  __pointSize = pointSize

  if(showPointsNumbers):
    return __displayMeshAsNumbers(mesh)
  else:
    return display(mesh.faces)

def __displayMeshAsNumbers(mesh):
    __begin3D()
    positions=[]
    indices=[]
    colors=[]

    for v in mesh.vertices:
        positions.extend((v.x,v.y,v.z))

    for face in mesh.faces:
        if len(face.vertices)==3:
            v0 = face.vertices[0]
            v1 = face.vertices[1]
            v2 = face.vertices[2]
            indices.extend([__getVertexIndex(v0,positions),__getVertexIndex(v1,positions),__getVertexIndex(v2,positions)])
        if len(face.vertices)==4:
            v0 = face.vertices[0]
            v1 = face.vertices[1]
            v2 = face.vertices[2]
            v3 = face.vertices[3]
            indices.extend([__getVertexIndex(v0,positions),__getVertexIndex(v1,positions),__getVertexIndex(v2,positions)])
            indices.extend([__getVertexIndex(v2,positions),__getVertexIndex(v3,positions),__getVertexIndex(v0,positions)])
    __drawMeshWithColors(positions,indices,colors)
    __end3D()
    return __code

def __getVertexIndex(v,positions):
    for i in range(0,len(positions),3):
        xPos = positions[i]
        yPos = positions[i+1]
        zPos = positions[i+2]
        if(v.x==xPos and v.y==yPos and v.z==zPos):
            return i
    return 0

def display(faces):
    __begin3D()
    positions=[]
    indices=[]
    colors=[]
    cIndex=0
    for face in faces:
        for v in face.vertices:
            positions.extend((v.x,v.y,v.z))
            colors.extend(face.color)
        indices.extend([cIndex,cIndex+1,cIndex+2])
        if len(face.vertices)==4:
            indices.extend([cIndex+2,cIndex+3,cIndex])
        cIndex+=len(face.vertices)
    __drawMeshWithColors(positions,indices,colors)
    __end3D()
    return __code

def __begin3D():
    global __code
    __code=""
    __code+='''<canvas id="renderCanvas" touch-action="none"></canvas>
        <script src="https://cdn.babylonjs.com/babylon.js"></script>
        <style>
            html, body {
                overflow: hidden;
                width:''' + __canvasWidth + ''';
                height: ''' + __canvasHeight + ''';
                margin: 0;
                padding: 0;
            }
            #renderCanvas {
                width:''' + __canvasWidth + ''';
                height: ''' + __canvasHeight + ''';
                touch-action: none;
            }
        </style>
        <script>
      var canvas = document.getElementById("renderCanvas");'''
    __code+='''var createScene = function () {var scene = new BABYLON.Scene(engine);'''
    __code+='''scene.clearColor = new BABYLON.Color3'''+str(__backgroundColor)+ ";"
    __code+='''var light = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(1, 1, 1), scene);var light2 = new BABYLON.DirectionalLight("direct", new BABYLON.Vector3(-1, -1, -1), scene);'''
    __code+='''var camera = new BABYLON.ArcRotateCamera("camera1",  0, 0, 0, new BABYLON.Vector3(0, 0, 0), scene);
            camera.setPosition(new BABYLON.Vector3(0, 5, -30));
             camera.attachControl(canvas, true);'''
    __code+=''' var light = new BABYLON.HemisphericLight("light1", new BABYLON.Vector3(0, 1, 0), scene); // Default intensity is 1. Let's dim the light a small amount
    light.intensity = 0.5;'''


def __drawMeshWithColors(vertices,faces,vertexColors):
    global __code
    __code+="var positions = "+str(vertices)+";"
    __code+="var indices = "+str(faces)+";"
    __code+="var colors = "+str(vertexColors)+";"
    return __code

def __drawTestMesh():
    global __code
    __code+='''    var positions = [-5, 2, -3, -7, -2, -3, -3, -2, -3, 5, 2, 3, 7, -2, 3, 3, -2, 3];
            var indices = [0, 1, 2, 3, 4, 5];    '''

def __end3D():
  global __code
  __code+= '''
        //Create a custom mesh
          var customMesh = new BABYLON.Mesh("custom", scene);
        //Empty array to contain calculated values
          var normals = [];
          var vertexData = new BABYLON.VertexData();
          BABYLON.VertexData.ComputeNormals(positions, indices, normals);
          //Assign positions, indices and normals to vertexData
          vertexData.positions = positions;
          vertexData.indices = indices;
          vertexData.normals = normals;
          vertexData.colors = colors;
          //Apply vertexData to custom mesh
          vertexData.applyToMesh(customMesh);
          /******Display custom mesh in wireframe view to show its creation****************/
          var mat = new BABYLON.StandardMaterial("mat", scene);
          mat.backFaceCulling = false;'''
  if __showWireframe:
    __code+='''mat.wireframe=true;'''
  if __showPointsCloud:
    __code+='''mat.pointsCloud=true;'''
    __code+='''mat.pointSize=''' + str(__pointSize) + ';'
  if __showEdges:
    __code+= '''customMesh.enableEdgesRendering();'''
    __code+= '''customMesh.edgesWidth = ''' + str(__edgesWidth)+';'
  __code+='''
        /*******************************************************************************/
        var makeTextPlane = function(text, color, size) {
            var dynamicTexture = new BABYLON.DynamicTexture("DynamicTexture", 50, scene, true);
            dynamicTexture.hasAlpha = true;
            dynamicTexture.drawText(text, 5, 40, "bold 36px Arial", color , "transparent", true);
            var plane = new BABYLON.Mesh.CreatePlane("TextPlane", size, scene, true);
            plane.material = new BABYLON.StandardMaterial("TextPlaneMaterial", scene);
            plane.material.backFaceCulling = false;
            plane.material.specularColor = new BABYLON.Color3(0, 0, 0);
            plane.material.diffuseTexture = dynamicTexture;
            return plane;
        };'''
  if __showPointsNumbers:
    __code+='''
    var drawNumber = function(scene, text, positionVector){
    //data reporter
    var outputplane = BABYLON.Mesh.CreatePlane("outputplane", 1.5, scene, false);
    outputplane.billboardMode = BABYLON.AbstractMesh.BILLBOARDMODE_ALL;
    outputplane.material = new BABYLON.StandardMaterial("outputplane", scene);
    outputplane.position = positionVector;
    outputplane.scaling.x = 1;
    outputplane.scaling.y = 1;
    var outputplaneTexture = new BABYLON.DynamicTexture("dynamic texture", 512, scene, true);
    outputplane.material.diffuseTexture = outputplaneTexture;
    outputplane.material.emissiveColor = new BABYLON.Color3'''+str(__pointColor)+ ''';
    outputplane.material.backFaceCulling = false;
    //outputplaneTexture.getContext().clearRect(0, 140, 512, 512);
    var textColor = new BABYLON.Color3''' + str(__pointColor) + '''.toHexString();
    outputplaneTexture.drawText(text, null, 300, "200px arial", textColor);
    outputplaneTexture.hasAlpha = true;
    };'''
    __code+=   '''
    var vPositions = customMesh.getVerticesData(BABYLON.VertexBuffer.PositionKind);
    var ind = 0;
    for(var i=0;i<vPositions.length;i+=3){
        var posX = (vPositions[i]);
        var posY = (vPositions[i+1]);
        var posZ = (vPositions[i+2]);
        drawNumber(scene,ind.toString(),new BABYLON.Vector3(posX,posY+1,posZ));
        ind++;
    }'''
  if __showAxis:
    __code+='''// show axis
            var showAxis = function(size) {
              var axisX = BABYLON.Mesh.CreateLines("axisX", [
                    new BABYLON.Vector3.Zero(), new BABYLON.Vector3(size, 0, 0), new BABYLON.Vector3(size * 0.95, 0.05 * size, 0),
                    new BABYLON.Vector3(size, 0, 0), new BABYLON.Vector3(size * 0.95, -0.05 * size, 0)
                ], scene);
              axisX.color = new BABYLON.Color3(1, 0, 0);
              var xChar = makeTextPlane("X", "red", size / 10);
              xChar.position = new BABYLON.Vector3(0.9 * size, -0.05 * size, 0);
              var axisY = BABYLON.Mesh.CreateLines("axisY", [
                  new BABYLON.Vector3.Zero(), new BABYLON.Vector3(0, size, 0), new BABYLON.Vector3( -0.05 * size, size * 0.95, 0),
                  new BABYLON.Vector3(0, size, 0), new BABYLON.Vector3( 0.05 * size, size * 0.95, 0)
              ], scene);
              axisY.color = new BABYLON.Color3(0, 1, 0);
              var yChar = makeTextPlane("Y", "green", size / 10);
              yChar.position = new BABYLON.Vector3(0, 0.9 * size, -0.05 * size);
              var axisZ = BABYLON.Mesh.CreateLines("axisZ", [
                  new BABYLON.Vector3.Zero(), new BABYLON.Vector3(0, 0, size), new BABYLON.Vector3( 0 , -0.05 * size, size * 0.95),
                  new BABYLON.Vector3(0, 0, size), new BABYLON.Vector3( 0, 0.05 * size, size * 0.95)
              ], scene);
              axisZ.color = new BABYLON.Color3(0, 0, 1);
              var zChar = makeTextPlane("Z", "blue", size / 10);
              zChar.position = new BABYLON.Vector3(0, 0.05 * size, 0.9 * size);
          };
          showAxis(10);'''
  __code+='''customMesh.material = mat;'''
  __code+='''return scene;
    };
      var engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
      var scene = createScene();
      engine.runRenderLoop(function () {
          if (scene) {scene.render();}
          });
      // Resize
      window.addEventListener("resize", function () {
          engine.resize();
      });
  </script>'''
