const fs=require('node:fs'),path=require('node:path');const root=__dirname;
let c=fs.readFileSync(path.join(root,'capture-video2.cjs'),'utf8');
c=c.slice(0,c.indexOf(" await win.loadFile(path.join(run,'index.html'))"));
c=c.replace("'assets/screens'","'assets/video4/screens'").replaceAll('output/video-02','output/video-04');
c=c.replace("appshotsEnabled:false","appshotsEnabled:true").replace("appshotsStatus:'disabled'","appshotsStatus:'ready'");
c+=`
 await win.loadFile(path.join(run,'index.html'));await ready('!!document.querySelector("#modern-navigation")');
 win.webContents.sendInputEvent({type:'mouseMove',x:650,y:185});await delay(160);await capture('chat-read-aloud');
 await settings('computer:appshots');await capture('appshots-ready');
 await settings('voice');await reveal('Voice');await capture('voice-chooser');
 await js(\`window.demo.store.setState({view:'chat',pendingAttachments:[{id:'example-shot',name:'Appshot-Tutorial.png',size:24000,type:'image/png',path:'tutorial-example/Appshot-Tutorial.png',rel_path:'Appshot-Tutorial.png',is_image:true,is_archive:false,extracted:[]}]})\`);await delay(500);
 await js(\`(()=>{const e=document.querySelector('textarea');Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(e,'Explain this error message.');e.dispatchEvent(new Event('input',{bubbles:true}));})()\`);
 await capture('appshot-draft');
 await js(\`window.demo.store.setState({pendingAttachments:[]})\`);
 await js(\`window.demo.voice.setState({focused:true,transcriptOpen:true,controls:{state:'listening',canStart:true,micMuted:false,muted:false,levels:()=>({input:0.15,output:0}),stop:()=>{},mute:()=>{},muteMic:()=>{},toggle:()=>{},interrupt:()=>{}}})\`);await delay(120);await capture('orb-transcript');
 fs.writeFileSync(path.join(out,'../screens.json'),JSON.stringify(manifest,null,2));win.destroy();app.quit();
}).catch(error=>{console.error(error.stack);app.exit(1)});
`;
fs.writeFileSync(path.join(root,'capture-video4.cjs'),c);
