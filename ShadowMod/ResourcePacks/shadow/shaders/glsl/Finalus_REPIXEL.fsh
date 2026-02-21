// __multiversion__
// This signals the loading code to prepend either #version 100 or #version 300 es as apropriate.

#include "fragmentVersionCentroid.h"
//本着色器作者@重生的老楚，作品《重生像素》中所含着色器程序并不开源，请勿盗用代码，尊重他人劳动成果！
//Et auctor est scadere est @重生的老楚. Quod scadere progressio continebat in opere "Repixel" non aperta. Non furantur in codice et respicit eventus aliorum.
#if __VERSION__ >= 300
precision highp float;
#if defined(TEXEL_AA) && defined(TEXEL_AA_FEATURE)
_centroid in highp vec2 uv;
#else
_centroid in vec2 uv;
#endif

#else

varying vec2 uv;

#endif
#include "uniformWorldConstants.h"
#include "uniformPerFrameConstants.h"
#include "uniformShaderConstants.h"
#include "uniformRenderChunkConstants.h"
#include "util.h"
uniform vec4 SUN_DIR;
uniform float TOTAL_REAL_WORLD_TIME;
const float pi = 3.1415926;
const float tau = 6.28318531;
varying highp vec3 chunk;
varying highp vec3 lusor;
varying highp vec3 ReshaderPos;
varying vec4 color;
in vec3 position;
in float ta;
in float ll;
in float no;
LAYOUT_BINDING(0) uniform sampler2D TEXTURE_0;

#include "Base_REPIXEL/Function_REPIXEL.glsl"

void main()
{
    vec3 sunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    vec3 lunaPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    vec3 lunaHidePos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    sunPos.z+=2.5;
    lunaPos.z+=2.8;
    lunaHidePos.z+=2.6;
    
    float sunAngle = sunPos.y;
    float lunaAngle = lunaPos.y;
    vec3 pos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));

#if !defined(TEXEL_AA) || !defined(TEXEL_AA_FEATURE)
	vec4 diffuse = texture2D( TEXTURE_0, uv );
#else
	vec4 diffuse = texture2D_AA(TEXTURE_0, uv );
#endif

#ifdef ALPHA_TEST
	if(diffuse.a < 0.5)
		discard;
#endif
    
    diffuse=CAELO_FINALUS(diffuse);
    
    vec4 lunacolor = vec4(1.8,1.4,1.2,1.0);
    vec4 lunabloom = vec4(1.5,0.8,1.0,1.5);
	float HIDE=max(1.0-length(lusor.xz/(lusor.y))*0.25,0.0);//穹顶地平线
    
	
	diffuse=mix(mix( mix(diffuse,lunabloom,linestep(1.795,1.8, length(pos-lunaHidePos))), diffuse, linestep(1.99,1.995, length(pos-lunaPos)) ),diffuse,clamp(pow(HIDE,1.0)*2.0,0.0,1.0));
	diffuse=mix( mix(diffuse,lunacolor,linestep(1.8,1.8, length(pos-lunaHidePos))), diffuse, linestep(1.99,1.99, length(pos-lunaPos)) );
    
    //diffuse = mix(diffuse,vec4(1.0),clamp(pow(HIDE,1.0)*2.0,0.0,1.0));
	gl_FragColor=diffuse;
}
