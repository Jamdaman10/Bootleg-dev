#version 430
layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
layout (rgba32f, binding = 0) uniform image2D textureToSet;

void main() {
    ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
    vec4 oldImage = imageLoad(textureToSet, coord);

    oldImage += imageLoad(textureToSet, coord + ivec2(1, 0));
    oldImage += imageLoad(textureToSet, coord + ivec2(-1, 0));
    oldImage += imageLoad(textureToSet, coord + ivec2(0, 1));
    oldImage += imageLoad(textureToSet, coord + ivec2(0, -1));

    oldImage /= 5.0;
    imageStore(textureToSet, coord, oldImage - 0.01);
}