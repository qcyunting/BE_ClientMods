// __multiversion__
// This signals the loading code to prepend either #version 100 or #version 300 es as apropriate.
precision highp float;
#include "vertexVersionCentroidUV.h"
#include "uniformWorldConstants.h"
#include "uniformPerFrameConstants.h"
#include "uniformShaderConstants.h"
attribute POS4 POSITION;
attribute vec2 TEXCOORD_0;
uniform vec4 SUN_DIR;
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
    vec3 solPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    uv = TEXCOORD_0;
    lusor=POSITION.xyz;
    //lusor.y-=0.128;//将立方体天空盒的坐标系修正为球形
    chunk=POSITION.xyz;
    //用于reflectmap的坐标
    ReshaderPos.x=POSITION.x;
    ReshaderPos.y=POSITION.y;
    ReshaderPos.z=-POSITION.z;
    ta = smoothstep(1.0,0.0,solPos.y*2.0);
    no = smoothstep(0.0,1.0,-solPos.y*2.0);
    ll=smoothstep(1.0,0.0,(FOG_CONTROL.x)/((FOG_CONTROL.y+0.3)-FOG_CONTROL.x));
    //no=pow(max(min(1.-FOG_COLOR.r*1.5,1.),0.),1.2);
    //ta=pow(max(min(1.-FOG_COLOR.b*1.5,1.),0.),.5);
    
    gl_Position = WORLDVIEWPROJ * vec4(POSITION.x,POSITION.y+0.128,POSITION.z,POSITION.w);
    position = POSITION.xyz;
}