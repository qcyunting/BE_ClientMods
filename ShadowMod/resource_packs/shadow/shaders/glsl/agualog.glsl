//渲染水与水下
#if !defined(ALPHA_TEST)
#ifdef BLEND
if(aguolog(index)&&!unsuperiliquamos(FOG_COLOR))
    {
    //反射图
    vec4 wfsc = REFLE_REPIXEL(Lumen);
    wfsc.a *= mix(1.0,0.5,ll);
    //混合进菲涅尔方程
    Lumen = mix(mix(wfsc,Lumen,Frasnel),Lumen,RSY);
    //反射的米氏散射
	Lumen.rgb += sunColor(sunAngle) * exp(-sqrt(pow((HLpos.x-sunPos.x),2.0)+pow((HLpos.y-sunPos.y),2.0)+pow((HLpos.z-sunPos.z),2.0)) * 3.0) * exp(-clamp(HLpos.y, 0.0, 1.0) * 4.0) * 30.0;
    Lumen.rgb += moonColor(sunAngle) * exp(-sqrt(pow((HLpos.x+sunPos.x),2.0)+pow((HLpos.y+sunPos.y),2.0)+pow((HLpos.z+sunPos.z),2.0)) * 3.0) * exp(-clamp(HLpos.y, 0.0, 1.0) * 4.0) * 30.0;

    //Lumen = mix(Lumen, vec4(0.2,0.3,0.4,0.5),RSY);//水面在室内不该反射天空
    }
#endif
#endif
if(unsuperiliquamos(FOG_COLOR))
    {
    #ifdef BLEND
    if(aguolog(index)){Lumen=mix(vec4(0.2,0.4,0.4,0.2),INSPERACQUA(Lumen),clamp(((length(lusor.xyz) / RENDER_DISTANCE) - FOG_CONTROL.x) / (FOG_CONTROL.y - FOG_CONTROL.x), 0.0, 1.0));}//在水下抬头看水面的颜色
    #endif
    //Lumen.rgb+=mix(AKUA*0.1,0.0,RSSY);
    if(NVY(Vultusnormalemvector)){
    Lumen.rgb=Lumen.rgb+MieD_AKUA.rgb*1.5;}//模拟漫反射
    Lumen.rgb*=mix(vec3(0.4,0.7,0.9),vec3(0.5,1.5,2.0)*0.7,LuxUV.x)*0.7;//水下光源
    Lumen=mix(Lumen,INSPERACQUA(Lumen),clamp(((length(lusor.xyz) / RENDER_DISTANCE) - FOG_CONTROL.x) / (FOG_CONTROL.y - FOG_CONTROL.x), 0.0, 1.0));//水下雾
    }
//Lumen.rgb*=AKUA;