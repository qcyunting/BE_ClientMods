// __multiversion__
// This signals the loading code to prepend either #version 100 or #version 300 es as apropriate.
precision highp float;
#include "vertexVersionCentroidUV.h"

#include "uniformWorldConstants.h"
#include "uniformPerFrameConstants.h"
#include "uniformShaderConstants.h"
attribute POS4 POSITION;
attribute vec2 TEXCOORD_0;
varying vec4 color;
varying highp vec3 lusor;
varying highp vec3 chunk;
varying highp vec3 ReshaderPos;
out vec3 position;
out float no;
out float ta;
out float ll;
void main()
{
    uv = TEXCOORD_0;
    //
    lusor=POSITION.xyz;
    chunk=POSITION.xyz;
    //lusor.y-=0.256;
    ReshaderPos.x=POSITION.x;
    ReshaderPos.y=POSITION.y;
    ReshaderPos.z=-POSITION.z;
    ll=smoothstep(1.0,0.0,(FOG_CONTROL.x)/((FOG_CONTROL.y+0.3)-FOG_CONTROL.x));
    no=pow(max(min(1.-FOG_COLOR.r*1.5,1.),0.),1.2);
    ta=pow(max(min(1.-FOG_COLOR.b*1.2,1.),0.),.5);
    
    gl_Position = WORLDVIEWPROJ * POSITION;
    position = POSITION.xyz;
}
/*
varying highp vec3 Pos;
mat2 rotate2d(float angle){
return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
}

vec4 apos = POSITION;
apos.y += 0.128;
Pos =(WORLD * apos).xyz;
apos.xz*=rotate2d(SUN_DIR.y);
gl_Position = WORLDVIEWPROJ * apos;
*/