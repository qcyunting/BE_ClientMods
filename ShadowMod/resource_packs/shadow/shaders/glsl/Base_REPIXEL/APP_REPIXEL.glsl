//本着色器作者@重生的老楚，作品《重生像素》中所含着色器程序并不开源，请勿盗用代码，尊重他人劳动成果！
//Et auctor est scadere est @重生的老楚. Quod scadere progressio continebat in opere "Repixel" non aperta. Non furantur in codice et respicit eventus aliorum.
vec3 Vultusnormalemvector= normalize(cross(dFdy(lusor),dFdx(chunk)));
vec4 corazion = texture2D( TEXTURE_0, TexUV );

#define NVY(Vultusnormalemvector) (Vultusnormalemvector.y<-0.8)
#define NVYB(Vultusnormalemvector) (Vultusnormalemvector.y>0.8)
#define NVX(Vultusnormalemvector) (Vultusnormalemvector.x<-0.8)
#define NVXB(Vultusnormalemvector) (Vultusnormalemvector.x>0.8)
#define NVZ(Vultusnormalemvector) (Vultusnormalemvector.z<-0.8)
#define NVZB(Vultusnormalemvector) (Vultusnormalemvector.z>0.8)

#define l(color_repixel) (color_repixel.a==0.0)
#define grasyp(color_repixel) (color_repixel.r!=color_repixel.g)
//#define mundos(FOG_COLOR) (FOG_COLOR.r>252.0/255.0&&FOG_COLOR.g<2.0/255.0&&FOG_COLOR.b<2.0/255.0)
//#define mundos(FOG_CONTROL) (FOG_CONTROL.x<0.055&&FOG_CONTROL.x>0.045)
#define hell_det(CN) (CN<0.11&&CN>0.0)
//#define mundoe(FOG_COLOR) ((FOG_COLOR.r > FOG_COLOR.g)&&(FOG_COLOR.b > FOG_COLOR.g)&&(FOG_COLOR.b > FOG_COLOR.r)&&(FOG_COLOR.r < 0.05&&FOG_COLOR.b < 0.05&&FOG_COLOR.g < 0.05))
#define mundoe(FOG_COLOR) (FOG_COLOR.r>252.0/255.0&&FOG_COLOR.g>252.0/255.0&&FOG_COLOR.b>252.0/255.0)
#define aguolog(index) (index.r<index.g&&index.r*1.1<index.b&&index.g<index.b*1.25&&index.b*index.b>index.r*index.g)
#define smoslat(color_repixel) (color_repixel.g+color_repixel.g>color_repixel.b+color_repixel.r&&color_repixel.a!=0.0)
#define unsuperiliquamos(FOG_COLOR) ((FOG_COLOR.b>FOG_COLOR.r*1.05+FOG_COLOR.g*0.98)||(FOG_COLOR.g*1.2>FOG_COLOR.r+FOG_COLOR.b)||(FOG_COLOR.g>FOG_COLOR.r+FOG_COLOR.b*0.5))
//functions of pixel logic
float distance=length(lusor.xz)/RENDER_DISTANCE;
float distancexyz=length(lusor.xyz)/RENDER_DISTANCE;
float RSY=(1.0-clamp((LuxUV.y-0.85)*30.0,0.0,1.0));
float RSGS=(1.0-clamp((color_repixel.g-0.52)*5.0,0.0,1.0));
float RSG=(1.0-clamp((color_repixel.g-0.47)*15.0,0.0,1.0));
float RSS=(1.0-clamp((LuxUV.y-0.1)*1.0,0.0,1.0));
float RSSY=(1.0-clamp((LuxUV.y+0.2)*1.0,0.0,1.0));

float NieburaCIE=(1.0-clamp((lusor.y+48.0)*0.03,0.0,1.0));
float NieburaHOR=(1.0-clamp((lusor.y-8.0)*0.03,0.0,1.0));
float NieburaGLO=(1.0-clamp((lusor.y+20.0)*0.015,0.0,1.0));

highp float globe = clamp(max(1.0-FOG_COLOR.b*1.0-FOG_COLOR.g,0.0),0.0,1.0);
float reflectlansku = clamp(exp(1.0-pow(length(lusor.xz/lusor.y*2.0)*mix(0.08, 0.1, globe),1.0))*0.2, 0.0, 1.0);
float Frasnel = clamp(exp(1.0-pow(length(lusor.xz/lusor.y*2.0)*mix(0.1, 0.2, globe),1.0))*0.3, 0.0, 1.0);
//float disref=(1.0-clamp((lusor.y-lusor.y*0.9)*0.2,0.0,1.0));
float LuxPowerContus = pow(LuxUV.x,7.0);

vec4 gionguegiongjy=textureLod(TEXTURE_0,TexUV,0.0);
vec4 gionguegiongjy_color=textureLod(TEXTURE_0,TexUV,0.0).rgba;