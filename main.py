import glfw
from OpenGL.GL import *
import numpy as np
import glm
import math

from shaders import shaders_setup
from utils import setup_vao_vbo
from models import Model, load_obj, load_mtl, load_texture
from visualization import camera_setup, lighting_setup

# Initialize GLFW
if not glfw.init():
    exit()

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "CearaFox", None, None)
if not window:
    glfw.terminate()
    exit()
glfw.make_context_current(window)

shader_program = shaders_setup('vertex_shader.glsl', 'fragment_shader.glsl')

vertices, texcoords, normals, indices, material_faces = load_obj('arwing.obj')

materials = load_mtl('arwing.mtl')

textures = {}
for material_name, material in materials.items():
    print(f"Loading texture for material: {material_name}")
    textures[material_name] = load_texture(material['texture'])

print("Loaded textures:", textures)

arwing_vao = setup_vao_vbo(vertices, texcoords, normals, indices)

# Use the correct material name from the MTL file
arwing_instance = Model(shader_program, arwing_vao, indices, material_faces, materials, textures)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Render loop
while not glfw.window_should_close(window):
    # Clear screen
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Use shader program
    glUseProgram(shader_program)

    camera_setup(shader_program)
    lighting_setup(shader_program)

    # Calculate rotation angle based on time
    rotation_angle = glfw.get_time() * glm.radians(45)  # Rotate 45 degrees per second
    arwing_instance.model = glm.rotate(glm.mat4(1.0), rotation_angle, glm.vec3(0, 1, 0))
    # arwing_instance.model = glm.scale(arwing_instance.model, glm.vec3(0.05,0.05,0.05))

    # Draw Player
    arwing_instance.draw_model()

    # Swap buffers and poll events
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup resources
glDeleteVertexArrays(1, [arwing_vao])
glDeleteBuffers(1, [arwing_vao])
glDeleteProgram(shader_program)

# Terminate GLFW
glfw.terminate()