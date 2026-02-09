// __multiversion__
// This signals the loading code to prepend either #version 100 or #version 300 es as apropriate.
//本着色器作者@重生的老楚，作品《重生像素》中所含着色器程序并不开源，请勿盗用代码，尊重他人劳动成果！
//Et auctor est scadere est @重生的老楚. Quod scadere progressio continebat in opere "Repixel" non aperta. Non furantur in codice et respicit eventus aliorum.
#include "vertexVersionCentroid.h"
#if __VERSION__ >= 300
precision highp float;
	#ifndef BYPASS_PIXEL_SHADER
		_centroid out vec2 TexUV;
		_centroid out vec2 LuxUV;
	#endif
#else
	#ifndef BYPASS_PIXEL_SHADER
		varying vec2 TexUV;
		varying vec2 LuxUV;
	#endif
#endif

#ifndef BYPASS_PIXEL_SHADER
	varying vec4 color_repixel;
#endif
uniform vec4 SUN_DIR;
varying highp vec3 ReshaderPos;
varying highp vec3 chunk;
varying highp vec3 lusor;
uniform vec3 WORLD_PARAMETERS;
out float no;
out float ta;
out float ll;
out float expe;
#ifdef LOW_PRECISION
	varying vec4 niebulaC;
#endif

#include "uniformWorldConstants.h"
#include "uniformPerFrameConstants.h"
#include "uniformShaderConstants.h"
#include "uniformRenderChunkConstants.h"

attribute POS4 POSITION;
attribute vec4 COLOR;
attribute vec2 TEXCOORD_0;
attribute vec2 TEXCOORD_1;

const float rA = 1.0;
const float rB = 1.0;
const vec3 UNIT_Y = vec3(0,1,0);
const float DIST_DESATURATION = 56.0 / 255.0; //WARNING this value is also hardcoded in the water color, don'tchange



void main()
{
    vec3 solPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    ta = smoothstep(1.0,0.0,solPos.y*2.0);
    no = smoothstep(0.0,1.0,-solPos.y*2.0);
    ll= smoothstep(1.0,0.0,(FOG_CONTROL.x)/((FOG_CONTROL.y+0.3)-FOG_CONTROL.x));
    //no=pow(max(min(1.-FOG_COLOR.r*1.5,1.),0.),1.2);
    //ta=pow(max(min(1.-FOG_COLOR.b*1.5,1.),0.),.5);
    expe=pow(max(min(1.-FOG_COLOR.b*1.5,1.),0.),.5);
    highp vec4 dh = POSITION;
#ifdef ALLOW_FADE
dh.t += 10.0*RENDER_CHUNK_FOG_ALPHA;
dh.t -= 30.0*pow(RENDER_CHUNK_FOG_ALPHA,3.0);
#endif

    POS4 worldPos;
#ifdef AS_ENTITY_RENDERER
		POS4 pos = WORLDVIEWPROJ * dh;
		worldPos = pos;
#else
    worldPos.xyz = (dh.xyz * CHUNK_ORIGIN_AND_SCALE.w) + CHUNK_ORIGIN_AND_SCALE.xyz;
    worldPos.w = 1.0;
  
    
    
    POS4 pos = WORLDVIEW * worldPos;
    pos = PROJ * pos;
#endif
    gl_Position = pos;

#ifndef BYPASS_PIXEL_SHADER
    TexUV = TEXCOORD_0;
    LuxUV = TEXCOORD_1;
	color_repixel = COLOR;
#endif

#if defined(FOG) || defined(BLEND)
	#ifdef FANCY
		vec3 relPos = -worldPos.xyz;
		float cameraDepth = length(relPos);
	#else
		float cameraDepth = pos.z;
	#endif
#endif

    
    ReshaderPos.x=worldPos.x;
    ReshaderPos.y=worldPos.y;
    ReshaderPos.z=-worldPos.z;
    chunk=POSITION.xyz;
    
    lusor = worldPos.xyz;
    
    vec3 TrameisAL=POSITION.xyz;
    
    #ifdef FOG
	float len = length(lusor.xyz) / RENDER_DISTANCE;
	#ifdef ALLOW_FADE
		len += RENDER_CHUNK_FOG_ALPHA;
	#endif

    niebulaC.rgb = FOG_COLOR.rgb;
	niebulaC.a = clamp((len - FOG_CONTROL.x) / (FOG_CONTROL.y - FOG_CONTROL.x), 0.0, 1.0);
    #endif
    
    
#ifdef ALPHA_TEST 
    #ifdef FANCY
    if(color_repixel.g!=color_repixel.b&&color_repixel.r<0.6){
        gl_Position.x+=sin(TIME*5.0+TrameisAL.x+TrameisAL.z)*0.01;
    }
    #endif
#endif
    float PI = 3.14;
    float QuattroT = PI/2.0;
#ifdef BLEND
    if((color_repixel.r<color_repixel.g*1.1)&&(color_repixel.r<color_repixel.b)){
    
        float W0 = sin(TIME*5.0+TrameisAL.x*QuattroT+TrameisAL.y*QuattroT)*0.05;
        float W1 = sin(TIME*5.0+TrameisAL.y*QuattroT+TrameisAL.z*QuattroT)*0.05;
        //gl_Position.y+=sin(TIME*5.0+TrameisAL.x*QuattroT+TrameisAL.y*QuattroT)*0.08;
        gl_Position.y += mix(W0,1.0,W1);
        
    }
#endif

#ifndef BYPASS_PIXEL_SHADER
#endif
}