import glfw
import glm
import numpy as np
from OpenGL.GL import *
from PIL import Image

class Model:
    def __init__(self, shader_program, vao, indices, texture_id=None):
        self.shader_program = shader_program
        self.vao = vao
        self.indices = indices
        self.texture_id = texture_id
        self.model = glm.mat4(1.0)

    def draw_model(self):
        glUseProgram(self.shader_program)

        # Set model matrix
        model_loc = glGetUniformLocation(self.shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(self.model))

        # Bind texture if available
        if self.texture_id:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glUniform1i(glGetUniformLocation(self.shader_program, "texture1"), 0)

        # Bind VAO and draw
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        # Unbind texture
        if self.texture_id:
            glBindTexture(GL_TEXTURE_2D, 0)

def load_obj(filename):
    vertices = []
    texcoords = []
    normals = []
    faces = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vt '):
                texcoords.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                face = []
                for vertex in line.strip().split()[1:]:
                    face.append(list(map(int, vertex.split('/'))))
                faces.append(face)

    vertex_data = []
    texcoord_data = []
    normal_data = []
    indices = []
    index = 0

    for face in faces:
        for vertex in face:
            vertex_index, texcoord_index, normal_index = vertex
            vertex_data.extend(vertices[vertex_index - 1])
            texcoord_data.extend(texcoords[texcoord_index - 1])
            normal_data.extend(normals[normal_index - 1])
            indices.append(index)
            index += 1

    return np.array(vertex_data, dtype=np.float32), np.array(texcoord_data, dtype=np.float32), np.array(normal_data, dtype=np.float32), np.array(indices, dtype=np.uint32)

def load_mtl(filename):
    materials = {}
    current_material = None

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('newmtl '):
                current_material = line.strip().split()[1]
                materials[current_material] = {}
            elif line.startswith('map_Kd '):
                materials[current_material]['texture'] = line.strip().split()[1]

    return materials

def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(image, dtype=np.uint8)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

def render_model(vertices, texcoords, normals, faces, materials):
    glEnable(GL_TEXTURE_2D)
    for face in faces:
        glBegin(GL_TRIANGLES)
        for vertex in face:
            if len(vertex) > 1 and vertex[1] > 0:
                glTexCoord2fv(texcoords[vertex[1] - 1])
            if len(vertex) > 2 and vertex[2] > 0:
                glNormal3fv(normals[vertex[2] - 1])
            glVertex3fv(vertices[vertex[0] - 1])
        glEnd()
    glDisable(GL_TEXTURE_2D)