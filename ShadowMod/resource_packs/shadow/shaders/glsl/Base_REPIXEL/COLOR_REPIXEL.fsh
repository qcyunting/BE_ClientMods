//本着色器作者@重生的老楚，作品《重生像素》中所含着色器程序并不开源，请勿盗用代码，尊重他人劳动成果！
//Et auctor est scadere est @重生的老楚. Quod scadere progressio continebat in opere "Repixel" non aperta. Non furantur in codice et respicit eventus aliorum.
vec3 testcolor = vec3(1.0,0.0,0.0);
vec3 Inter3 = vec3(1.0);
vec4 Inter4 = vec4(1.0);

vec4 RaColorUniform = mix(mix(mix(
vec4(1.5,1.0,0.5,1.5),    
vec4(2.5,0.5,-0.5,3.5),ta),
vec4(0.5,0.5,0.5,0.0),ll),
vec4(2.0),no);

vec4 NuColorUniform = mix(mix(mix(
vec4(1.0),    
vec4(1.0,0.8,0.6,1.0),ta),
vec4(0.5,0.5,0.5,0.0),ll),
vec4(0.5,0.5,0.5,0.0),no);



vec3 QueaColorBasicDelReshaderLumir=vec3(10.0,4.0,2.0)*(1.0+sin(TIME*3.6)*0.2);
vec3 AOdeTerrae = vec3(0.2);

vec3 ShadowColor = mix(mix(mix(
vec3(1.0,1.0,0.8),    
vec3(1.0),ta),
vec3(1.0),ll),
vec3(1.0),no)*0.8;



vec3 terraBaseCU = mix(mix(mix(
vec3(1.7,1.55,1.4),    
vec3(0.9,0.8,0.6),ta),
vec3(0.85),ll),
vec3(0.85),no)*0.6;

vec4 FOGCOLOR = mix(mix(mix(
vec4(0.4,0.5,0.7,1.0),    
vec4(0.5,0.4,0.3,1.0),ta),
vec4(0.7,0.7,0.7,0.0),ll),
vec4(0.25,0.4,0.55,1.0),no);

vec4 WATERCOLOR = mix(mix(mix(
vec4(0.4,0.55,0.7,0.5),    
vec4(0.4,0.55,0.7,0.5),ta),
vec4(0.7,0.7,0.7,0.5),ll),
vec4(0.2,0.4,0.5,0.5),no);

vec3 NubesDeTerrae = WATERCOLOR.rgb*1.0;


highp float terraLumenPower = mix(1.0,0.4,no);