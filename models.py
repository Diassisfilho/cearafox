import glfw
import glm
import numpy as np
from OpenGL.GL import *
from PIL import Image

from utils import setup_vao_vbo

class Model:
    def __init__(self, shader_program, vao, indices, material_faces, materials, textures):
        self.shader_program = shader_program
        self.vao = vao
        self.indices = indices
        self.material_faces = material_faces
        self.materials = materials
        self.textures = textures
        self.model = glm.mat4(1.0)

    def draw_model(self):
        glUseProgram(self.shader_program)

        # Set model matrix
        model_loc = glGetUniformLocation(self.shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(self.model))

        # Bind VAO
        glBindVertexArray(self.vao)

        # Draw each face with the corresponding material and texture
        start_index = 0
        for material_name in self.materials:
            if 'texture' in self.materials[material_name]:
                texture_id = self.textures[material_name]
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                glUniform1i(glGetUniformLocation(self.shader_program, "texture1"), 0)

            # Find the range of indices for the current material
            material_indices = [i for i, m in enumerate(self.material_faces) if m == material_name]
            if material_indices:
                for i in range(len(material_indices)):
                    start_index = material_indices[i] * 3
                    end_index = start_index + 3
                    glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, ctypes.c_void_p(start_index * 4))

        glBindVertexArray(0)

        # Unbind texture
        glBindTexture(GL_TEXTURE_2D, 0)

def load_obj(filename):
    vertices = []
    texcoords = []
    normals = []
    faces = []
    material_faces = []

    current_material = None

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vt '):
                texcoords.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('usemtl '):
                current_material = line.strip().split()[1]
            elif line.startswith('f '):
                face = []
                for vertex in line.strip().split()[1:]:
                    face.append(list(map(int, vertex.split('/'))))
                faces.append(face)
                material_faces.append(current_material)

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

    obj_data = {
        'vertex_data': np.array(vertex_data, dtype=np.float32),
        'texcoord_data': np.array(texcoord_data, dtype=np.float32),
        'normal_data': np.array(normal_data, dtype=np.float32),
        'indices': np.array(indices, dtype=np.uint32),
        'material_faces': material_faces
    }

    return obj_data

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

def setup_model(shader_program, obj_path, mtl_path):
    model_obj_data = load_obj(obj_path)

    model_materials = load_mtl(mtl_path)

    model_textures = {}
    for material_name, material in model_materials.items():
        print(f"Loading texture for material: {material_name}")
        model_textures[material_name] = load_texture(material['texture'])

    print("Loaded textures:", model_textures)

    model_vao = setup_vao_vbo(
        model_obj_data['vertex_data'],
        model_obj_data['texcoord_data'],
        model_obj_data['normal_data'],
        model_obj_data['indices']
    )

    # Use the correct material name from the MTL file
    return Model(
        shader_program,
        model_vao,
        model_obj_data['indices'],
        model_obj_data['material_faces'],
        model_materials,
        model_textures
    )

def rotate_instance_by_time(instance):
    rotation_angle = glfw.get_time() * glm.radians(45)  # Rotate 45 degrees per second
    instance.model = glm.rotate(glm.mat4(1.0), rotation_angle, glm.vec3(0, 1, 0))