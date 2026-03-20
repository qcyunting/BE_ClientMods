// __multiversion__
// This signals the loading code to prepend either #version 100 or #version 300 es as apropriate.

#include "fragmentVersionCentroid.h"

#if __VERSION__ >= 300
precision highp float;
	#ifndef BYPASS_PIXEL_SHADER
		#if defined(TEXEL_AA) && defined(TEXEL_AA_FEATURE)
			_centroid in highp vec2 TexUV;
			_centroid in highp vec2 LuxUV;
		#else
			_centroid in vec2 TexUV;
			_centroid in vec2 LuxUV;
		#endif
	#endif
#else
	#ifndef BYPASS_PIXEL_SHADER
	    
		varying vec2 TexUV;
		varying vec2 LuxUV;
	#endif
#endif

uniform vec4 SUN_DIR;
uniform float TOTAL_REAL_WORLD_TIME;
const float pi = 3.1415926;
const float tau = 6.28318531;

varying vec4 color_repixel;
varying highp vec3 ReshaderPos;
varying highp vec3 chunk;
varying highp vec3 lusor;

in float ta;
in float ll;
in float no;
in float expe;

#ifdef LOW_PRECISION
varying vec4 niebulaC;
#endif

#include "uniformWorldConstants.h"
#include "uniformPerFrameConstants.h"
#include "uniformShaderConstants.h"
#include "uniformRenderChunkConstants.h"
#include "util.h"

LAYOUT_BINDING(0) uniform sampler2D TEXTURE_0;
LAYOUT_BINDING(1) uniform sampler2D TEXTURE_1;
LAYOUT_BINDING(2) uniform sampler2D TEXTURE_2;


#include "Base_REPIXEL/Function_REPIXEL.glsl"

void main(){

vec3 sunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;

sunPos.z-=0.5;
float sunAngle = sunPos.y;
vec3 pos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));

vec3 HLpos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));

#include "Base_REPIXEL/APP_REPIXEL.glsl"
#include "Base_REPIXEL/COLOR_REPIXEL.fsh"

float AKUA=acos(abs(REFP(normalize(lusor),WATTS(chunk)) ));

#ifdef BYPASS_PIXEL_SHADER
	gl_FragColor = vec4(0, 0, 0, 0);
	return;
#else 

#if USE_TEXEL_AA
	vec4 Lumen = texture2D_AA(TEXTURE_0, TexUV);
#else
	vec4 Lumen = texture2D(TEXTURE_0, TexUV);
#endif
	
#ifdef SEASONS_FAR
	Lumen.a = 1.0;
#endif

#if USE_ALPHA_TEST
	#ifdef ALPHA_TO_COVERAGE
	#define ALPHA_THRESHOLD 0.05
	#else
	#define ALPHA_THRESHOLD 0.5
	#endif
	if(Lumen.a < ALPHA_THRESHOLD)
		discard;
#endif
vec4 index = color_repixel;
#if defined(BLEND)
	Lumen.a *= index.a;
#endif

#if !defined(ALWAYS_LIT)
    Lumen *= sqrt(texture2D( TEXTURE_1, LuxUV));
#endif

//本着色器作者@楚隐霄，作品《弥浪隐霄》中所含着色器程序并不开源，请勿盗用代码，尊重他人劳动成果！
//Et auctor est scadere est @楚隐霄. Quod scadere progressio continebat in opere "Repixel" non aperta. Non furantur in codice et respicit eventus aliorum.
#ifndef SEASONS
	#if !USE_ALPHA_TEST && !defined(BLEND)
		Lumen.a = index.a;
	#endif
	
	vec3 vinaAO = normalize(index.rgb);
	Lumen.rgb *= mix(vinaAO,index.rgb,mix(1.0,0.5,LuxUV.x));
#else
	vec2 uv = index.xy;
	Lumen.rgb *= mix(Inter3, texture2D( TEXTURE_2, uv).rgb*2.0, index.b);
	Lumen.rgb *= index.aaa;
	Lumen.a = 1.0;
