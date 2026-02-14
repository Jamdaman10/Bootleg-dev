#version 430
#define screenSize 2
#define speed 1.0
#define sensorDistance 10.0
#define sensorAngle 45.0
#define turnSpeed 1.0
layout (local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
layout (rgba32f, binding = 0) uniform image2D textureToSet;
layout(std430, binding = 1) buffer inputBuffer {
    vec4 inputData[];
};
layout(std430, binding = 2) buffer outputBuffer {
    vec4 outputData[];
};
float hash(vec2 co){
  return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}
float getDensity(float x, float y, float a){
    vec2 scannedPos = vec2(x + (cos(a) * sensorDistance), y + (sin(a) * sensorDistance));
    float density = 0.0;

    density += imageLoad(textureToSet, ivec2(scannedPos)).x;
    return density;

}
void main() {
    uint pos = gl_GlobalInvocationID.x;
    vec4 data = inputData[pos];
    data.x += cos(data.z * 360.0)*speed;
    data.y += sin(data.z * 360.0)*speed;
    float left = getDensity(data.x, data.y, (data.z * 360) - sensorAngle);
    float right = getDensity(data.x, data.y, (data.z * 360) + sensorAngle);
    float forward = getDensity(data.x, data.y, (data.z * 360));

    if (left > right && left > forward){
        data.z -= (turnSpeed) / 360.0;
    }
    else if(right > left && right > forward){
        data.z += turnSpeed / 360.0;
    }
    if(data.y > screenSize * 600.0 || data.y < 0.0){
        data.z = 0.0 - data.z;
    }
    if(data.x > screenSize * 800.0 || data.x < 0.0){
        data.z = 180 - data.z;
    }

    outputData[pos] = data;
    imageStore(textureToSet, ivec2(data.xy), vec4(1.0, 1.0, 1.0, 1.0));
}
