import numpy as np
from OpenGL.GL import *

def setup_vao_vbo(vertices, texcoords, normals, indices):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    tbo = glGenBuffers(1)
    nbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)

    # Vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Texture coordinate buffer
    glBindBuffer(GL_ARRAY_BUFFER, tbo)
    glBufferData(GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(2)

    # Normal buffer
    glBindBuffer(GL_ARRAY_BUFFER, nbo)
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)

    # Element buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao

def setup_vao_vbo_skybox():
    skybox_vertices = [
        # positions          
        -1.0,  1.0, -1.0,
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,

        -1.0, -1.0,  1.0,
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        -1.0, -1.0,  1.0,

         1.0, -1.0, -1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0, -1.0,
         1.0, -1.0, -1.0,

        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        -1.0,  1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0,

        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0
    ]

    skybox_vertices = np.array(skybox_vertices, dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, skybox_vertices.nbytes, skybox_vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * skybox_vertices.itemsize, ctypes.c_void_p(0))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao

gold_ring_positions = [
    (0.00, 6.00, -14.00),
    (-12.13, -10.68, 9.61),
    (-35.60, -10.04, -1.27),
    (-46.12, -9.34, -38.85),
    (-68.33, -7.83, -14.50),
    (-2.90, -11.90, -55.31),
    (-2.90, -11.90, -45.31),
    (28.38, -13.07, -57.73),
    (39.85, -9.39, -76.39),
    (43.15, -13.68, -40.28),
    (-53.22, 2.48, -70.81),
    (61.51, -11.87, 28.54),
    (0.45, 70.05, -79.15),
    ]

gold_ring_rotations = [
    (0.08, -0.49, 0.00),
    (0.01, 1.33, 0.00),
    (-0.014, 0.27, 0.00),
    (-0.014, 0.27, 0.00),
    (-0.014, 0.27, 0.00),
    (-0.07, 0.11, 0.00),
    (-0.07, 0.11, 0.00),
    (-0.07, -6.44, 0.00),
    (0.47, 4.71, 0.00),
    (-0.03, -1.93, 0.00),
    (-0.09, -1.43, 0.00),
    (0.03, -8.07, 0.00),
    (0.00, 1.58, 0.00)
    ]
