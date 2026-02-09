

#define GienereNubes vec3(3.0,1.0,3.0)
#define CovireNubes 0.6
#define HightNubesBlock0 16.0
#define HightNubesBlock1 6.0

vec4 NubeLumen(float a){
    vec4 color = mix(mix(mix(vec4(1.0), vec4(1.5,0.75,0.6,1.0),ta),vec4(0.4,0.4,0.4,0.6),ll),vec4(0.3,0.4,0.5,1.0), no);
return color;
}


#define VeloCambioLuna 0.01

#define AlturaDelHorizonte 0.04

#define HorizonStepPower 3.5

#define ColorCieloDia vec4(0.0,0.25,0.5,1.0)
#define ColorCaeloDia vec4(0.1,0.3,0.5,1.0)
#define ColorHorizDia vec4(0.6,0.7,0.8,1.0)

#define ColorCieloTar vec4(0.0,0.25,0.5,1.0)
#define ColorCaeloTar vec4(0.0,0.25,0.5,1.0)
#define ColorHorizTar vec4(1.5,0.25,0.2,1.5)

#define ColorCieloNoc vec4(0.0,0.1,0.15,1.0)
#define ColorCaeloNoc vec4(0.0,0.2,0.2,1.0)
#define ColorHorizNoc vec4(0.1,0.23,0.25,1.0)

#define ColorCieloLlo vec4(0.7,0.7,0.7,1.0)
#define ColorCaeloLlo vec4(0.7,0.7,0.7,1.0)
#define ColorHorizLlo vec4(0.7,0.7,0.7,1.0)


vec3 ACESToneMapping(vec3 color, float adapted_lum){
	const float A = 2.52;
	const float B = 0.03;
	const float C = 2.43;
	const float D = 0.59;
	const float E = 0.14;
	color *= adapted_lum;
	return (color * (A * color + B)) / (color * (C * color + D) + E);}
	

	vec3 FilmToneMapping(vec3 color)
{
	color = max(vec3(0.0), color - vec3(0.1));
	color = (color * (6.6 * color + .3)) / (color * (5.0 * color + 2.6) + 0.35);
	return color;
}


highp float REFP(highp vec3 Yaa,highp vec3 Yar){return (Yaa.x*Yar.x+Yaa.y*Yar.y+Yaa.z*Yar.z)/length(Yaa)/length(Yar);}
highp float REFV(highp vec3 Eakins){
Eakins.z+=TIME*1.0;
float doublePI = 6.28;
float WX = Eakins.x*doublePI;
float WY = Eakins.y*doublePI;
float WZ = Eakins.z*doublePI;
float TREM1 = sin(TIME*5.0+WX*0.25-cos(WZ));
float TREM2 = sin(TIME*5.0+WX+sin(WZ)+WZ*0.5);
float TREM3 = sin(TIME*5.0+WX*0.5+sin(WZ)+WZ*0.25);
float TREM4 = sin(TIME*5.0+WX*2.0+sin(WZ)+WZ);
return mix(TREM1,TREM3,TREM2)*TREM4;
}
highp vec3 WATTS(highp vec3 Vakins){
highp float Nonvoi=REFV(Vakins+vec3(0.4,0.3,0.2))-REFV(Vakins);
return vec3(-Nonvoi,0.0,1.0);}
/*======================*/


float hash21(vec2 p) {
	float r = fract(43757.5453 * sin(dot(p, vec2(12.9898, 78.233))));return r;
}
float hash22(vec2 p) {
	float r = fract(43757.5453 * cos(dot(p, vec2(12.9898, 78.233))));return r;
}
highp float hash15( highp float n ){
    return fract(cos(n)*43758.5453);
}



highp float Cractusoudmap(in highp vec2 mapFX){
highp float QN=49.0;highp float QD=QN+1.0;
highp float sient=sqrt(QN);
highp vec2 ReshaderPos=floor(mapFX);highp vec2 nioseSet=fract(mapFX);
highp float nioseCon=ReshaderPos.x+ReshaderPos.y*(QD+sient);
highp float RandOut = mix(mix(hash15(nioseCon), hash15(nioseCon+1.0),nioseSet.x), 
                          mix(hash15(nioseCon+(QD+sient)), hash15(nioseCon+ (QD+(sient+1.0))),nioseSet.x),nioseSet.y);
return RandOut;}



