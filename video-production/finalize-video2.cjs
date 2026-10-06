/* Deliver only the verified, visually reviewed master. Never overwrite a different owner file. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=__dirname,evidence=path.resolve(root,'../../../Claude and OpenAI docs/Genesis-Knowledge/evidence/tutorial-video-2-20261002');
const master=path.join(root,'output/video-02/Genesis-Find-Your-Way-Around.mp4');
const destination='C:/Development-Gen/Publish/youtube videos/02 - Genesis - Find Your Way Around.mp4';
const pilotDelivery='C:/Development-Gen/Publish/youtube videos/01 - Genesis - Your First Five Minutes.mp4';
const read=n=>JSON.parse(fs.readFileSync(path.join(evidence,n))),hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const verification=read('verification.json'),audio=read('audio-analysis.json'),native=read('native-frame-map.json'),visual=read('visual-review.json'),layout=read('layout-check.json');
const pilotExpected=read('preflight.json').files['output/Genesis-Your-First-Five-Minutes.mp4'];
if(hash(pilotDelivery)!==pilotExpected)throw Error('Delivered video 1 preservation mismatch.');
const sha256=hash(master);
if(verification.videoSha256!==sha256||native.videoSha256!==sha256||visual.videoSha256!==sha256||audio.videoSha256!==sha256)throw Error('Evidence does not belong to this exact master.');
if(verification.decode.exitCode!==0||verification.sceneFrames!==68||verification.transitionFrames!==134||verification.phoneFrames!==20||!verification.normalSpeedPlayback.finishedAt)throw Error('Playback/decoding coverage incomplete.');
if(verification.info.duration!==1835||verification.info.width!==1920||verification.info.height!==1080||verification.normalSpeedPlayback.muted||verification.normalSpeedPlayback.playbackRate!==1||verification.normalSpeedPlayback.audioDecodedBytes<=0||verification.normalSpeedPlayback.quality.corruptedVideoFrames>0||verification.normalSpeedPlayback.events.some(e=>['error','stalled'].includes(e.event)))throw Error('Media/playback quality gate failed.');
if(layout.errors.length||visual.beatFramesInspected!==68||visual.cutFramesInspected!==134||visual.phoneFramesInspected!==20||visual.issues.length)throw Error('Visual/layout review incomplete.');
if(verification.pilotPreservation.some(p=>!p.unchanged)||verification.sourceHashes.some(p=>!p.match))throw Error('Preservation check failed.');
for(const p of verification.pilotPreservation)if(hash(path.join(root,p.name))!==p.sha256)throw Error('Pilot changed after playback began: '+p.name);
if(hash('C:/Development-Gen/songs/video 2 song.mp3')!==read('preflight.json').songSha256)throw Error('Selected soundtrack changed.');
const catalog=JSON.parse(fs.readFileSync(path.resolve(root,'../tutorials/assets/screens.json'))),originals=read('all-original-screen-hashes.json');
for(const p of originals)if(hash(path.resolve(root,'../tutorials/assets/screens',catalog.screens[p.name].file))!==p.expected)throw Error('Original screenshot changed: '+p.name);
for(const p of verification.sourceHashes){const extra=p.name.startsWith('@video2/'),name=extra?p.name.slice(8):p.name,candidate=extra?path.join(root,'assets/screens',name+'.png'):path.resolve(root,'../tutorials/assets/screens',name+'.png');if(hash(candidate)!==p.sha256)throw Error('Used screenshot changed after playback began: '+p.name);}
if(audio.interiorSilentBlocks!==0||audio.duration<1834.95||audio.joins.length!==8)throw Error('Audio coverage/join analysis incomplete.');
fs.mkdirSync(path.dirname(destination),{recursive:true});
if(fs.existsSync(destination)){if(hash(destination)!==sha256)throw Error('A different delivered file already exists; preserve it.');}
else fs.copyFileSync(master,destination,fs.constants.COPYFILE_EXCL);
const deliveredSha256=hash(destination);if(deliveredSha256!==sha256)throw Error('Delivery copy hash mismatch.');
const result={date:'2026-10-02',deliveredAt:new Date().toISOString(),master,destination,sha256,deliveredSha256,fileBytes:fs.statSync(destination).size,duration:verification.info.duration,width:verification.info.width,height:verification.info.height,video1DeliveredSha256:pilotExpected,video1Preserved:true,ownerReview:'pending',uploaded:false};
fs.writeFileSync(path.join(evidence,'delivery.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
