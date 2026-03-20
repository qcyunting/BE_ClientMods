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
varying highp vec3 chunk;
varying highp vec3 lusor;
varying highp vec3 ReshaderPos;
varying vec4 color;
in vec3 position;
in float ta;
in float ll;
in float no;
LAYOUT_BINDING(0) uniform sampler2D TEXTURE_0;
/*=======基本数学计算相关======*/
float POWER_DUO(float x){
    return x * x ;
}
float pow2(float x) {
    return x * x;
}

vec2 pow2(vec2 x) {
    return x * x;
}

vec3 pow2(vec3 x) {
    return x * x;
}

vec4 pow2(vec4 x) {
    return x * x;
}

float pow3(float x) {
    return x * x * x;
}

vec2 pow3(vec2 x) {
    return x * x * x;
}

vec3 pow3(vec3 x) {
    return x * x * x;
}

vec4 pow3(vec4 x) {
    return x * x * x;
}

float pow4(float x) {
    x = x * x;
    return x * x;
}

vec2 pow4(vec2 x) {
    x = x * x;
    return x * x;
}

vec3 pow4(vec3 x) {
    x = x * x;
    return x * x;
}

vec4 pow4(vec4 x) {
    x = x * x;
    return x * x;
}

float pow5(float x) {
    float x2 = x * x;
    return x2 * x2 * x;
}

vec2 pow5(vec2 x) {
    vec2 x2 = x * x;
    return x2 * x2 * x;
}

vec3 pow5(vec3 x) {
    vec3 x2 = x * x;
    return x2 * x2 * x;
}

vec4 pow5(vec4 x) {
    x = x * x;
    x = x * x;
    return x * x;
}

float pow8(float x) {
    x = x * x;
    x = x * x;
    return x * x;
}

vec2 pow8(vec2 x) {
    x = x * x;
    x = x * x;
    return x * x;
}

vec3 pow8(vec3 x) {
    x = x * x;
    x = x * x;
    return x * x;
}

vec4 pow8(vec4 x) {
    x = x * x;
    x = x * x;
    return x * x;
}


#include "Base_REPIXEL/Function_REPIXEL.glsl"

void main()
{
    
#include "Base_REPIXEL/COLOR_REPIXEL.fsh"
#if !defined(TEXEL_AA) || !defined(TEXEL_AA_FEATURE)
	vec4 diffuse = texture2D( TEXTURE_0, uv );
#else
	vec4 diffuse = texture2D_AA(TEXTURE_0, uv );
#endif

#ifdef ALPHA_TEST
	if(diffuse.a < 0.5)
		discard;
#endif
    #if !defined(ALPHA_TEST)
    #if !defined(BLEND)
        //投影天际线
    float TexSkyline=max(1.0-length(lusor.xz/(lusor.y))*0.02,0.0);
    //求天空盒纹理三通道平均值与方差
    float AVG_ColorTexturas = (diffuse.r + diffuse.g + diffuse.b)/3.0;
    float VAR_ColorTexturas = (pow2(AVG_ColorTexturas - diffuse.r) + pow2(AVG_ColorTexturas - diffuse.g) + pow2(AVG_ColorTexturas - diffuse.b))/3.0;
    diffuse.rgb = mix(diffuse.rgb, vec3((diffuse.r+diffuse.g+diffuse.b)/3.0), 1.0);
    
    //天空盒纹理中云与天空的环境光颜色
    vec4 Ambient_NubiTex = mix(mix(mix(vec4(1.2,0.9,0.8,1.0),vec4(2.0,1.3,0.35,1.0),ta),vec4(0.6,0.6,0.6,1.0),ll),vec4(0.5,0.6,0.75,1.0),no);
    vec4 Ambient_CaelTex = mix(mix(mix(vec4(1.25,1.25,1.25,1.0),vec4(0.2,0.4,0.6,1.0),ta),vec4(0.5,0.5,0.5,1.0),ll),vec4(0.2,0.2,0.2,1.0),no);
    //天空盒纹理的云和天空部分分别乘上环境光颜色
    diffuse.rgb *= 4.0;
    diffuse.rgb *= Ambient_NubiTex.rgb;
    //diffuse *= mix(Ambient_CaelTex, Ambient_NubiTex, AVG_ColorTexturas);
    //天空盒纹理颜色与实时计算的天空进行混合<
    diffuse = mix( mix( RAGNC_REPIXEL(diffuse), mix(RAGNC_REPIXEL(diffuse),diffuse,mix(0.0,1.0,VAR_ColorTexturas*2.0)), smoothstep(0.0,1.0,pow(TexSkyline,4.5)) ),  RAGNC_REPIXEL(diffuse),mix(0.0,1.0,lusor.y>0.0) );
    //diffuse = RAGNC_REPIXEL(diffuse);
    gl_FragColor = diffuse;
	gl_FragColor.rgb = FilmToneMapping(gl_FragColor.rgb);
	#endif
    vec4 diffuse0 = texture2D( TEXTURE_0, uv );
    #define INSPERACQUAINTEC(FOG_COLOR) ((FOG_COLOR.b>FOG_COLOR.r*1.05+FOG_COLOR.g*0.98)||(FOG_COLOR.g*1.2>FOG_COLOR.r+FOG_COLOR.b)||(FOG_COLOR.g>FOG_COLOR.r+FOG_COLOR.b*0.5))
    if(INSPERACQUAINTEC(FOG_COLOR)){
        diffuse0 = ACQUA_CUBE(diffuse0);
        diffuse0.rgb = FilmToneMapping(diffuse0.rgb);
        gl_FragColor = diffuse0;
    }
    #endif
	
}
