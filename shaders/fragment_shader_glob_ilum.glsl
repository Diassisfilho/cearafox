#version 330 core
in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

out vec4 FragColor;

uniform vec3 ambientColor;
uniform sampler2D texture1;

void main()
{
    vec3 ambient = ambientColor;
    vec4 textureColor = texture(texture1, TexCoord);
    FragColor = vec4(ambient, 1.0) * textureColor;
}