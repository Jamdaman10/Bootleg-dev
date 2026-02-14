#version 330 core
uniform sampler2D image;

out vec4 color;
in vec2 fragmentTexCoord;

void main() {
    vec2 uv = fragmentTexCoord;
    vec4 col = texture2D(image, uv);

    // Fake glow
    float glow = smoothstep(0.8, 1.0, length(col.rgb));
    col.rgb += glow * 0.2;

    color = col;
}
