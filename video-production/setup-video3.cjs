/* Separate video-3 pipeline. Earlier production files are read only. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=__dirname,out=path.join(root,'output/video-03'),evidence=path.resolve(root,'../../../Claude and OpenAI docs/Genesis-Knowledge/evidence/tutorial-video-3-20261002');
fs.mkdirSync(out,{recursive:true});fs.mkdirSync(evidence,{recursive:true});
const hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
if(!fs.existsSync(path.join(evidence,'preservation-baseline.json'))){
 const files=fs.readdirSync(root).filter(n=>fs.statSync(path.join(root,n)).isFile()&&!n.includes('video3')).map(n=>path.join(root,n));
 function walk(dir){for(const n of fs.readdirSync(dir)){const f=path.join(dir,n);if(fs.statSync(f).isDirectory())walk(f);else files.push(f)}}
 walk(path.join(root,'output/video-02'));walk(path.resolve(root,'../tutorials/assets'));walk(path.join(root,'assets'));
 files.push(path.join(root,'output/Genesis-Your-First-Five-Minutes.mp4'));
 for(const n of fs.readdirSync('C:/Development-Gen/Publish/youtube videos')){const f=path.join('C:/Development-Gen/Publish/youtube videos',n);if(fs.statSync(f).isFile())files.push(f)}
 fs.writeFileSync(path.join(evidence,'preservation-baseline.json'),JSON.stringify({createdAt:new Date().toISOString(),files:[...new Set(files)].map(f=>({file:f,sha256:hash(f)}))},null,2));
}
for(const stem of ['qa','layout-check','audio','verify','native-frames','review-frames','export-coverage']){
 let code=fs.readFileSync(path.join(root,stem+'-video2.cjs'),'utf8').replaceAll('video2','video3').replaceAll('video-02','video-03').replaceAll('video-2-20261002','video-3-20261002').replaceAll('Genesis-Find-Your-Way-Around','Genesis-Choose-Your-Intelligence').replaceAll('Video 2','Video 3').replaceAll('video 2','video 3');
 if(stem==='verify')code=code.replace('[5,10,16,21,25,34,46,50,61,63]','phoneIndices').replace('[5,10,16,21,25,34,46,50,61,63]','phoneIndices').replace('const browser=await','const phoneIndices=Array.from({length:10},(_,i)=>Math.min(data.scenes.length-1,Math.floor((i+.5)*data.scenes.length/10)));\nconst browser=await');
 if(stem==='qa')code=code.replace("fs.writeFileSync(path.join(evidence,'preflight.json')", "manifest.preservationBaseline='preservation-baseline.json';\nfs.writeFileSync(path.join(evidence,'preflight.json')");
 if(stem==='export-coverage')code=code.replace('all 22 steps','all 30 steps').replace('complete category 1 continuation','complete category 2').replace("'adapt-video3.cjs'", "'setup-video3.cjs'").replace(/,'prepare-capture-video3.cjs','capture-video3.cjs'/,'');
 fs.writeFileSync(path.join(root,stem+'-video3.cjs'),code);
}
// Extra @video2 fixture routing is retained only for existing unchanged assets if needed.
let renderer=fs.readFileSync(path.join(root,'render-video2.cjs'),'utf8').replaceAll('timeline-video2.json','timeline-video3.json').replaceAll('editable video 2','editable video 3').replace("'MAKE YOURSELF AT HOME'","'CHOOSE YOUR INTELLIGENCE'");
const start=renderer.indexOf(' const musicDuration='),end=renderer.indexOf(' const mix=cp.spawnSync',start);
renderer=renderer.slice(0,start)+` const musicDuration=Number(m[1])*3600+Number(m[2])*60+Number(m[3]);
 const {crossfade,repeatStart,trimEnd,fadeIn,fadeOut,rationale}=data.audio;
 const repeatDuration=trimEnd-repeatStart,loopCount=1+Math.max(0,Math.ceil((total-trimEnd)/(repeatDuration-crossfade)));
 const args=['-y','-hide_banner','-i',silent];for(let n=0;n<loopCount;n++)args.push('-i',data.music);args.push('-i',path.join(output,'chapters.ffmeta'));
 const filters=[];for(let n=1;n<=loopCount;n++)filters.push('['+n+':a]atrim=start='+(n===1?0:repeatStart)+':end='+trimEnd+',asetpts=PTS-STARTPTS[a'+n+']');let previous='a1';
 for(let n=2;n<=loopCount;n++){const next='join'+n;filters.push('['+previous+'][a'+n+']acrossfade=d='+crossfade+':c1=qsin:c2=qsin['+next+']');previous=next;}
 filters.push('['+previous+']loudnorm=I=-20:TP=-2:LRA=9,afade=t=in:st=0:d='+fadeIn+',afade=t=out:st='+(total-fadeOut)+':d='+fadeOut+'[a]');
 args.push('-filter_complex',filters.join(';'),'-map','0:v:0','-map','[a]','-map_metadata',String(loopCount+1),'-map_chapters',String(loopCount+1),'-t',String(total),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',final);
 fs.writeFileSync(path.join(output,'audio-plan.json'),JSON.stringify({music:data.music,musicDuration,total,crossfade,repeatStart,trimEnd,repeatDuration,curve:'equal-power qsin',loopCount,bedDuration:trimEnd+(loopCount-1)*(repeatDuration-crossfade),joins:Array.from({length:loopCount-1},(_,i)=>({start:trimEnd-crossfade+i*(repeatDuration-crossfade),end:trimEnd+i*(repeatDuration-crossfade)})),fadeIn,fadeOut,targetLUFS:-20,rationale},null,2));
`+renderer.slice(end);
fs.writeFileSync(path.join(root,'render-video3.cjs'),renderer);
let page=fs.readFileSync(path.join(root,'review-video2.html'),'utf8').replaceAll('video-02','video-03').replaceAll('Genesis-Find-Your-Way-Around','Genesis-Choose-Your-Intelligence').replaceAll('Find your way around Genesis','Choose your intelligence').replaceAll('Video 2','Video 3').replace('30:35','Full category 2').replace('All five remaining lessons','All five lessons');fs.writeFileSync(path.join(root,'review-video3.html'),page);
console.log('Separate pipeline and preservation baseline ready.');