float FandDd(highp vec2 ReshaderPos){ReshaderPos=floor(ReshaderPos);
highp float nubeCodeDOTd=dot(ReshaderPos,vec2(0.1,ReshaderPos.y*0.5));
return hash15(nubeCodeDOTd)*0.005;
}
highp float KSFOd(highp vec2 nubelocspiri,float Qd)
{float Enputd=mix(0.64,0.73,ll),
findd=0.0;for(int recuclumFloat=0;
recuclumFloat<7;recuclumFloat++){
findd+=Cractusoudmap(nubelocspiri)*Qd/Enputd;
Enputd*=1.9;nubelocspiri*=2.8;nubelocspiri+=TIME*0.02;
nubelocspiri*=1.5;
}

return 1.0-pow(0.15,max(1.0-findd,0.0));
}


highp vec4 DeoGraciFinald(highp vec2 mapFX,highp float KSFFBMd,highp float UnderReshader){
vec4 Enputh=vec4(0.0,0.0,0.0,0.0),
	 EnNubeSpaceh=vec4(1.05);for(float recuclumFloat=0.0;recuclumFloat<1.0;recuclumFloat++){
	 EnNubeSpaceh*=vec4(0.6,0.7,1.0,0.85);
	 mapFX/=1.01; 
	 
Enputh=mix(Enputh,EnNubeSpaceh,smoothstep(0.0,0.5,KSFOd((mapFX+TIME*0.02),KSFFBMd) ) );
}return clamp(Enputh, 0.0, 1.0);}




highp float AURORA(highp vec2 nubelocspiri,float Qd)
{float Enputd=mix(0.64,0.73,ll),
findd=0.0;for(int recuclumFloat=0;
recuclumFloat<5;recuclumFloat++){
findd+=Cractusoudmap(nubelocspiri)*Qd/Enputd;
Enputd*=2.1;nubelocspiri*=2.8;nubelocspiri+=TIME*0.02;
nubelocspiri*=1.5;
}
return 1.0-pow(0.15,max(1.0-findd,0.0));
}
highp vec4 AuroraStep(highp vec2 mapFX,highp float KSFFBMd,highp float UnderReshader){
vec4 Enputh=vec4(0.0,0.0,0.0,0.0),
	 EnNubeSpaceh=vec4(1.05);for(float recuclumFloat=0.0;recuclumFloat<1.0;recuclumFloat++){
	 EnNubeSpaceh*=vec4(0.6,0.7,0.8,0.8);
	 mapFX/=1.015; 
	 
Enputh=mix(Enputh,EnNubeSpaceh,smoothstep(0.0,0.5,AURORA((mapFX+TIME*0.02),KSFFBMd) ) );
}return clamp(Enputh, 0.0, 1.0);}


highp float linestep(highp float a,highp float b,highp float x){
return clamp((x-a)/(b-a),0.0,1.0);
}
highp float ApliHashBasic(highp float ImeunaConste){
return fract(cos(ImeunaConste)*64.0);
}
highp float ApliHashEquel(highp vec2 EXP_Concriteis){
highp vec2 FlooreTemBriegne=floor(EXP_Concriteis);highp vec2 FrectusTemBriegne=fract(EXP_Concriteis);
float Otti=8.0;float Mieno=Otti-1.0;float SezDqutt=pow(Otti,2.0);
highp float ImeunaConste=FlooreTemBriegne.x+FlooreTemBriegne.y*(SezDqutt-Mieno);
highp float ReshaderTrabaisNoise=mix(mix(ApliHashBasic(ImeunaConste+0.0),
ApliHashBasic(ImeunaConste+1.0),FrectusTemBriegne.x), mix(ApliHashBasic(ImeunaConste+(SezDqutt-Mieno)),ApliHashBasic(ImeunaConste+(SezDqutt-(Mieno-1.0))),FrectusTemBriegne.x),FrectusTemBriegne.y);
return ReshaderTrabaisNoise;
}

