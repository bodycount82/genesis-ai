/* Cache settled foregrounds for the current scene, preserving every animated frame. */
const fs=require('fs'),path=require('path');const f=path.join(__dirname,'render-video6.cjs');let c=fs.readFileSync(f,'utf8');if(c.includes('recordingForeground'))throw Error('Already optimized');
const begin=c.indexOf('function draw(s,l,t,absolute){'),logo=c.indexOf(' ctx.drawImage(logo',begin),background=c.slice(begin+'function draw(s,l,t,absolute){'.length,logo);
c=c.slice(0,begin)+'let recordingForeground=false;\nfunction drawOriginal(s,l,t,absolute){if(!recordingForeground){'+background+'}'+c.slice(logo);
c=c.replace(" ctx.fillStyle='#ffffff20';ctx.fillRect(96,1024,1728,3);ctx.fillStyle=C.gold;ctx.fillRect(96,1024,1728*absolute/total,3);"," if(!recordingForeground){ctx.fillStyle='#ffffff20';ctx.fillRect(96,1024,1728,3);ctx.fillStyle=C.gold;ctx.fillRect(96,1024,1728*absolute/total,3);}");
c=c.replace(' txt(ctx,`${String(Math.floor(absolute/60))',' if(!recordingForeground)txt(ctx,`${String(Math.floor(absolute/60))');
const at=c.indexOf('async function init()');c=c.slice(0,at)+`function draw(s,l,t,absolute){
 if(t<4.5){drawOriginal(s,l,t,absolute);return}
 if(!l.settledForeground){ctx.clearRect(0,0,W,H);recordingForeground=true;drawOriginal(s,l,5,0);recordingForeground=false;l.settledForeground=createCanvas(W,H);l.settledForeground.getContext('2d').drawImage(canvas,0,0)}
 ${background}
 ctx.drawImage(l.settledForeground,0,0);
 ctx.fillStyle='#ffffff20';ctx.fillRect(96,1024,1728,3);ctx.fillStyle=C.gold;ctx.fillRect(96,1024,1728*absolute/total,3);
 txt(ctx,\`\$\{String(Math.floor(absolute/60)).padStart(2,'0')\}:\$\{String(Math.floor(absolute%60)).padStart(2,'0')\} / \$\{Math.floor(total/60)\}:\$\{String(total%60).padStart(2,'0')\}\`,1600,1040,17,C.muted);
 if(t>s.duration-.55){ctx.fillStyle=\`rgba(12,14,22,\$\{ease((t-(s.duration-.55))/.55)\})\`;ctx.fillRect(0,160,W,820)}
}
`+c.slice(at);fs.writeFileSync(f,c);console.log('Current-scene settled layers cached; motion, progress and fades still rendered at 30fps');
