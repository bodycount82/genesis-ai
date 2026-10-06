/* One-time pipeline continuation. Starts verification only after this render finishes. */
const fs=require('fs'),path=require('path'),cp=require('child_process');
const out=path.join(__dirname,'output/video-06');
const delay=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{while(!fs.readFileSync(path.join(out,'render-progress.log'),'utf8').includes('FINISHED ')){if(fs.readFileSync(path.join(out,'render-errors.log'),'utf8').trim())throw Error('Render error; inspect log');await delay(2000);}
for(const [script,label]of [['verify-video6.cjs','verification'],['native-frames-video6.cjs','native-frames']]){const p=cp.spawn(process.execPath,[script],{cwd:__dirname,windowsHide:true,stdio:['ignore',fs.openSync(path.join(out,label+'-progress.log'),'w'),fs.openSync(path.join(out,label+'-errors.log'),'w')]});fs.writeFileSync(path.join(out,label+'-pid.json'),JSON.stringify({pid:p.pid,startedAt:new Date().toISOString(),script}));console.log('Started '+script+' PID '+p.pid);p.on('close',code=>{fs.writeFileSync(path.join(out,label+'-exit.json'),JSON.stringify({code,finishedAt:new Date().toISOString()}));console.log(script+' exited '+code);});}
})().catch(e=>{console.error(e);process.exitCode=1});