#endif


    vec3 TC = vec3(1.0);

 
    if(!unsuperiliquamos(FOG_COLOR)){
        
        float NdotL = dot(Vultusnormalemvector, normalize(sunPos));
        Lumen.rgb*=mix(terraBaseCU,ShadowColor,RSY*(1.0-LuxPowerContus)*(1.0-ta));
        //Lumen.rgb*=mix(TC,ShadowColor,RSG*(1.0-LuxPowerContus)*(1.0-RSY)*(1.0-ta));//斜阴影
        
        Lumen.rgb=mix(Lumen.rgb,vec3((Lumen.r+Lumen.g+Lumen.b)/2.0),mix(0.0,0.4,no*(1.0-LuxUV.x)));
        
        }
        
        //模拟曝光
        //Lumen.rgb *= mix(1.0,3.0,expe*(1.0-ta));
        //Lightmap+
        Lumen.rgb *= mix(TC,QueaColorBasicDelReshaderLumir,LuxPowerContus*(mix(0.0,1.0,no),1.0,RSS));

   
    vec4 cielorecoSia = TERRA_REPIXEL(Lumen);
  
    vec3 MieD_Dia = sunColor(sunAngle) * exp(-sqrt(pow((pos.x-sunPos.x),2.0)+pow((pos.y-sunPos.y),2.0)+pow((pos.z-sunPos.z),2.0)) * 2.0) * exp(-clamp(pos.y, 0.0, 1.0) * 2.0) * mix(2.0,5.0,ta);
    vec3 MieD_Noc = moonColor(sunAngle) * exp(-sqrt(pow((pos.x+sunPos.x),2.0)+pow((pos.y+sunPos.y),2.0)+pow((pos.z+sunPos.z),2.0)) * 2.0) * exp(-clamp(pos.y, 0.0, 1.0) * 2.0) * 5.0;
    vec3 MieD_AKUA = UnWaterSunColor(sunAngle) * exp(-sqrt(pow((pos.x-sunPos.x),2.0)+pow((pos.y-sunPos.y),2.0)+pow((pos.z-sunPos.z),2.0)) * 2.0) * exp(-clamp(pos.y, 0.0, 1.0) * 2.0) * mix(2.0,5.0,ta);
    #include "agualog.glsl";
    
        if(!unsuperiliquamos(FOG_COLOR)){
            Lumen = mix(Lumen,mix(cielorecoSia,Lumen,RSSY),distance*mix(0.6,1.2,ll));
           
        }
        Lumen.rgb=FilmToneMapping(Lumen.rgb);

    #if !defined(ALPHA_TEST)
    if(floor(gionguegiongjy.a*255.0+0.0001)==252.0){
        if(color_repixel.g<=color_repixel.r){
            Lumen.rgba = gionguegiongjy_color;
        }
    }
    #endif    
	
	gl_FragColor = Lumen;//world_0 finished
    /*=================*/
    
    //渲染下界
    #define hell(FOG_COLOR) (FOG_COLOR.r>75.0/255.0&&FOG_COLOR.g<2.0/255.0&&FOG_COLOR.b<2.0/255.0) 
    
    if(hell_det(FOG_CONTROL.x)){
    vec4 diffuse0 = texture(TEXTURE_0, TexUV);
    diffuse0.rgb *= index.rgb;    
	diffuse0.rgb *= vec3(1.2,1.0,0.8);
	diffuse0.rgb *= mix(vec3(1.0),vec3(3.0,2.0,1.0),LuxPowerContus);//光源
	diffuse0 = mix(diffuse0,FOG_COLOR,distance);
	gl_FragColor = diffuse0;
	}
	
	
    vec4 diffuse = texture(TEXTURE_0, TexUV);
    diffuse.rgb *= index.rgb;    
    if(mundoe(FOG_COLOR)){
        vec3 endsun = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
        endsun.z+=2.5;
        float endsunAngle = endsun.y;
        #ifdef BLEND
            diffuse.a = 0.5;
        #endif
        diffuse.rgb *= vec3(0.5,0.4,1.0)*0.7;//基色
        
        diffuse.rgb *= mix(TC,vec3(5.0,4.0,1.5),LuxPowerContus);//光源
        
       
        if(NVY(Vultusnormalemvector)){
            vec3 Mie_end = endlandColor(endsunAngle) * exp(-sqrt(pow((pos.x+endsun.x),2.0)+pow((pos.y+endsun.y),2.0)+pow((pos.z+endsun.z),2.0)) * 2.0) * exp(-clamp(pos.y, 0.0, 1.0) * 2.0) * 15.0;
            diffuse.rgb += Mie_end;
            }
            diffuse = mix(diffuse,NIEBUR_FINALUS(diffuse),distancexyz);
        gl_FragColor = diffuse;
    }
    
#endif // BYPASS_PIXEL_SHADER
}