highp float NubesBezitReshader(highp vec2 LucitesGlore,int LupSempeis){//鱼眼&分形
LucitesGlore.x+=sin(TIME*0.01);
LucitesGlore.y*=2.5;
float Nesmenstro=mix(0.9,1.4,ll);float AtErFrogeRespicite=0.0;
LucitesGlore*=0.16;LucitesGlore+=4.0;

for(int LUX=0;LUX<5;LUX++){
AtErFrogeRespicite=AtErFrogeRespicite+ApliHashEquel(LucitesGlore-AtErFrogeRespicite*2.0)/(Nesmenstro);
Nesmenstro*=2.5;LucitesGlore*=2.7;
LucitesGlore+=TIME*0.003*Nesmenstro;
}
highp float SiseDiNubis=0.09;
return pow(abs(AtErFrogeRespicite)+sqrt(SiseDiNubis),2.5);
}
vec4 NubeSollutim(vec2 FlooreTemBriegne){
float EnziBrootAR=NubesBezitReshader(FlooreTemBriegne,16); 
highp float trictom=7.0;highp float cinqidisuni=2.0;
vec4 FinalicioneReshaderN=mix(vec4(1.0)*EnziBrootAR,vec4(1.0)-EnziBrootAR,max(min(EnziBrootAR,trictom/cinqidisuni),0.0));
return exp(FinalicioneReshaderN);
}
vec4 MixNubesFinal(vec2 FlooreTemBriegne,vec4 LlamaneNumpre,vec3 LlamaneNumpri){
float CathaLache=1.0;
vec4 MejtoNermile=(CathaLache*2.0-NubeSollutim(FlooreTemBriegne))*NubeSollutim(FlooreTemBriegne); 
vec4 FinalicioneReshaderN=mix(LlamaneNumpre,
vec4(LlamaneNumpri,CathaLache),CathaLache*max(0.0,MejtoNermile.x)); 
return FinalicioneReshaderN;
}


highp float NubesBezitReshaderAR(highp vec2 LucitesGlore,int LupSempeis){//鱼眼&分形
LucitesGlore.x+=sin(TIME*0.04);
LucitesGlore.y*=6.0;
float Nesmenstro=1.3;float AtErFrogeRespicite=0.0;
LucitesGlore*=0.1;LucitesGlore+=4.0;

for(int LUX=0;LUX<3;LUX++){
AtErFrogeRespicite=AtErFrogeRespicite+ApliHashEquel(LucitesGlore-AtErFrogeRespicite*5.0)/(Nesmenstro);
Nesmenstro*=2.1;LucitesGlore*=2.0;
LucitesGlore.x+=TIME*0.1*Nesmenstro;
}
highp float SiseDiNubis=0.09;
return pow(abs(AtErFrogeRespicite)+sqrt(SiseDiNubis),2.5);
}
vec4 NubeSollutimAR(vec2 FlooreTemBriegne){
float EnziBrootAR=NubesBezitReshaderAR(FlooreTemBriegne,16); 
highp float trictom=5.0;highp float cinqidisuni=2.0;
vec4 FinalicioneReshaderN=mix(vec4(1.0)*EnziBrootAR,vec4(1.0)-EnziBrootAR,max(min(EnziBrootAR,trictom/cinqidisuni),0.0));
return exp(FinalicioneReshaderN);
}
vec4 MixNubesFinalAR(vec2 FlooreTemBriegne,vec4 LlamaneNumpre,vec3 LlamaneNumpri){
float CathaLache=0.65;
vec4 MejtoNermile=(CathaLache*2.0-NubeSollutimAR(FlooreTemBriegne))*NubeSollutimAR(FlooreTemBriegne); 
vec4 FinalicioneReshaderN=mix(LlamaneNumpre,
vec4(LlamaneNumpri,CathaLache),CathaLache*max(0.0,MejtoNermile.x)); 
return FinalicioneReshaderN;
}

