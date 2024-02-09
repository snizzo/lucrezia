#version 150

// Vertex shader
in vec4 p3d_Vertex;
out vec2 texcoord;

uniform mat4 p3d_ModelViewProjectionMatrix;

void main() {
  // Transform the vertex position by the model-view-projection matrix
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  // Pass the texture coordinate to the fragment shader
  texcoord = p3d_Vertex.xy * 0.5 + 0.5;
}

// Fragment shader
in vec2 texcoord;
out vec4 fragColor;

uniform sampler2D tex;

void main() {
  // Sample the original scene color
  vec4 color = texture(tex, texcoord);
  // Apply some bloom effect by brightening and blurring the color
  color += texture(tex, texcoord + vec2(0.001, 0.001)) * 0.5;
  color += texture(tex, texcoord + vec2(-0.001, -0.001)) * 0.5;
  color += texture(tex, texcoord + vec2(0.001, -0.001)) * 0.5;
  color += texture(tex, texcoord + vec2(-0.001, 0.001)) * 0.5;
  // Set the fragment color to the bloomed color
  fragColor = color;
}