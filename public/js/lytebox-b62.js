Array.prototype.removeDuplicates=function(){
for(var i=1;i<this.length;i++){
if(this[i][0]==this[i-1][0]){
this.splice(i,1);
}
}
};
Array.prototype.empty=function(){
for(var i=0;i<=this.length;i++){
this.shift();
}
};
String.prototype.trim=function(){
return this.replace(/^\s+|\s+$/g,"");
};
function LyteBox(){
this.theme="grey";
this.hideFlash=true;
this.outerBorder=true;
this.resizeSpeed=8;
this.maxOpacity=80;
this.navType=1;
this.autoResize=true;
this.doAnimations=true;
this.borderSize=12;
this.slideInterval=4000;
this.showNavigation=true;
this.showClose=true;
this.showDetails=true;
this.showPlayPause=true;
this.autoEnd=true;
this.pauseOnNextClick=false;
this.pauseOnPrevClick=true;
if(this.resizeSpeed>10){
this.resizeSpeed=10;
}
if(this.resizeSpeed<1){
resizeSpeed=1;
}
this.resizeDuration=(11-this.resizeSpeed)*0.15;
this.resizeWTimerArray=new Array();
this.resizeWTimerCount=0;
this.resizeHTimerArray=new Array();
this.resizeHTimerCount=0;
this.showContentTimerArray=new Array();
this.showContentTimerCount=0;
this.overlayTimerArray=new Array();
this.overlayTimerCount=0;
this.imageTimerArray=new Array();
this.imageTimerCount=0;
this.timerIDArray=new Array();
this.timerIDCount=0;
this.slideshowIDArray=new Array();
this.slideshowIDCount=0;
this.imageArray=new Array();
this.activeImage=null;
this.slideArray=new Array();
this.activeSlide=null;
this.frameArray=new Array();
this.activeFrame=null;
this.checkFrame();
this.isSlideshow=false;
this.isLyteframe=false;
this.ie=false;
this.ie7=(this.ie&&window.XMLHttpRequest);
this.initialize();
}
LyteBox.prototype.initialize=function(){
this.updateLyteboxItems();
var _3=this.doc.getElementsByTagName("body").item(0);
if(this.doc.getElementById("lbOverlay")){
_3.removeChild(this.doc.getElementById("lbOverlay"));
_3.removeChild(this.doc.getElementById("lbMain"));
}
var _4=this.doc.createElement("div");
_4.setAttribute("id","lbOverlay");
_4.setAttribute((this.ie?"className":"class"),this.theme);
if((this.ie&&!this.ie7)||(this.ie7&&this.doc.compatMode=="BackCompat")){
_4.style.position="absolute";
}
_4.style.display="none";
_3.appendChild(_4);
var _5=this.doc.createElement("div");
_5.setAttribute("id","lbMain");
_5.style.display="none";
_3.appendChild(_5);
var _6=this.doc.createElement("div");
_6.setAttribute("id","lbOuterContainer");
_6.setAttribute((this.ie?"className":"class"),this.theme);
_5.appendChild(_6);
var _7=this.doc.createElement("div");
_7.setAttribute("id","lbIframeContainer");
_7.style.display="none";
_6.appendChild(_7);
var _8=this.doc.createElement("iframe");
_8.setAttribute("id","lbIframe");
_8.setAttribute("name","lbIframe");
_8.style.display="none";
_7.appendChild(_8);
var _9=this.doc.createElement("div");
_9.setAttribute("id","lbImageContainer");
_6.appendChild(_9);
var _a=this.doc.createElement("img");
_a.setAttribute("id","lbImage");
_9.appendChild(_a);
var _b=this.doc.createElement("div");
_b.setAttribute("id","lbLoading");
_6.appendChild(_b);
var _c=this.doc.createElement("div");
_c.setAttribute("id","lbDetailsContainer");
_c.setAttribute((this.ie?"className":"class"),this.theme);
_5.appendChild(_c);
var _d=this.doc.createElement("div");
_d.setAttribute("id","lbDetailsData");
_d.setAttribute((this.ie?"className":"class"),this.theme);
_c.appendChild(_d);
var _e=this.doc.createElement("div");
_e.setAttribute("id","lbDetails");
_d.appendChild(_e);
var _f=this.doc.createElement("span");
_f.setAttribute("id","lbCaption");
_e.appendChild(_f);
var _10=this.doc.createElement("div");
_10.setAttribute("id","lbHoverNav");
_9.appendChild(_10);
var _11=this.doc.createElement("div");
_11.setAttribute("id","lbBottomNav");
_d.appendChild(_11);
var _12=this.doc.createElement("a");
_12.setAttribute("id","lbPrev");
_12.setAttribute((this.ie?"className":"class"),this.theme);
_12.setAttribute("href","#");
_10.appendChild(_12);
var _13=this.doc.createElement("a");
_13.setAttribute("id","lbNext");
_13.setAttribute((this.ie?"className":"class"),this.theme);
_13.setAttribute("href","#");
_10.appendChild(_13);
var _14=this.doc.createElement("span");
_14.setAttribute("id","lbNumberDisplay");
_e.appendChild(_14);
var _15=this.doc.createElement("span");
_15.setAttribute("id","lbNavDisplay");
_15.style.display="none";
_e.appendChild(_15);
var _16=this.doc.createElement("a");
_16.setAttribute("id","lbClose");
_16.setAttribute((this.ie?"className":"class"),this.theme);
_16.setAttribute("href","#");
_11.appendChild(_16);
var _17=this.doc.createElement("a");
_17.setAttribute("id","lbPause");
_17.setAttribute((this.ie?"className":"class"),this.theme);
_17.setAttribute("href","#");
_17.style.display="none";
_11.appendChild(_17);
var _18=this.doc.createElement("a");
_18.setAttribute("id","lbPlay");
_18.setAttribute((this.ie?"className":"class"),this.theme);
_18.setAttribute("href","#");
_18.style.display="none";
_11.appendChild(_18);
};
LyteBox.prototype.updateLyteboxItems=function(){
var _19=(this.isFrame)?window.parent.frames[window.name].document.getElementsByTagName("a"):document.getElementsByTagName("a");
for(var i=0;i<_19.length;i++){
var _1b=_19[i];
var _1c=String(_1b.getAttribute("rel"));
if(_1b.getAttribute("href")){
if(_1c.toLowerCase().match("lytebox")){
_1b.onclick=function(){
myLytebox.start(this,false,false);
return false;
};
}else{
if(_1c.toLowerCase().match("lyteshow")){
_1b.onclick=function(){
myLytebox.start(this,true,false);
return false;
};
}else{
if(_1c.toLowerCase().match("lyteframe")){
_1b.onclick=function(){
myLytebox.start(this,false,true);
return false;
};
}
}
}
}
}
};
LyteBox.prototype.start=function(_1d,_1e,_1f){
if(this.ie&&!this.ie7){
this.toggleSelects("hide");
}
if(this.hideFlash){
this.toggleFlash("hide");
}
this.isLyteframe=(_1f?true:false);
var _20=this.getPageSize();
var _21=this.doc.getElementById("lbOverlay");
var _22=this.doc.getElementsByTagName("body").item(0);
_21.style.height=_20[1]+"px";
_21.style.display="";
this.appear("lbOverlay",(this.doAnimations?0:this.maxOpacity));
var _23=(this.isFrame)?window.parent.frames[window.name].document.getElementsByTagName("a"):document.getElementsByTagName("a");
if(this.isLyteframe){
this.frameArray=[];
this.frameNum=0;
if((_1d.getAttribute("rel")=="lyteframe")){
var rev=_1d.getAttribute("rev");
this.frameArray.push(new Array(_1d.getAttribute("href"),_1d.getAttribute("title"),(rev==null||rev==""?"width: 400px; height: 400px; scrolling: auto;":rev)));
}else{
if(_1d.getAttribute("rel").indexOf("lyteframe")!=-1){
for(var i=0;i<_23.length;i++){
var _26=_23[i];
if(_26.getAttribute("href")&&(_26.getAttribute("rel")==_1d.getAttribute("rel"))){
var rev=_26.getAttribute("rev");
this.frameArray.push(new Array(_26.getAttribute("href"),_26.getAttribute("title"),(rev==null||rev==""?"width: 400px; height: 400px; scrolling: auto;":rev)));
}
}
this.frameArray.removeDuplicates();
while(this.frameArray[this.frameNum][0]!=_1d.getAttribute("href")){
this.frameNum++;
}
}
}
}else{
this.imageArray=[];
this.imageNum=0;
this.slideArray=[];
this.slideNum=0;
if((_1d.getAttribute("rel")=="lytebox")){
this.imageArray.push(new Array(_1d.getAttribute("href"),_1d.getAttribute("title")));
}else{
if(_1d.getAttribute("rel").indexOf("lytebox")!=-1){
for(var i=0;i<_23.length;i++){
var _26=_23[i];
if(_26.getAttribute("href")&&(_26.getAttribute("rel")==_1d.getAttribute("rel"))){
this.imageArray.push(new Array(_26.getAttribute("href"),_26.getAttribute("title")));
}
}
this.imageArray.removeDuplicates();
while(this.imageArray[this.imageNum][0]!=_1d.getAttribute("href")){
this.imageNum++;
}
}
if(_1d.getAttribute("rel").indexOf("lyteshow")!=-1){
for(var i=0;i<_23.length;i++){
var _26=_23[i];
if(_26.getAttribute("href")&&(_26.getAttribute("rel")==_1d.getAttribute("rel"))){
this.slideArray.push(new Array(_26.getAttribute("href"),_26.getAttribute("title")));
}
}
this.slideArray.removeDuplicates();
while(this.slideArray[this.slideNum][0]!=_1d.getAttribute("href")){
this.slideNum++;
}
}
}
}
var _27=this.doc.getElementById("lbMain");
_27.style.top=(this.getPageScroll()+(_20[3]/15))+"px";
_27.style.display="";
if(!this.outerBorder){
this.doc.getElementById("lbOuterContainer").style.border="none";
this.doc.getElementById("lbDetailsContainer").style.border="none";
}else{
this.doc.getElementById("lbOuterContainer").style.borderBottom="";
this.doc.getElementById("lbOuterContainer").setAttribute((this.ie?"className":"class"),this.theme);
}
this.doc.getElementById("lbOverlay").onclick=function(){
myLytebox.end();
return false;
};
this.doc.getElementById("lbMain").onclick=function(e){
var e=e;
if(!e){
if(window.parent.frames[window.name]&&(parent.document.getElementsByTagName("frameset").length<=0)){
e=window.parent.window.event;
}else{
e=window.event;
}
}
var id=(e.target?e.target.id:e.srcElement.id);
if(id=="lbMain"){
myLytebox.end();
return false;
}
};
this.doc.getElementById("lbClose").onclick=function(){
myLytebox.end();
return false;
};
this.doc.getElementById("lbPause").onclick=function(){
myLytebox.togglePlayPause("lbPause","lbPlay");
return false;
};
this.doc.getElementById("lbPlay").onclick=function(){
myLytebox.togglePlayPause("lbPlay","lbPause");
return false;
};
this.isSlideshow=_1e;
this.isPaused=(this.slideNum!=0?true:false);
if(this.isSlideshow&&this.showPlayPause&&this.isPaused){
this.doc.getElementById("lbPlay").style.display="";
this.doc.getElementById("lbPause").style.display="none";
}
if(this.isLyteframe){
this.changeContent(this.frameNum);
}else{
if(this.isSlideshow){
this.changeContent(this.slideNum);
}else{
this.changeContent(this.imageNum);
}
}
};
LyteBox.prototype.changeContent=function(_2a){
if(this.isSlideshow){
for(var i=0;i<this.slideshowIDCount;i++){
window.clearTimeout(this.slideshowIDArray[i]);
}
}
this.activeImage=this.activeSlide=this.activeFrame=_2a;
if(!this.outerBorder){
this.doc.getElementById("lbOuterContainer").style.border="none";
this.doc.getElementById("lbDetailsContainer").style.border="none";
}else{
this.doc.getElementById("lbOuterContainer").style.borderBottom="";
this.doc.getElementById("lbOuterContainer").setAttribute((this.ie?"className":"class"),this.theme);
}
this.doc.getElementById("lbLoading").style.display="";
this.doc.getElementById("lbImage").style.display="none";
this.doc.getElementById("lbIframe").style.display="none";
this.doc.getElementById("lbPrev").style.display="none";
this.doc.getElementById("lbNext").style.display="none";
this.doc.getElementById("lbIframeContainer").style.display="none";
this.doc.getElementById("lbDetailsContainer").style.display="none";
this.doc.getElementById("lbNumberDisplay").style.display="none";
if(this.navType==2||this.isLyteframe){
object=this.doc.getElementById("lbNavDisplay");
object.innerHTML="&nbsp;&nbsp;&nbsp;<span id=\"lbPrev2_Off\" style=\"display: none;\" class=\""+this.theme+"\">&laquo; prev</span><a href=\"#\" id=\"lbPrev2\" class=\""+this.theme+"\" style=\"display: none;\">&laquo; prev</a> <b id=\"lbSpacer\" class=\""+this.theme+"\">||</b> <span id=\"lbNext2_Off\" style=\"display: none;\" class=\""+this.theme+"\">next &raquo;</span><a href=\"#\" id=\"lbNext2\" class=\""+this.theme+"\" style=\"display: none;\">next &raquo;</a>";
object.style.display="none";
}
if(this.isLyteframe){
var _2c=myLytebox.doc.getElementById("lbIframe");
var _2d=this.frameArray[this.activeFrame][2];
var _2e=_2d.split(";");
for(var i=0;i<_2e.length;i++){
if(_2e[i].indexOf("width:")>=0){
var w=_2e[i].replace("width:","");
_2c.width=w.trim();
}else{
if(_2e[i].indexOf("height:")>=0){
var h=_2e[i].replace("height:","");
_2c.height=h.trim();
}else{
if(_2e[i].indexOf("scrolling:")>=0){
var s=_2e[i].replace("scrolling:","");
_2c.scrolling=s.trim();
}else{
if(_2e[i].indexOf("border:")>=0){
}
}
}
}
}
this.resizeContainer(parseInt(_2c.width),parseInt(_2c.height));
}else{
imgPreloader=new Image();
imgPreloader.onload=function(){
var _32=imgPreloader.width;
var _33=imgPreloader.height;
if(myLytebox.autoResize){
var _34=myLytebox.getPageSize();
var x=_34[2]-150;
var y=_34[3]-150;
if(_32>x){
_33=Math.round(_33*(x/_32));
_32=x;
if(_33>y){
_32=Math.round(_32*(y/_33));
_33=y;
}
}else{
if(_33>y){
_32=Math.round(_32*(y/_33));
_33=y;
if(_32>x){
_33=Math.round(_33*(x/_32));
_32=x;
}
}
}
}
var _37=myLytebox.doc.getElementById("lbImage");
_37.src=(myLytebox.isSlideshow?myLytebox.slideArray[myLytebox.activeSlide][0]:myLytebox.imageArray[myLytebox.activeImage][0]);
_37.width=_32;
_37.height=_33;
myLytebox.resizeContainer(_32,_33);
imgPreloader.onload=function(){
};
};
imgPreloader.src=(this.isSlideshow?this.slideArray[this.activeSlide][0]:this.imageArray[this.activeImage][0]);
}
};
LyteBox.prototype.resizeContainer=function(_38,_39){
this.wCur=this.doc.getElementById("lbOuterContainer").offsetWidth;
this.hCur=this.doc.getElementById("lbOuterContainer").offsetHeight;
this.xScale=((_38+(this.borderSize*2))/this.wCur)*100;
this.yScale=((_39+(this.borderSize*2))/this.hCur)*100;
var _3a=(this.wCur-this.borderSize*2)-_38;
var _3b=(this.hCur-this.borderSize*2)-_39;
if(!(_3b==0)){
this.hDone=false;
this.resizeH("lbOuterContainer",this.hCur,_39+this.borderSize*2,this.getPixelRate(this.hCur,_39));
}else{
this.hDone=true;
}
if(!(_3a==0)){
this.wDone=false;
this.resizeW("lbOuterContainer",this.wCur,_38+this.borderSize*2,this.getPixelRate(this.wCur,_38));
}else{
this.wDone=true;
}
if((_3b==0)&&(_3a==0)){
if(this.ie){
this.pause(250);
}else{
this.pause(100);
}
}
this.doc.getElementById("lbPrev").style.height=_39+"px";
this.doc.getElementById("lbNext").style.height=_39+"px";
this.doc.getElementById("lbDetailsContainer").style.width=(_38+(this.borderSize*2)+(this.ie&&this.doc.compatMode=="BackCompat"&&this.outerBorder?2:0))+"px";
this.showContent();
};
LyteBox.prototype.showContent=function(){
if(this.wDone&&this.hDone){
for(var i=0;i<this.showContentTimerCount;i++){
window.clearTimeout(this.showContentTimerArray[i]);
}
if(this.outerBorder){
this.doc.getElementById("lbOuterContainer").style.borderBottom="none";
}
this.doc.getElementById("lbLoading").style.display="none";
if(this.isLyteframe){
this.doc.getElementById("lbIframe").style.display="";
this.appear("lbIframe",(this.doAnimations?0:100));
}else{
this.doc.getElementById("lbImage").style.display="";
this.appear("lbImage",(this.doAnimations?0:100));
this.preloadNeighborImages();
}
if(this.isSlideshow){
if(this.activeSlide==(this.slideArray.length-1)){
if(this.autoEnd){
this.slideshowIDArray[this.slideshowIDCount++]=setTimeout("myLytebox.end('slideshow')",this.slideInterval);
}
}else{
if(!this.isPaused){
this.slideshowIDArray[this.slideshowIDCount++]=setTimeout("myLytebox.changeContent("+(this.activeSlide+1)+")",this.slideInterval);
}
}
this.doc.getElementById("lbHoverNav").style.display=(this.showNavigation&&this.navType==1?"":"none");
this.doc.getElementById("lbClose").style.display=(this.showClose?"":"none");
this.doc.getElementById("lbDetails").style.display=(this.showDetails?"":"none");
this.doc.getElementById("lbPause").style.display=(this.showPlayPause&&!this.isPaused?"":"none");
this.doc.getElementById("lbPlay").style.display=(this.showPlayPause&&!this.isPaused?"none":"");
this.doc.getElementById("lbNavDisplay").style.display=(this.showNavigation&&this.navType==2?"":"none");
}else{
this.doc.getElementById("lbHoverNav").style.display=(this.navType==1&&!this.isLyteframe?"":"none");
if((this.navType==2&&!this.isLyteframe&&this.imageArray.length>1)||(this.frameArray.length>1&&this.isLyteframe)){
this.doc.getElementById("lbNavDisplay").style.display="";
}else{
this.doc.getElementById("lbNavDisplay").style.display="none";
}
this.doc.getElementById("lbClose").style.display="";
this.doc.getElementById("lbDetails").style.display="";
this.doc.getElementById("lbPause").style.display="none";
this.doc.getElementById("lbPlay").style.display="none";
}
this.doc.getElementById("lbImageContainer").style.display=(this.isLyteframe?"none":"");
this.doc.getElementById("lbIframeContainer").style.display=(this.isLyteframe?"":"none");
try{
this.doc.getElementById("lbIframe").src=this.frameArray[this.activeFrame][0];
}
catch(e){
}
}else{
this.showContentTimerArray[this.showContentTimerCount++]=setTimeout("myLytebox.showContent()",200);
}
};
LyteBox.prototype.updateDetails=function(){
var _3d=this.doc.getElementById("lbCaption");
var _3e=(this.isSlideshow?this.slideArray[this.activeSlide][1]:(this.isLyteframe?this.frameArray[this.activeFrame][1]:this.imageArray[this.activeImage][1]));
_3d.style.display="";
_3d.innerHTML=(_3e==null?"":_3e);
this.updateNav();
this.doc.getElementById("lbDetailsContainer").style.display="";
_3d=this.doc.getElementById("lbNumberDisplay");
if(this.isSlideshow&&this.slideArray.length>1){
_3d.style.display="";
_3d.innerHTML="Image "+eval(this.activeSlide+1)+" of "+this.slideArray.length;
this.doc.getElementById("lbNavDisplay").style.display=(this.navType==2&&this.showNavigation?"":"none");
}else{
if(this.imageArray.length>1&&!this.isLyteframe){
_3d.style.display="";
_3d.innerHTML="Image "+eval(this.activeImage+1)+" of "+this.imageArray.length;
this.doc.getElementById("lbNavDisplay").style.display=(this.navType==2?"":"none");
}else{
if(this.frameArray.length>1&&this.isLyteframe){
_3d.style.display="";
_3d.innerHTML="Page "+eval(this.activeFrame+1)+" of "+this.frameArray.length;
this.doc.getElementById("lbNavDisplay").style.display="";
}else{
this.doc.getElementById("lbNavDisplay").style.display="none";
}
}
}
this.appear("lbDetailsContainer",(this.doAnimations?0:100));
};
LyteBox.prototype.updateNav=function(){
if(this.isSlideshow){
if(this.activeSlide!=0){
var _3f=(this.navType==2?this.doc.getElementById("lbPrev2"):this.doc.getElementById("lbPrev"));
_3f.style.display="";
_3f.onclick=function(){
if(myLytebox.pauseOnPrevClick){
myLytebox.togglePlayPause("lbPause","lbPlay");
}
myLytebox.changeContent(myLytebox.activeSlide-1);
return false;
};
}else{
if(this.navType==2){
this.doc.getElementById("lbPrev2_Off").style.display="";
}
}
if(this.activeSlide!=(this.slideArray.length-1)){
var _3f=(this.navType==2?this.doc.getElementById("lbNext2"):this.doc.getElementById("lbNext"));
_3f.style.display="";
_3f.onclick=function(){
if(myLytebox.pauseOnNextClick){
myLytebox.togglePlayPause("lbPause","lbPlay");
}
myLytebox.changeContent(myLytebox.activeSlide+1);
return false;
};
}else{
if(this.navType==2){
this.doc.getElementById("lbNext2_Off").style.display="";
}
}
}else{
if(this.isLyteframe){
if(this.activeFrame!=0){
var _3f=this.doc.getElementById("lbPrev2");
_3f.style.display="";
_3f.onclick=function(){
myLytebox.changeContent(myLytebox.activeFrame-1);
return false;
};
}else{
this.doc.getElementById("lbPrev2_Off").style.display="";
}
if(this.activeFrame!=(this.frameArray.length-1)){
var _3f=this.doc.getElementById("lbNext2");
_3f.style.display="";
_3f.onclick=function(){
myLytebox.changeContent(myLytebox.activeFrame+1);
return false;
};
}else{
this.doc.getElementById("lbNext2_Off").style.display="";
}
}else{
if(this.activeImage!=0){
var _3f=(this.navType==2?this.doc.getElementById("lbPrev2"):this.doc.getElementById("lbPrev"));
_3f.style.display="";
_3f.onclick=function(){
myLytebox.changeContent(myLytebox.activeImage-1);
return false;
};
}else{
if(this.navType==2){
this.doc.getElementById("lbPrev2_Off").style.display="";
}
}
if(this.activeImage!=(this.imageArray.length-1)){
var _3f=(this.navType==2?this.doc.getElementById("lbNext2"):this.doc.getElementById("lbNext"));
_3f.style.display="";
_3f.onclick=function(){
myLytebox.changeContent(myLytebox.activeImage+1);
return false;
};
}else{
if(this.navType==2){
this.doc.getElementById("lbNext2_Off").style.display="";
}
}
}
}
this.enableKeyboardNav();
};
LyteBox.prototype.enableKeyboardNav=function(){
document.onkeydown=this.keyboardAction;
};
LyteBox.prototype.disableKeyboardNav=function(){
document.onkeydown="";
};
LyteBox.prototype.keyboardAction=function(e){
var _41=key=escape=null;
_41=(e==null)?event.keyCode:e.which;
key=String.fromCharCode(_41).toLowerCase();
escape=(e==null)?27:e.DOM_VK_ESCAPE;
if((key=="x")||(key=="c")||(_41==escape)){
myLytebox.end();
}else{
if((key=="p")||(_41==37)){
if(myLytebox.isSlideshow){
if(myLytebox.activeSlide!=0){
myLytebox.disableKeyboardNav();
myLytebox.changeContent(myLytebox.activeSlide-1);
}
}else{
if(myLytebox.isLyteframe){
if(myLytebox.activeFrame!=0){
myLytebox.disableKeyboardNav();
myLytebox.changeContent(myLytebox.activeFrame-1);
}
}else{
if(myLytebox.activeImage!=0){
myLytebox.disableKeyboardNav();
myLytebox.changeContent(myLytebox.activeImage-1);
}
}
}
}else{
if((key=="n")||(_41==39)){
if(myLytebox.isSlideshow){
if(myLytebox.activeSlide!=(myLytebox.slideArray.length-1)){
myLytebox.disableKeyboardNav();
myLytebox.changeContent(myLytebox.activeSlide+1);
}
}else{
if(myLytebox.isLyteframe){
if(myLytebox.activeFrame!=(myLytebox.frameArray.length-1)){
myLytebox.disableKeyboardNav();
myLytebox.changeContent(myLytebox.activeFrame+1);
}
}else{
if(myLytebox.activeImage!=(myLytebox.imageArray.length-1)){
myLytebox.disableKeyboardNav();
myLytebox.changeContent(myLytebox.activeImage+1);
}
}
}
}
}
}
};
LyteBox.prototype.preloadNeighborImages=function(){
if(this.isSlideshow){
if((this.slideArray.length-1)>this.activeSlide){
preloadNextImage=new Image();
preloadNextImage.src=this.slideArray[this.activeSlide+1][0];
}
if(this.activeSlide>0){
preloadPrevImage=new Image();
preloadPrevImage.src=this.slideArray[this.activeSlide-1][0];
}
}else{
if((this.imageArray.length-1)>this.activeImage){
preloadNextImage=new Image();
preloadNextImage.src=this.imageArray[this.activeImage+1][0];
}
if(this.activeImage>0){
preloadPrevImage=new Image();
preloadPrevImage.src=this.imageArray[this.activeImage-1][0];
}
}
};
LyteBox.prototype.togglePlayPause=function(_42,_43){
if(this.isSlideshow&&_42=="lbPause"){
for(var i=0;i<this.slideshowIDCount;i++){
window.clearTimeout(this.slideshowIDArray[i]);
}
}
this.doc.getElementById(_42).style.display="none";
this.doc.getElementById(_43).style.display="";
if(_42=="lbPlay"){
this.isPaused=false;
if(this.activeSlide==(this.slideArray.length-1)){
this.end();
}else{
this.changeContent(this.activeSlide+1);
}
}else{
this.isPaused=true;
}
};
LyteBox.prototype.end=function(_45){
var _46=(_45=="slideshow"?false:true);
if(this.isSlideshow&&this.isPaused&&!_46){
return;
}
this.disableKeyboardNav();
this.doc.getElementById("lbMain").style.display="none";
this.fade("lbOverlay",(this.doAnimations?this.maxOpacity:0));
this.toggleSelects("visible");
if(this.hideFlash){
this.toggleFlash("visible");
}
if(this.isSlideshow){
for(var i=0;i<this.slideshowIDCount;i++){
window.clearTimeout(this.slideshowIDArray[i]);
}
}
if(this.isLyteframe){
this.initialize();
}
};
LyteBox.prototype.checkFrame=function(){
if(window.parent.frames[window.name]&&(parent.document.getElementsByTagName("frameset").length<=0)){
this.isFrame=true;
this.lytebox="window.parent."+window.name+".myLytebox";
this.doc=parent.document;
}else{
this.isFrame=false;
this.lytebox="myLytebox";
this.doc=document;
}
};
LyteBox.prototype.getPixelRate=function(cur,img){
var _4a=(img>cur)?img-cur:cur-img;
if(_4a>=0&&_4a<=100){
return 10;
}
if(_4a>100&&_4a<=200){
return 15;
}
if(_4a>200&&_4a<=300){
return 20;
}
if(_4a>300&&_4a<=400){
return 25;
}
if(_4a>400&&_4a<=500){
return 30;
}
if(_4a>500&&_4a<=600){
return 35;
}
if(_4a>600&&_4a<=700){
return 40;
}
if(_4a>700){
return 45;
}
};
LyteBox.prototype.appear=function(id,_4c){
var _4d=this.doc.getElementById(id).style;
_4d.opacity=(_4c/100);
_4d.MozOpacity=(_4c/100);
_4d.KhtmlOpacity=(_4c/100);
_4d.filter="alpha(opacity="+(_4c+10)+")";
if(_4c==100&&(id=="lbImage"||id=="lbIframe")){
try{
_4d.removeAttribute("filter");
}
catch(e){
}
this.updateDetails();
}else{
if(_4c>=this.maxOpacity&&id=="lbOverlay"){
for(var i=0;i<this.overlayTimerCount;i++){
window.clearTimeout(this.overlayTimerArray[i]);
}
return;
}else{
if(_4c>=100&&id=="lbDetailsContainer"){
try{
_4d.removeAttribute("filter");
}
catch(e){
}
for(var i=0;i<this.imageTimerCount;i++){
window.clearTimeout(this.imageTimerArray[i]);
}
this.doc.getElementById("lbOverlay").style.height=this.getPageSize()[1]+"px";
}else{
if(id=="lbOverlay"){
this.overlayTimerArray[this.overlayTimerCount++]=setTimeout("myLytebox.appear('"+id+"', "+(_4c+20)+")",1);
}else{
this.imageTimerArray[this.imageTimerCount++]=setTimeout("myLytebox.appear('"+id+"', "+(_4c+10)+")",1);
}
}
}
}
};
LyteBox.prototype.fade=function(id,_50){
var _51=this.doc.getElementById(id).style;
_51.opacity=(_50/100);
_51.MozOpacity=(_50/100);
_51.KhtmlOpacity=(_50/100);
_51.filter="alpha(opacity="+_50+")";
if(_50<=0){
try{
_51.display="none";
}
catch(err){
}
}else{
if(id=="lbOverlay"){
this.overlayTimerArray[this.overlayTimerCount++]=setTimeout("myLytebox.fade('"+id+"', "+(_50-20)+")",1);
}else{
this.timerIDArray[this.timerIDCount++]=setTimeout("myLytebox.fade('"+id+"', "+(_50-10)+")",1);
}
}
};
LyteBox.prototype.resizeW=function(id,_53,_54,_55,_56){
if(!this.hDone){
this.resizeWTimerArray[this.resizeWTimerCount++]=setTimeout("myLytebox.resizeW('"+id+"', "+_53+", "+_54+", "+_55+")",100);
return;
}
var _57=this.doc.getElementById(id);
var _58=_56?_56:(this.resizeDuration/2);
var _59=(this.doAnimations?_53:_54);
_57.style.width=(_59)+"px";
if(_59<_54){
_59+=(_59+_55>=_54)?(_54-_59):_55;
}else{
if(_59>_54){
_59-=(_59-_55<=_54)?(_59-_54):_55;
}
}
this.resizeWTimerArray[this.resizeWTimerCount++]=setTimeout("myLytebox.resizeW('"+id+"', "+_59+", "+_54+", "+_55+", "+(_58+0.02)+")",_58+0.02);
if(parseInt(_57.style.width)==_54){
this.wDone=true;
for(var i=0;i<this.resizeWTimerCount;i++){
window.clearTimeout(this.resizeWTimerArray[i]);
}
}
};
LyteBox.prototype.resizeH=function(id,_5c,_5d,_5e,_5f){
var _60=_5f?_5f:(this.resizeDuration/2);
var _61=this.doc.getElementById(id);
var _62=(this.doAnimations?_5c:_5d);
_61.style.height=(_62)+"px";
if(_62<_5d){
_62+=(_62+_5e>=_5d)?(_5d-_62):_5e;
}else{
if(_62>_5d){
_62-=(_62-_5e<=_5d)?(_62-_5d):_5e;
}
}
this.resizeHTimerArray[this.resizeHTimerCount++]=setTimeout("myLytebox.resizeH('"+id+"', "+_62+", "+_5d+", "+_5e+", "+(_60+0.02)+")",_60+0.02);
if(parseInt(_61.style.height)==_5d){
this.hDone=true;
for(var i=0;i<this.resizeHTimerCount;i++){
window.clearTimeout(this.resizeHTimerArray[i]);
}
}
};
LyteBox.prototype.getPageScroll=function(){
if(self.pageYOffset){
return this.isFrame?parent.pageYOffset:self.pageYOffset;
}else{
if(this.doc.documentElement&&this.doc.documentElement.scrollTop){
return this.doc.documentElement.scrollTop;
}else{
if(document.body){
return this.doc.body.scrollTop;
}
}
}
};
LyteBox.prototype.getPageSize=function(){
var _64,_65,_66,_67;
if(window.innerHeight&&window.scrollMaxY){
_64=this.doc.scrollWidth;
_65=(this.isFrame?parent.innerHeight:self.innerHeight)+(this.isFrame?parent.scrollMaxY:self.scrollMaxY);
}else{
if(this.doc.body.scrollHeight>this.doc.body.offsetHeight){
_64=this.doc.body.scrollWidth;
_65=this.doc.body.scrollHeight;
}else{
_64=this.doc.getElementsByTagName("html").item(0).offsetWidth;
_65=this.doc.getElementsByTagName("html").item(0).offsetHeight;
_64=(_64<this.doc.body.offsetWidth)?this.doc.body.offsetWidth:_64;
_65=(_65<this.doc.body.offsetHeight)?this.doc.body.offsetHeight:_65;
}
}
if(self.innerHeight){
_66=(this.isFrame)?parent.innerWidth:self.innerWidth;
_67=(this.isFrame)?parent.innerHeight:self.innerHeight;
}else{
if(document.documentElement&&document.documentElement.clientHeight){
_66=this.doc.documentElement.clientWidth;
_67=this.doc.documentElement.clientHeight;
}else{
if(document.body){
_66=this.doc.getElementsByTagName("html").item(0).clientWidth;
_67=this.doc.getElementsByTagName("html").item(0).clientHeight;
_66=(_66==0)?this.doc.body.clientWidth:_66;
_67=(_67==0)?this.doc.body.clientHeight:_67;
}
}
}
var _68=(_65<_67)?_67:_65;
var _69=(_64<_66)?_66:_64;
return new Array(_69,_68,_66,_67);
};
LyteBox.prototype.toggleFlash=function(_6a){
var _6b=this.doc.getElementsByTagName("object");
for(var i=0;i<_6b.length;i++){
_6b[i].style.visibility=(_6a=="hide")?"hidden":"visible";
}
var _6d=this.doc.getElementsByTagName("embed");
for(var i=0;i<_6d.length;i++){
_6d[i].style.visibility=(_6a=="hide")?"hidden":"visible";
}
if(this.isFrame){
for(var i=0;i<parent.frames.length;i++){
try{
_6b=parent.frames[i].window.document.getElementsByTagName("object");
for(var j=0;j<_6b.length;j++){
_6b[j].style.visibility=(_6a=="hide")?"hidden":"visible";
}
}
catch(e){
}
try{
_6d=parent.frames[i].window.document.getElementsByTagName("embed");
for(var j=0;j<_6d.length;j++){
_6d[j].style.visibility=(_6a=="hide")?"hidden":"visible";
}
}
catch(e){
}
}
}
};
LyteBox.prototype.toggleSelects=function(_6f){
var _70=this.doc.getElementsByTagName("select");
for(var i=0;i<_70.length;i++){
_70[i].style.visibility=(_6f=="hide")?"hidden":"visible";
}
if(this.isFrame){
for(var i=0;i<parent.frames.length;i++){
try{
_70=parent.frames[i].window.document.getElementsByTagName("select");
for(var j=0;j<_70.length;j++){
_70[j].style.visibility=(_6f=="hide")?"hidden":"visible";
}
}
catch(e){
}
}
}
};
LyteBox.prototype.pause=function(_73){
var now=new Date();
var _75=now.getTime()+_73;
while(true){
now=new Date();
if(now.getTime()>_75){
return;
}
}
};
if(window.addEventListener){
window.addEventListener("load",initLytebox,false);
}else{
if(window.attachEvent){
window.attachEvent("onload",initLytebox);
}else{
window.onload=function(){
initLytebox();
};
}
}
function initLytebox(){
myLytebox=new LyteBox();
}