highp float NubesBezitReshaderR(highp vec2 LucitesGlore,int LupSempeis){//鱼眼&分形
LucitesGlore.x+=sin(TIME*0.004);
float Nesmenstro=1.5;float AtErFrogeRespicite=0.0;
LucitesGlore*=0.1;LucitesGlore+=4.0;

for(int LUX=0;LUX<4;LUX++){
AtErFrogeRespicite=AtErFrogeRespicite+ApliHashEquel(LucitesGlore-AtErFrogeRespicite*1.0)/(Nesmenstro);
Nesmenstro*=1.65;LucitesGlore*=2.7;
LucitesGlore+=TIME*0.003*Nesmenstro;
}
highp float SiseDiNubis=0.09;
return pow(abs(AtErFrogeRespicite)+sqrt(SiseDiNubis),2.5);
}
vec4 NubeSollutimR(vec2 FlooreTemBriegne){
float EnziBrootAR=NubesBezitReshaderR(FlooreTemBriegne,16); 
highp float trictom=3.0;highp float cinqidisuni=4.0;
vec4 FinalicioneReshaderN=mix(vec4(1.0)*EnziBrootAR,vec4(1.0)-EnziBrootAR,max(min(EnziBrootAR,trictom/cinqidisuni),0.0));
return FinalicioneReshaderN;
}
vec4 MixNubesFinalR(vec2 FlooreTemBriegne,vec4 LlamaneNumpre,vec3 LlamaneNumpri){
float CathaLache=1.0;
vec4 MejtoNermile=(CathaLache*2.0-NubeSollutimR(FlooreTemBriegne))*NubeSollutimR(FlooreTemBriegne); 
vec4 FinalicioneReshaderN=mix(LlamaneNumpre,
vec4(LlamaneNumpri,CathaLache),CathaLache*max(0.0,MejtoNermile.x)); 
return FinalicioneReshaderN;
}
vec3 sunColor(float sunAngle){
    sunAngle = clamp(sunAngle + 0.1, 0.0, 1.0);
    return mix( mix(vec3(0.3),vec3(0.6,0.3,0.0)*0.7,ta),vec3(0.3),ll) * exp2(log2(sunAngle) * 0.9);
}

vec3 endColor(float sunAngle){
    sunAngle = clamp(sunAngle + 0.1, 0.0, 1.0);
    return vec3(1.5,1.1,0.2) * exp2(log2(sunAngle) * 0.9);
}
vec3 endlandColor(float sunAngle){
    sunAngle = clamp(sunAngle + 0.1, 0.0, 1.0);
    return vec3(0.8,0.4,0.2)*3.0 * exp2(log2(sunAngle) * 0.9);
}
vec3 moonColor(float sunAngle){
    sunAngle = clamp(-sin(sunAngle), 0.0, 1.0);
    return mix(vec3(0.35,0.4,0.45)*0.8,vec3(0.4),ll) * exp2(log2(sunAngle) * 0.9)*0.5;
}

vec3 UnWaterSunColor(float sunAngle){
    sunAngle = clamp(sunAngle + 0.1, 0.0, 1.0);
    return vec3(0.1,0.35,0.35) * exp2(log2(sunAngle) * 0.9);
}


float saturate(float x) {
	return clamp(x, 0.0, 1.0);
}

vec2 saturate(vec2 x) {
	return clamp(x, vec2(0.0), vec2(1.0));
}

vec3 saturate(vec3 x) {
	return clamp(x, vec3(0.0), vec3(1.0));
}

vec3 drawstars(vec3 skylight, vec3 skyvec, vec3 sunlight)
	{
		vec2 coord = floor(abs(skyvec.xz) * 400.0) / 400.0;
		vec3 stars = vec3(0.6,1.0,1.5);
		float stars_map = hash21(coord);
		
		stars_map *= hash21(coord + vec2(0.25));
		stars_map *= hash21(coord + vec2(0.25));
		stars=vec3(0.6,1.0,1.5);
		stars *= saturate(stars_map - 0.9);
		stars.xyz *= 120.0;
		
		stars *= mix(0.0, mix(1.0,0.0,ll), smoothstep(mix(0.0,1.0,ll), 1.5, skyvec.y));
		return stars + skylight;
	}


