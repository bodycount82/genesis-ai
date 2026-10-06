/* Deliver a fully verified video-4 master, without overwriting any owner file. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');const root=__dirname,out=path.join(root,'output/video-04'),evidence=path.resolve(root,'../../../Claude and OpenAI docs/Genesis-Knowledge/evidence/tutorial-video-4-20261002');
const data=JSON.parse(fs.readFileSync(path.join(root,'timeline-video4.json'))),master=path.join(out,data.filename),destination='C:/Development-Gen/Publish/youtube videos/04 - Genesis - Speak Listen See.mp4';
const read=n=>JSON.parse(fs.readFileSync(path.join(evidence,n))),hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const v=read('verification.json'),a=read('audio-analysis.json'),native=read('native-frame-map.json'),visual=read('visual-review.json'),container=read('container-validation.json'),layout=read('layout-check.json'),pre=read('preflight.json'),baseline=read('preservation-baseline.json'),sha256=hash(master),total=data.scenes.reduce((n,s)=>n+s.duration,0),count=data.scenes.length;
if([v.videoSha256,a.videoSha256,native.videoSha256,visual.videoSha256,container.videoSha256].some(h=>h!==sha256))throw Error('Evidence does not belong to this master');
if(!container.faststart||container.chapters.length!==8)throw Error('Faststart/chapter verification incomplete');
if(v.decode.exitCode!==0||v.sceneFrames!==count||v.transitionFrames!==(count-1)*2||v.phoneFrames!==20||!v.normalSpeedPlayback.finishedAt)throw Error('Decode/playback coverage incomplete');
if(!v.normalSpeedPlayback.startedAt||v.normalSpeedPlayback.samples.length<total/6||v.normalSpeedPlayback.events.some(e=>e.event==='seeking'))throw Error('Complete uninterrupted normal-speed playback required');
const p=v.normalSpeedPlayback;if(v.info.duration!==total||v.info.width!==1920||v.info.height!==1080||p.muted||p.playbackRate!==1||p.audioDecodedBytes<=0||p.quality.corruptedVideoFrames>0||p.events.some(e=>['error','stalled'].includes(e.event)))throw Error('Media/playback gate failed');
if(layout.errors.length||visual.beatFramesInspected!==count||visual.cutFramesInspected!==(count-1)*2||visual.phoneFramesInspected!==20||visual.issues.length)throw Error('Visual review incomplete');
if(a.interiorSilentBlocks!==0||a.duration<total-.05||a.joins.length!==JSON.parse(fs.readFileSync(path.join(out,'audio-plan.json'))).joins.filter(j=>j.start<total).length)throw Error('Audio gate failed');
if(pre.exactSourceText.length!==37||pre.exactSourceText.some(s=>!s.teaching||!s.tip||!s.checkpoint))throw Error('Incomplete source teaching');
for(const b of baseline.files)if(hash(b.file)!==b.sha256)throw Error('Earlier artifact changed: '+b.file);
if(hash(data.music)!==pre.songSha256)throw Error('Song changed');
if(fs.existsSync(destination)){if(hash(destination)!==sha256)throw Error('Different delivered file exists; preserve it')}else fs.copyFileSync(master,destination,fs.constants.COPYFILE_EXCL);
if(hash(destination)!==sha256)throw Error('Delivery hash mismatch');
const result={date:'2026-10-02',deliveredAt:new Date().toISOString(),master,destination,sha256,deliveredSha256:hash(destination),fileBytes:fs.statSync(destination).size,duration:total,width:1920,height:1080,fps:30,steps:37,lessons:data.lessonIds,preservedFiles:baseline.files.length,ownerReview:'pending',uploaded:false};fs.writeFileSync(path.join(evidence,'delivery.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
