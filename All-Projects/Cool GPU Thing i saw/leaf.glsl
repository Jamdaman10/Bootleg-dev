#version 430
#define screenSize 2
layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
layout (rgba32f, binding = 0) uniform image2D textureToSet;
layout(std430, binding = 1) buffer inputBuffer {
    vec4 inputData[];
};
layout(std430, binding = 2) buffer outputBuffer {
    vec4 outputData[];
};
uniform float time;
float hash(vec2 co){
  return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    uint pos = gl_GlobalInvocationID.x;
    vec4 data = inputData[pos];

    if (data.z == 0.0){
        if (hash(data.xy * data.w + time) > 0.5){
            data.x += 5.0;
        }
        if (hash(data.xy * data.w * 12.3 + time) > 0.5){
            data.x -= 5.0;
        }
        if (hash(data.xy * data.w * 32.06 + time) > 0.5){
            data.y += 5.0;
        }
        if (hash(data.xy * data.w * 12.4 + time) > 0.5){
            data.y -= 5.0;
        }
        
        if (imageLoad(textureToSet, ivec2(data.xy + vec2(1.0, 0.0))).z == 1.0 || imageLoad(textureToSet, ivec2(data.xy + vec2(-1.0, 0.0))).z == 1.0 || imageLoad(textureToSet, ivec2(data.xy + vec2(0.0, 1.0))).z == 1.0 || imageLoad(textureToSet, ivec2(data.xy + vec2(0.0, -1.0))).z == 1.0){
            data.z = 1.0;
        }
    }
    //data.x = mod(data.x, 800.0 * screenSize);
    //data.y = mod(data.y, 600.0 * screenSize);

    outputData[pos] = data;
    imageStore(textureToSet, ivec2(data.xy), vec4(1.0,1.0,data.z, 1.0));
}
