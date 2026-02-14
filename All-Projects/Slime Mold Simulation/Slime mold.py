import pygame
import moderngl
import numpy as np

screenSize = 2
pygame.init()
width, height = round(800*screenSize), round(600*screenSize)
screen = pygame.display.set_mode((width/screenSize, height/screenSize), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("ModernGL + Pygame Shader Example")

ctx = moderngl.create_context()

particleCount = 1024 * 1024

outputTexture = ctx.texture((width, height), 4)
outputTexture.use(location=0)
randomNumbers = np.random.rand(particleCount * 16)
randomNumbers[::4] *= width
randomNumbers[1::4] *= height
inputData = ctx.buffer(randomNumbers.astype('f4').tobytes())
outputData = ctx.buffer(bytearray(particleCount * 16))
inputData.bind_to_storage_buffer(binding=1)
outputData.bind_to_storage_buffer(binding=2)

vertexShader = """
#version 330
in vec2 in_vert;
out vec2 fragCoord;
void main() {
    fragCoord = in_vert;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

fragmentShader = """
#version 330
in vec2 fragCoord;
uniform sampler2D drawImage;
out vec4 frag_color;
void main() {
    vec2 v = fragCoord;
    v /= 2.0;
    v += 0.5;
    frag_color = texture(drawImage, v);
}
"""

computeShaderText = open("compute.glsl").read()
computeShader = ctx.compute_shader(computeShaderText)

blurShaderText = open("holyMoly.glsl").read()
blurShader = ctx.compute_shader(blurShaderText)

prog = ctx.program(vertex_shader=vertexShader, fragment_shader=fragmentShader)
prog["drawImage"].value = 0

outputTexture.bind_to_image(0, True, True)
vertices = np.array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
     1.0,  1.0,
], dtype='f4')

vbo = ctx.buffer(vertices)
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.0, 0.0, 0.0)
    #outputTexture.write(np.zeros((width, height, 4), dtype='u1').tobytes())
    inputData.bind_to_storage_buffer(binding=1)
    outputData.bind_to_storage_buffer(binding=2)

    blurShader.run(width, height, 1)
    computeShader.run(particleCount, 1, 1)
    vao.render(moderngl.TRIANGLE_STRIP)
    inputData = outputData

    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