highp vec4 RAGNC_REPIXEL(vec4 colar){
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*AlturaDelHorizonte,0.0);
    vec3 SunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    vec3 SunPos1 = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    SunPos.z+=0.5; SunPos1.z+=0.42*(1.0-cos(TIME*VeloCambioLuna)*0.3);
    float sunAngle = SunPos.y;
    vec3 pos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));
    
    vec3 MieDiaPlus = sunColor(sunAngle) * exp(-sqrt(pow((pos.x-SunPos.x),2.0)+pow((pos.y-SunPos.y),2.0)+pow((pos.z-SunPos.z),2.0)) * 3.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 30.0;
    vec3 MieNocPlus = moonColor(sunAngle) * exp(-sqrt(pow((pos.x+SunPos.x),2.0)+pow((pos.y+SunPos.y),2.0)+pow((pos.z+SunPos.z),2.0)) * 3.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 30.0;
    
    vec4 LeSempreNubed0 = MixNubesFinal(lusor.xz/(lusor.y)*8.0,vec4(0.0),vec3(1.0));
    vec4 AuroraPower = AuroraStep(lusor.xz/(lusor.y)*2.0,0.6,0.8);
    vec4 LeSempreNubed = DeoGraciFinald(lusor.xz/(lusor.y)*2.0,0.6,0.8);
    
    
    vec4 auroracolor = mix(mix(mix(vec4(0.0),vec4(0.0),ta),vec4(0.0),ll),vec4(0.0,1.0,0.8,1.0), no);
    vec4 cloudcolor = mix(mix(mix( ColorHorizDia, vec4(1.0,0.2,0.2,1.0), ta), ColorHorizLlo, ll), ColorHorizNoc, no);
   
    vec4 suncolor = mix(vec4(1.0),vec4(1.5,0.6,0.4,2.0),ta);
    
    highp vec3 viewDir = normalize(-lusor);

    vec4 ColorCieloRepixel = mix(mix(mix( ColorCieloDia, ColorCieloTar, ta), ColorCieloLlo, ll), ColorCieloNoc, no);
    vec4 ColorCaeloRepixel = mix(mix(mix( ColorCaeloDia, ColorCaeloTar, ta), ColorCaeloLlo, ll), ColorCaeloNoc, no);
 
    vec4 ColorHorizRepixel = mix(mix(mix( ColorHorizDia, ColorHorizTar, ta), ColorHorizLlo, ll), ColorHorizNoc, no);       
                                                                      
    colar = ColorCieloRepixel;
    colar.rgb += mix(mix(drawstars(vec3(0.0),viewDir,vec3(0.0)),vec3(0.0),SUN_DIR.w),vec3(0.0),ll);
    
    
    colar = mix( ColorCaeloRepixel, colar, clamp(pow(Skylusor01,6.0), 0.0, 1.0) );
    
    colar = mix( ColorHorizRepixel, colar, clamp(pow(Skylusor01,3.0), 0.0, 1.0) );
    
    colar=mix( mix(mix(suncolor,colar,ll*1.1),colar,no), colar, linestep(0.123,0.125, length(pos-SunPos)) );
    
    colar=mix( colar, mix( mix(mix(colar,vec4(1.0),no),colar,ll*1.2), colar, linestep(0.13,0.135, length(pos+SunPos)) ),linestep(0.11*(1.0-cos(TIME*VeloCambioLuna)*0.4),0.115*(1.0-cos(TIME*VeloCambioLuna)*0.4), length(pos+SunPos1) ));
   
    colar = mix(colar,vec4(0.0,0.0,0.0,1.0),clamp(pow(Skylusor01,HorizonStepPower)*1.0,0.0,1.0)*mix(0.0,1.0,lusor.y>0.0));
   
    colar.rgb += MieDiaPlus.rgb+MieNocPlus.rgb;
    return colar;
}


vec4 REFLE_REPIXEL(vec4 colar){
    float acqua=acos(abs(REFP(normalize(lusor),WATTS(chunk)) ));
   
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*AlturaDelHorizonte,0.0);
    vec3 SunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    vec3 SunPos1 = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    SunPos.z-=0.5;
    SunPos1.z-=0.42*(1.0-cos(TIME*VeloCambioLuna)*0.3);
    float sunAngle = SunPos.y;
    vec3 pos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));
    vec3 posf = normalize(vec3(lusor.x, -lusor.y  , lusor.z));
    highp float Globe = clamp(max(1.0-FOG_COLOR.b*1.0-FOG_COLOR.g,0.0),0.0,1.0);
    float Reflectlansku = clamp(exp(1.0-pow(length(lusor.xz/lusor.y*2.0)*mix(0.08, 0.1, Globe),1.0))*0.2, 0.0, 1.0);
    acqua = mix(1.0,acqua,Reflectlansku);
    
    vec4 LeSempreNubedAR = AuroraStep(ReshaderPos.xz/(ReshaderPos.y)*2.0*acqua,0.6,0.8);//云
   
   
    
    vec4 cloudcolor = mix(mix(mix( ColorHorizDia, ColorHorizTar, ta), ColorHorizLlo, ll), ColorHorizNoc, no);//云颜色
    
                               
    highp vec3 viewDir = normalize(-lusor);
    
    vec4 auroracolor = mix(mix(mix(vec4(0.0),vec4(0.0),ta),vec4(0.0),ll),vec4(0.0,1.0,0.8,1.0), no);//极光颜色
    vec4 suncolor = mix(vec4(1.0,1.0,1.0,1.5),vec4(1.5,0.6,0.4,2.0),ta);
    
 
    vec4 ColorCieloRepixel = mix(mix(mix( ColorCieloDia, ColorCieloTar, ta), ColorCieloLlo, ll), ColorCieloNoc, no);
    vec4 ColorCaeloRepixel = mix(mix(mix( ColorCaeloDia, ColorCaeloTar, ta), ColorCaeloLlo, ll), ColorCaeloNoc, no);
  
    vec4 ColorHorizRepixel = mix(mix(mix( ColorHorizDia, ColorHorizTar, ta), ColorHorizLlo, ll), ColorHorizNoc, no);
    
    colar = ColorCieloRepixel;
    colar.rgb += mix(mix(drawstars(vec3(0.0),viewDir,vec3(0.0)),vec3(0.0),SUN_DIR.w),vec3(0.0),ll);                                
   
    colar = mix( ColorCaeloRepixel, colar, clamp(pow(Skylusor01,6.0), 0.0, 1.0) );

    colar = mix( ColorHorizRepixel, colar, clamp(pow(Skylusor01,3.0), 0.0, 1.0) );
 
    colar=mix(  mix(mix(suncolor,colar,ll),colar,no),  colar,  linestep(0.123,0.125, length(pos-SunPos)  )  );
    colar=mix( colar, mix(  mix(mix(colar,vec4(1.0),no),colar,ll*1.3),  colar,  linestep(0.13,0.135, length(pos+SunPos) )  ),linestep(0.11*(1.0-cos(TIME*VeloCambioLuna)*0.4),0.115*(1.0-cos(TIME*VeloCambioLuna)*0.4), length(pos+SunPos1) ));

    return colar;
}

