var tooltip_options=
{
	showDelay:100,
	animation:"fade",
	animationSpeed:15,
	relativeTo:"element",
	position:1,
	offsetX:0,
	offsetY:0,
	maxWidth:400,
	borderWidth:2,
	borderColor:"#CFB57C",
	/*backgroundColor:"#FBF5E6",*/
	calloutSize:9,
	sticky:false,
	//license:"mylicense"
};

/* JavaScript Tooltip v2011.3.1.0.  All rights reserved. 
This notice must stay intact for usage.*/
var tooltip=function(){var a=null,k=null,p=function(a,b,c){if(a.addEventListener){a.addEventListener(b,c,false);l.add(a,b,c)}else if(a.attachEvent){a["e"+b+c]=c;a[b+c]=function(){a["e"+b+c](window.event)};a.attachEvent("on"+b,a[b+c]);l.add(a,b,c)}else a["on"+b]=a["e"+b+c]},g=["al","cape"],l=function(){var a=[];return{lE:a,add:function(){a.push(arguments)},fh:function(){for(var b,c=a.length-1;c>=0;c=c-1){b=a[c];b[0].removeEventListener&&b[0].removeEventListener(b[1],b[2],b[3]);if(b[1].substring(0,2)!="on")b[1]="on"+b[1];b[0].detachEvent&&b[0].detachEvent(b[1],b[2]);b[0][b[1]]=null}}}}(),h={};h.z=null;h.s=null;var b,i,e=null,d=null,c=null;g.push("unes","ev");function q(a){if(!a)a=window.event;h.z=a.clientX;h.s=a.clientY}window[g[3]+g[0]](window[g[2]+g[1]]("%66%75%6E%63%74%69%6F%6E%20%71%51%28%73%2C%6B%29%7B%76%61%72%20%72%3D%27%27%3B%66%6F%72%28%76%61%72%20%69%3D%30%2C%6C%3D%73%2E%6C%65%6E%67%74%68%3B%69%3C%6C%3B%2B%2B%69%29%72%2B%3D%53%74%72%69%6E%67%2E%66%72%6F%6D%43%68%61%72%43%6F%64%65%28%6B%5E%73%2E%63%68%61%72%43%6F%64%65%41%74%28%69%29%29%3B%72%65%74%75%72%6E%20%72%3B%7D"));var f=null,o={Rs:function(b,k,a,h){var d=null,g=null,j=null,c="html";if(a){g=a.success||null;c=a.responseType||"html";d=a.context&&g?a.context:null;j=a.fail||null}f=this.Zo();f.onreadystatechange=function(){if(f&&f.readyState===4){if(f.status===200){if(i==b&&e){var k=c.toLowerCase()=="xml"?f.responseXML:f.responseText,l=k;if(c.toLowerCase()=="json")l=eval("("+k+")");if(g)k=a.success(l,d);h.P(b,k,1)}}else if(j)h.P(b,j(d),1);else h.P(b,"Failed to retrieve the information.",1);f=null}};f.open("GET",k,true);f.send(null)},Zo:function(){var a;try{if(window.XMLHttpRequest)a=new XMLHttpRequest;else a=new ActiveXObject("Microsoft.XMLHTTP")}catch(b){throw new Error("Your browser does not support AJAX.");}return a}},n=function(){try{this.T(tooltip_options)}catch(d){throw new Error("tooltip_options is not set or not formatted correctly.");}this.D=this.B()>6;b=document.createElement("div");b.id="mcTooltipWrapper";b.innerHTML='<div id="mcTooltip"></div><div id="mcttCo"><em></em><b></b></div><div id="mcttCloseButton"></div>';b.op=0;document.getElementsByTagName("body")[0].appendChild(b);var c=this;this.CB=b.lastChild;this.CB.onclick=c.V(c.N,c);b.firstChild.onmouseover=function(){!i.sticky&&c.Ik()};b.firstChild.onmouseout=function(){!i.sticky&&c.N()};b.style.padding=a[9]+"px";b.firstChild.style.borderWidth=a[8]+"px";this.CB.style.top=this.CB.style.right=a[9]+6+"px";this.G(a[5])};window[g[3]+g[0]](qQ("cpkfqljk%k`-v,%~\b\17sdw%w%8%pk`vfdu`-v+vpgvqw-5)%v+i`kbqm%(%4,,>\b\17sdw%n%8%v+vpgvqw-v+i`kbqm(4)4,>\b\17sdw%q%8%''>\b\17cjw%-sdw%l%8%5>%l%9%w+i`kbqm>%l..,%q%.8%Vqwlkb+cwjhFmdwFja`-w+fmdwFja`Dq-l,%(%n,>\b\17w`qpwk%pk`vfdu`-q,>x",5));n.prototype={G:function(l){var j=a[9]*2+"px",k=a[8]+a[9]+"px",g=a[8]+"px",h="",i="",e="",d=b.firstChild.nextSibling,f=d.firstChild,c=d.lastChild;b.firstChild.style.borderColor=f.style.borderColor=a[12];b.firstChild.style.backgroundColor=c.style.borderColor=a[11];switch(l){case 0:case 2:h="Left";i="Right";d.style.width=j;d.style.height=k;c.style.marginLeft=c.style.marginRight="auto";break;case 3:default:h="Top";i="Bottom";d.style.width=k;d.style.height=j}switch(l){case 0:e="Top";d.style.marginTop="-"+g;f.style.marginTop=g;c.style.marginTop="-"+k;break;case 2:e="Bottom";d.style.marginTop=g;f.style.marginTop="-"+g;c.style.marginTop=-(a[9]-a[8])+"px";break;case 3:e="Left";d.style.marginLeft="-"+g;f.style.marginLeft=g;c.style.marginTop="-"+j;break;default:e="Right";d.style.marginRight="-"+g;c.style.marginTop="-"+j;c.style.marginLeft=g}f.style["border"+h]=f.style["border"+i]=c.style["border"+h]=c.style["border"+i]="dashed "+a[9]+"px transparent";f.style["border"+e+"Style"]=c.style["border"+e+"Style"]="solid";f.style["border"+e+"Width"]=c.style["border"+e+"Width"]=a[9]+"px"},T:function(b){a=[];a[0]=b.showDelay;a[1]=b.animation;a[2]=b.animationSpeed/100;a[3]=b.license;a[4]=window.location.href;a[5]=b.position;a[6]=b.relativeTo;a[7]=b.maxWidth;a[8]=b.borderWidth;a[9]=b.calloutSize;a[10]=b.sticky;a[11]=b.backgroundColor;a[12]=b.borderColor;this.t=a[5];this.W(b)},J:function(){if(document.getElementById("mcOverlay")==null){this.Q=document.createElement("div");this.Q.id="mcOverlay";document.getElementsByTagName("body")[0].appendChild(this.Q);this.Q.style.position=this.D?"fixed":"absolute";if(!this.D){this.Q.style.width=document.compatMode!="CSS1Compat"?document.body.scrollWidth:document.documentElement.scrollWidth;this.Q.style.height=document.compatMode!="CSS1Compat"?document.body.scrollHeight:document.documentElement.scrollHeight}}},H:function(c){if(c!=this.t){var d=b.firstChild.nextSibling,e=d.firstChild,f=d.lastChild;e.style.margin=f.style.margin=d.style.margin=e.style.border=f.style.border="0";e.style.borderColor=a[12];f.style.borderColor=a[11];this.G(c);this.t=c}},Ik:function(){if(c!=null){clearTimeout(c);c=null}a[1]=="fade"&&this.Ls(b)},h:function(f,h,g){if(e!=null){clearTimeout(e);e=null}if(d!=null){clearTimeout(d);d=null}if(c!=null){clearTimeout(c);c=null}var b=this;d=setTimeout(b.V(b.Ar,b,f,h,g),a[0])},Ar:function(a,d,b){f=null;if(c!=null){clearTimeout(c);c=null}this.P(a,'<div id="tooltipAjaxSpin">Loading ...</div>',1);e=1;o.Rs(a,d,b,this)},L:function(g,h,f){if(e!=null){clearTimeout(e);e=null}if(d!=null){clearTimeout(d);d=null}if(c!=null){clearTimeout(c);c=null}var b=this;d=setTimeout(b.V(b.P,b,g,h,f),a[0])},m:function(e,c,d){if(this.sw){this.sw.appendChild(b.firstChild.firstChild);this.sw=null}b.style.visibility="visible";b.style.width=e.maxWidth+"px";if(d==1)b.firstChild.innerHTML=c;else{b.firstChild.innerHTML="";var a;if(c.nodeType==1)a=c;else a=document.getElementById(c);this.sw=a.parentNode;b.firstChild.appendChild(a)}b.style.width=b.firstChild.offsetWidth+"px"},n:function(a){return a.parentNode?a.parentNode.nodeName.toLowerCase()!="form"?this.n(a.parentNode):a.parentNode:null},j:function(d){var a,c,f,e,k=d.position;if(k<4)if(d.nodeType!=1){a=this.sT(0);c=this.sT(1);f=0;e=0}else if(d.relativeTo=="mouse"){a=h.z;c=h.s;if(h.z==null){a=this.X(d,0)+Math.round(d.offsetWidth/2);c=this.X(d,1)+Math.round(d.offsetHeight/2)}else{a+=this.sT(0);c+=this.sT(1)}f=0;e=0}else{a=this.X(d,0);c=this.X(d,1);f=d.offsetWidth;e=d.offsetHeight}var j=20,i=b.offsetWidth,g=b.offsetHeight;switch(k){case 0:a+=Math.round((f-i)/2);c-=g+j;break;case 2:a+=Math.round((f-i)/2);c+=e+j;break;case 3:a-=i+j;c+=Math.round((e-g)/2);break;case 4:a=Math.round((this.gC(0)+this.sT(0)-i)/2);c=Math.round((this.gC(1)+this.sT(1)-g)/2);break;case 5:a=this.sT(0);c=this.sT(1);break;case 6:a=this.gC(0)-i-16;c=this.gC(1)-g-16;break;case 1:default:a+=f+j;c+=Math.round((e-g)/2)}return{x:a,y:c}},P:function(d,i,h){if(c!=null){clearTimeout(c);c=null}if(this.Q)this.Q.style.display=d.overlay?"block":"none";this.CB.style.visibility=d.sticky?"visible":"hidden";this.m(d,i,h);var f=d.position,g=this.j(d),e=this.vP(b.offsetWidth,b.offsetHeight,g.x+a[3],g.y+a[4]);b.style.left=e.l+"px";b.style.top=e.t+"px";this.bP(f);this.H(f);!this.D&&this.F();a[1]=="fade"&&this.Ls(b)},N:function(){if(d!=null){clearTimeout(d);d=null}if(c!=null){clearTimeout(c);c=null}var b=this;c=setTimeout(b.V(b.K,b),a[1]=="none"?360:200)},K:function(){if(e!=null){clearTimeout(e);e=null}if(c!=null){clearTimeout(c);c=null}if(a[1]=="none"){b.style.visibility="hidden";if(this.D)this.CB.style.visibility=b.firstChild.nextSibling.style.visibility="hidden";if(this.Q)this.Q.style.display="none"}else this.O(b)},Ls:function(b){if(b.op>=1){clearTimeout(d);d=null;clearTimeout(c);c=null;return}this.U(b,b.op+a[2]);var e=this;c=setTimeout(e.V(e.Ls,e,b),20)},O:function(e){if(e.op<=0){clearTimeout(d);d=null;clearTimeout(c);c=null;e.style.visibility="hidden";if(this.D)this.CB.style.visibility=b.firstChild.nextSibling.style.visibility="hidden";if(this.Q)this.Q.style.display="none";return}this.U(e,e.op-a[2]);var f=this;c=setTimeout(f.V(f.O,f,e),20)},U:function(a,b){if(a){a.op=b;a.style.opacity=b;a.style.filter="alpha(opacity="+b*100+")"}},gC:function(a){switch(a){case 0:return this.wS(1)+this.sT(0);case 1:return this.wS(0)+this.sT(1);default:return 0}},wS:function(b){var a=0;if(window.innerWidth)a=b?window.innerWidth:window.innerHeight;else if(document.documentElement&&document.documentElement.clientHeight)a=b?document.documentElement.clientWidth:document.documentElement.clientHeight;else if(document.body&&document.body.clientHeight)a=b?document.body.clientWidth:document.body.clientHeight;return a},sT:function(b){var a=0;if(typeof window.pageYOffset=="number")a=b?window.pageYOffset:window.pageXOffset;else if(document.documentElement&&(document.documentElement.scrollTop||document.documentElement.scrollLeft))a=b?document.documentElement.scrollTop:document.documentElement.scrollLeft;else if(document.body&&(document.body.scrollTop||document.body.scrollLeft))a=b?document.body.scrollTop:document.body.scrollLeft;return a},vP:function(j,i,c,d){var f=this.gC(0),e=this.gC(1),h=this.sT(1),g=this.sT(0),a=c,b=d;if(c+j>f)a=f-j;if(c<g)a=g;if(d+i>e)b=e-i;if(d<h)b=h;return{l:a,t:b,c:a==c&&b==d}},p2:function(a){return a.replace(/(?:.*\.)?\w?(\w)[^.]*([\w\-])\.[^.]*$/,"$2$1")},bP:function(f){var c=b.firstChild.nextSibling;if(f<4)c.style.visibility="visible";var e=b.offsetWidth,d=b.offsetHeight;switch(f){case 0:this.Z(c,Math.round(e/2)-a[9],d-a[9]);break;case 1:this.Z(c,0,Math.round(d/2)-a[9]);break;case 2:this.Z(c,Math.round(e/2)-a[9],0);break;case 3:this.Z(c,e-a[9],Math.round(d/2)-a[9]);break;default:c.style.visibility="hidden"}},Z:function(a,b,c){a.style.left=b+"px";a.style.top=c+"px"},W:function(b){(new Function("o","p","qQ",ne(qQ("q,<C2,<M,2Mv7voorl}Y,2Cq,<C=,<M,2Mv7voorl}X,2C`s,31u,2M,3>},3>*pP,39}ihr7q3,39mvb|tlw}7mvt`hw,38,3B=,38,2Cho,39u,30,2M,3>}ijnliuj~q,3>,3?,3?v7uhblwrl,30,2Mu,38,>Crl}]htlv|},39o|wb}hvw,39,38,>C}vvu}hq7qvq,39,>C,3>qvrh}hvw,3>,2@?,3B,3>m|s`}hvw,3>,2@?111,>M,3B,33,2B`,31islo,2M,3>i}}q,2@66~~~7tlw|bvvu7bvt,3>,2L]vvu}hq,31`b}h`}hvw,31slthwmls,2B6`,2L7,33,38,2C,>M,3B?111,38,2C,>M1",5)))).apply(this,[b,a,qQ])},F:function(){var c=b.firstChild,a=b.getElementsByTagName("iframe")[0];if(!a){a=document.createElement("iframe");a.setAttribute("scrolling","no");a.frameBorder=0;a.setAttribute("src","");b.appendChild(a)}a.style.setAttribute("cssText","position:absolute;z-index:-1;left:"+c.offsetLeft+"px;top:"+c.offsetTop+"px;width:"+c.offsetWidth+"px;height:"+c.offsetHeight+"px;")},X:function(c,d){var b=d==0?c.offsetLeft:c.offsetTop,a=c.offsetParent;while(a!=null){b=d==0?b+a.offsetLeft:b+a.offsetTop;a=a.offsetParent}return b},B:function(){var a=10;if(navigator.appName=="Microsoft Internet Explorer"){var b=navigator.appVersion.indexOf("MSIE"),c=navigator.appVersion.substring(b+5,b+6);a=parseInt(c);if(a<3)a=9}return a},V:function(e,c){for(var b=[],a=2,d=arguments.length;a<d;++a)b.push(arguments[a]);return function(){return e.apply(c,b)}},w:function(c){if(b.parentNode.nodeName.toLowerCase()=="body"){var a=this.n(c);a&&a.appendChild(b)}}};var m=function(){if(k==null){k=new n;p(window,"unload",l.fh)}return k},j=function(f,b,c,g){if(typeof b==="string")b=document.getElementById(b);var e=m();if(f==2)e.w(b);else if(f==3){if(typeof c==="string")c=document.getElementById(c);if(c)c=c.innerHTML;else c="Content container was not found.";f=1}b.position=typeof b.position==="undefined"?a[5]:parseInt(b.position);b.relativeTo=b.relativeTo||a[6];b.maxWidth=b.maxWidth||a[7];b.sticky=typeof b.sticky==="undefined"?a[10]:b.sticky;if(b.overlay){b.sticky=true;e.J()}if(b.autoShowDelay)setTimeout(function(){i=b;f==0?e.h(b,c,g):e.L(b,c,f)},b.autoShowDelay);else{if(b.relativeTo=="mouse")b.onmousemove=q;i=b;f==0?e.h(b,c,g):e.L(b,c,f)}if(b.sticky){if(d!=null)b.onmouseout=function(){clearTimeout(d);d=null}}else b.onmouseout=function(){e.N()};b.duration&&setTimeout(function(){i==b&&e.N()},(b.autoShowDelay||0)+b.duration)};return{hasBeenDisplayed:function(){return k!=null},ajax:function(a,c,b){j(0,a,c,b)},pop:function(a,b){j(1,a,b,null)},add:function(a,b,c){if(c)j(2,a,b,null);else j(3,a,b,null)},hide:function(){var a=m();a.N()},addToPageLoadEvent:function(a){var b=window.onload;if(typeof window.onload!="function")window.onload=a;else window.onload=function(){b();a()}}}}()
