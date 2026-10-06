/* One-time isolated video-4 initializer. Earlier productions are read-only. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=__dirname,out=path.join(root,'output/video-04'),evidence=path.resolve(root,'../../../Claude and OpenAI docs/Genesis-Knowledge/evidence/tutorial-video-4-20261002');
fs.mkdirSync(out,{recursive:true});fs.mkdirSync(evidence,{recursive:true});
function hash(f){const h=crypto.createHash('sha256'),fd=fs.openSync(f,'r'),b=Buffer.alloc(1024*1024);try{let n;while((n=fs.readSync(fd,b,0,b.length,null)))h.update(b.subarray(0,n));}finally{fs.closeSync(fd)}return h.digest('hex')}
if(!fs.existsSync(path.join(evidence,'preservation-baseline.json'))){
 const files=[];function walk(dir,filter=()=>true){for(const n of fs.readdirSync(dir)){const f=path.join(dir,n);if(fs.statSync(f).isDirectory())walk(f,filter);else if(filter(f))files.push(f)}}
 for(const n of fs.readdirSync(root)){const f=path.join(root,n);if(fs.statSync(f).isFile()&&!n.includes('video4'))files.push(f)}
 for(const d of ['output/video-02','output/video-03','assets'])walk(path.join(root,d));
 walk(path.resolve(root,'../tutorials/assets'));files.push(path.join(root,'output/Genesis-Your-First-Five-Minutes.mp4'));
 walk('C:/Development-Gen/Publish/youtube videos');
 fs.writeFileSync(path.join(evidence,'preservation-baseline.json'),JSON.stringify({createdAt:new Date().toISOString(),files:[...new Set(files)].map(file=>({file,sha256:hash(file)}))},null,2));
}
for(const stem of ['qa','layout-check','audio','native-frames','review-frames','export-coverage','render']){
 let code=fs.readFileSync(path.join(root,stem+'-video3.cjs'),'utf8').replaceAll('video3','video4').replaceAll('video-03','video-04').replaceAll('video-3-20261002','video-4-20261002').replaceAll('Genesis-Choose-Your-Intelligence','Genesis-Speak-Listen-See').replaceAll('Video 3','Video 4').replaceAll('video 3','video 4');
 if(stem==='render')code=code.replaceAll('CHOOSE YOUR INTELLIGENCE','SPEAK. LISTEN. SEE.').replace('for(let i=0;i<5;i++){const x=102+i*348','for(let i=0;i<data.progressLabels.length;i++){const x=102+i*(1728/data.progressLabels.length)');
 if(stem==='export-coverage')code=code.replaceAll('all 30 steps','all 37 steps').replaceAll('complete category 2','complete category 3').replace("'verify-video4-resume.cjs',",'').replace("'final-record-video4.cjs',",'').replace("'run-native-video4-review.ps1',",'');
 if(fs.existsSync(path.join(root,stem+'-video4.cjs')))throw Error('Already initialized: '+stem);
 fs.writeFileSync(path.join(root,stem+'-video4.cjs'),code);
}
console.log('Isolated video-4 pipeline and preservation baseline created.');
