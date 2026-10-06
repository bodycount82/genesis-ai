const fs=require('node:fs'),path=require('node:path');const root=__dirname;
let c=fs.readFileSync(path.join(root,'capture-video2.cjs'),'utf8').replaceAll('assets/screens','assets/video5/screens').replaceAll('output/video-02','output/video-05').replaceAll('2026-10-02','2026-10-03');
c=c.replace("await capture('chat-modern');",`await capture('chat-modern');
 for(const name of ['Chat','Work','Autonomy']){const b=await js(\`(()=>{const e=document.querySelector('[aria-label="'+${JSON.stringify('PLACEHOLDER')}+'"]');return null})()\`);}
`);
// Replace only the scripted capture sequence, preserving isolation/build helpers.
const begin=c.indexOf(" await win.loadFile"),end=c.indexOf(" fs.writeFileSync(path.join(out,'../screens.json')",begin);
c=c.slice(0,begin)+`
 await win.loadFile(path.join(run,'index.html'));await ready('!!document.querySelector("#modern-navigation")');await capture('chat-modern');
 for(const name of ['Chat','Work','Autonomy']){const pos=await js(\`(()=>{const r=document.querySelector('[aria-label="'+\${JSON.stringify(name)}+'"]')?.getBoundingClientRect();if(!r)throw Error('Missing mode');return {x:r.x+r.width/2,y:r.y+r.height/2}})()\`);win.webContents.sendInputEvent({type:'mouseMove',x:Math.round(pos.x),y:Math.round(pos.y)});await delay(1000);await capture('hover-'+name.toLowerCase());}
 await js(\`window.demo.store.setState({snapshot:{...window.demo.store.getState().snapshot,mode:'Work',state:'working',status:'Working',loop_running:true,paused:false},feedPlan:[{task:'Read the garden notes',status:'done'},{task:'Draft a watering chart',status:'in_progress'},{task:'Check the chart against the notes',status:'pending'}]})\`);await capture('modern-working');
 await js(\`window.demo.store.setState({snapshot:{...window.demo.store.getState().snapshot,paused:true,loop_running:false,state:'idle',status:'Paused'}})\`);await capture('modern-paused');
 await js(\`window.demo.store.setState({snapshot:{...window.demo.store.getState().snapshot,mode:'Chat',paused:false,loop_running:false}})\`);await click('Plan');await capture('plan-controls');
 const pos=await js(\`(()=>{const e=document.querySelector('button[title="Move down"]');const r=e?.getBoundingClientRect();return r?{x:r.x+5,y:r.y+5}:null})()\`);if(pos){win.webContents.sendInputEvent({type:'mouseMove',x:Math.round(pos.x),y:Math.round(pos.y)});await delay(400);await capture('plan-hover');}
`+c.slice(end);
fs.writeFileSync(path.join(root,'capture-video5.cjs'),c);console.log('Video 5 fixture capture prepared');