vec4 TERRA_REPIXEL(vec4 colar){
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*AlturaDelHorizonte,0.0);
    highp vec3 viewDir = normalize(-lusor);
    vec3 SunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    SunPos.z-=0.5;
    float sunAngle = SunPos.y;
    vec3 pos = normalize(vec3(lusor.x, lusor.y  , -lusor.z));
    
    vec3 MieDiaPlus = sunColor(sunAngle) * exp(-sqrt(pow((pos.x-SunPos.x),2.0)+pow((pos.y-SunPos.y),2.0)+pow((pos.z-SunPos.z),2.0)) * 3.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 30.0;
    vec3 MieNocPlus = moonColor(sunAngle) * exp(-sqrt(pow((pos.x+SunPos.x),2.0)+pow((pos.y+SunPos.y),2.0)+pow((pos.z+SunPos.z),2.0)) * 3.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 30.0;
    
   
    vec4 ColorCieloRepixel = mix(mix(mix( ColorCieloDia, ColorCieloTar, ta), ColorCieloLlo, ll), ColorCieloNoc, no);
    vec4 ColorCaeloRepixel = mix(mix(mix( ColorCaeloDia, ColorCaeloTar, ta), ColorCaeloLlo, ll), ColorCaeloNoc, no);
   
    vec4 ColorHorizRepixel = mix(mix(mix( ColorHorizDia, ColorHorizTar, ta), ColorHorizLlo, ll), ColorHorizNoc, no);       
                
   
    colar = mix( ColorHorizRepixel, colar, clamp(pow(Skylusor01,3.0), 0.0, 1.0) );
   
    colar.rgb += MieDiaPlus.rgb+MieNocPlus.rgb;
    return colar;
}


vec4 INSPERACQUA(vec4 colar){
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*0.1,0.0);
    highp vec3 viewDir = normalize(-lusor);
    vec3 SunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    SunPos.z-=0.5;
    float sunAngle = SunPos.y;
    vec3 pos = normalize(vec3(lusor.x, lusor.y  , -lusor.z));
    
    vec3 MieDiaPlus = UnWaterSunColor(sunAngle) * exp(-sqrt(pow((pos.x-SunPos.x),2.0)+pow((pos.y-SunPos.y),2.0)+pow((pos.z-SunPos.z),2.0)) * 3.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 30.0;

    vec4 RcielocolorUniform = vec4(0.2,0.5,0.5,1.0) ; 
    vec4 RciellcolorUniform = vec4(0.1,0.3,0.3,1.0) ; 
    colar = RcielocolorUniform;

    colar = mix( RciellcolorUniform,colar,clamp(pow(Skylusor01,2.5)*1.0,-0.5,1.0));
    colar = mix(colar,vec4(0.0,0.0,0.0,1.0),clamp(pow(Skylusor01,1.5)*1.0,0.0,1.0)*mix(1.0,0.0,lusor.y>0.01));
    
    colar.rgb += MieDiaPlus.rgb;
    return colar;
}

highp vec4 ACQUA_CUBE(vec4 colar){
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*0.1,0.0);
    vec3 SunPos = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
    SunPos.z+=0.5;
    float sunAngle = SunPos.y;
    vec3 pos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));
   
    vec3 MieDiaPlus = UnWaterSunColor(sunAngle) * exp(-sqrt(pow((pos.x-SunPos.x),2.0)+pow((pos.y-SunPos.y),2.0)+pow((pos.z-SunPos.z),2.0)) * 3.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 30.0;
    
    vec4 RcielocolorUniform = vec4(0.2,0.5,0.5,1.0) ; 
    vec4 RciellcolorUniform = vec4(0.1,0.3,0.3,1.0) ; 
                                                                                          
    colar = RcielocolorUniform;
  
    colar = mix( RciellcolorUniform,colar,clamp(pow(Skylusor01,2.5)*1.0,-0.5,1.0));
    
   
    colar = mix(colar,vec4(0.0,0.0,0.0,1.0),clamp(pow(Skylusor01,1.5)*1.0,0.0,1.0)*mix(0.0,1.0,lusor.y>0.05));

    colar.rgb += MieDiaPlus.rgb;
    return colar;
}


