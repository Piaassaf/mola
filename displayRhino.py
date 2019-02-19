import rhinoscriptsyntax as rs
def display(faces):
    vertices=[]
    facesIndices=[]
    vertexColors=[]
    for f in faces:
        faceIndices=[]
        for v in f.vertices:
            faceIndices.append(len(vertices))
            vertices.append(v)
        facesIndices.append(faceIndices)
        vertexColors.append((f.color[0]*255,f.color[1]*255,f.color[2]*255))
    rs.AddMesh(vertices,facesIndices,None,None,vertexColors)