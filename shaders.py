from OpenGL.GL import *

# Function to read shader source from file
def read_shader_source(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
# Compile shaders and create shader program
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    # Check for compilation errors
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compilation failed: {error}")
    
    return shader

def shaders_setup(vertex_shader_path, fragment_shader_path) -> None:
    # Read shaders from files
    vertex_shader_source = read_shader_source(vertex_shader_path)
    fragment_shader_source = read_shader_source(fragment_shader_path)

    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    
    # Check for linking errors
    result = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if not result:
        error = glGetProgramInfoLog(shader_program).decode()
        raise RuntimeError(f"Program linking failed: {error}")
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return shader_program