vec4 CAELO_FINALUS(vec4 colar){
    vec3 endsun = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;

    endsun.z+=2.5;
    vec3 pos = normalize(vec3(lusor.x, lusor.y  , lusor.z));
    float endsunAngle = endsun.y;
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*0.05,0.0);
    
    highp vec3 viewDir = normalize(-lusor);
                                          
    vec4 RcielocolorUniform = vec4(0.0,-0.2,0.2,1.0);
    vec4 RciellcolorUniform = vec4(0.25,0.1,0.45,1.0);
  
    colar = RcielocolorUniform;
    
    colar = mix( RciellcolorUniform,colar,smoothstep(0.0,1.0,pow(Skylusor01,4.5)));
    colar.rgb += mix(drawstars(vec3(0.0),viewDir,vec3(0.0))*vec3(1.5,0.4,0.9),vec3(0.0),-SUN_DIR.w);
    vec3 Mie_end = endColor(endsunAngle) * exp(-sqrt(pow((pos.x+endsun.x),2.0)+pow((pos.y+endsun.y),2.0)+pow((pos.z+endsun.z),2.0)) * 2.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 10.0;
    colar.rgb += Mie_end;
    colar.rgb = FilmToneMapping(colar.rgb);
    return colar;
}

vec4 NIEBUR_FINALUS(vec4 colar){
    vec3 endsun = SUN_DIR.xyz*(SUN_DIR.w*2.0 - 1.0)-SUN_DIR.z*0.5;
 
    endsun.z+=2.5;
    vec3 pos = normalize(vec3(lusor.x, -lusor.y  , -lusor.z));
    float endsunAngle = endsun.y;
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*0.05,0.0);
    
    
                                          
    vec4 RcielocolorUniform = vec4(0.0,-0.2,0.2,1.0);
    vec4 RciellcolorUniform = vec4(0.25,0.1,0.45,1.0);
    colar = RcielocolorUniform;
    colar = mix( RciellcolorUniform,colar,smoothstep(0.0,1.0,pow(Skylusor01,4.5)));
   
    vec3 Mie_end = endColor(endsunAngle) * exp(-sqrt(pow((pos.x+endsun.x),2.0)+pow((pos.y+endsun.y),2.0)+pow((pos.z+endsun.z),2.0)) * 2.0) * exp(-clamp(pos.y, 0.0, 1.0) * 4.0) * 10.0;
    colar.rgb += Mie_end;
    colar.rgb = FilmToneMapping(colar.rgb);
    return colar;
}

vec4 HellFOG(vec4 colar){
    float Skylusor01=max(1.0-length(lusor.xz/(lusor.y))*0.1,0.0);
    vec4 RcielocolorUniform = vec4(0.3,0.2,0.0,1.0);
    vec4 RciellcolorUniform = vec4(0.5,0.1,0.2,1.0);
    colar = RcielocolorUniform;
    colar = mix( RciellcolorUniform,colar,smoothstep(0.0,1.0,pow(Skylusor01,4.5)));
    colar.rgb = FilmToneMapping(colar.rgb);
    return colar;
}