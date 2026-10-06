/* Produce a separate configuration-aware copy of the approved renderer. Pilot stays byte-identical. */
const fs=require('node:fs'),path=require('node:path');const root=__dirname;
let code=fs.readFileSync(path.join(root,'render.cjs'),'utf8');
code=code.replace("const root=__dirname,assets=path.resolve(root,'../tutorials/assets'),output=path.join(root,'output');fs.mkdirSync(output,{recursive:true});\nconst data=JSON.parse(fs.readFileSync(path.join(root,'timeline.json'),'utf8'));", "const root=__dirname,assets=path.resolve(root,'../tutorials/assets');\nconst data=JSON.parse(fs.readFileSync(path.join(root,'timeline-video2.json'),'utf8'));\nconst output=path.join(root,data.outputFolder);fs.mkdirSync(output,{recursive:true});");
// Windows source can use CRLF. Replacements below are independent of newlines.
if(!code.includes('timeline-video2.json')){code=code.replace("output=path.join(root,'output')","output=path.join(root,'output/video-02')").replace("'timeline.json'","'timeline-video2.json'");}
code=code.replace("const chapters=['MODEL','SETUP','EXTRAS','FIRST MESSAGE','FOLLOW-UP']",'const chapters=data.progressLabels');
code=code.replace("'# Your first five minutes — editable pilot'","'# '+data.title+' — editable video 2'");
code=code.replace("'title=Genesis AI — Your first five minutes'","'title=Genesis AI — '+data.title");
code=code.replace("step:s.chapter,title:s.title","step:s.chapter,lesson:s.lesson,sourceSteps:s.sourceSteps,checkpointSteps:s.checkpointSteps||[],readingWords:s.readingWords,readingSeconds:s.readingSeconds,locateSeconds:s.locateSeconds,title:s.title");
code=code.replace("['Introduction','Give Genesis a brain','Choose your setup','Finish extras later','Try something small','Make the answer useful'][n]",'data.chapters[n]');
code=code.replace("{lesson:'welcome',total,scenes:coverage}","{lessons:data.lessonIds,total,chapters:data.chapters,sourceLessons:data.sourceLessons,scenes:coverage}");
code=code.replace("'Genesis-Your-First-Five-Minutes.mp4'",'data.filename');
code=code.replace("path.join(assets,'screens',name+'.png')","name.startsWith('@video2/')?path.join(root,'assets/screens',name.slice(8)+'.png'):path.join(assets,'screens',name+'.png')");
// Build only the current scene's layers: the complete category must not cache hundreds of full-size canvases.
code=code.replace('const layers=data.scenes.map(makeLayers);','');
code=code.replace('draw(data.scenes[i],layers[i],4,absolute+4);','draw(data.scenes[i],makeLayers(data.scenes[i]),5,absolute+5);');
code=code.replace('for(let i=0;i<data.scenes.length;i++){console.log(`Rendering', 'for(let i=0;i<data.scenes.length;i++){const sceneLayers=makeLayers(data.scenes[i]);console.log(`Rendering');
code=code.replace('draw(data.scenes[i],layers[i],j/FPS,absolute+j/FPS);','draw(data.scenes[i],sceneLayers,j/FPS,absolute+j/FPS);');
// Keep two-line list text comfortably inside the approved 100px cards.
code=code.replace("wrap(c,s.items[i],970,y+27,810,33,C.text,'Genesis');", "const rows=listRows(c,s.items[i]);rows.forEach((row,j)=>txt(c,row,970,y+(100-(rows.length-1)*39.6-40)/2+j*39.6,33,C.text,'Genesis'));");
code=code.replace('function makeLayers(s)', "function listRows(c,text){c.font='33px Genesis';const rows=[];let row='';for(const word of text.split(' ')){const next=row?row+' '+word:word;if(c.measureText(next).width>810&&row){rows.push(row);row=word}else row=next}rows.push(row);return rows;}\nfunction makeLayers(s)");
const mixStart=code.indexOf("const args=['-y','-hide_banner','-i',silent");const mixEnd=code.indexOf('const mix=cp.spawnSync',mixStart);
if(mixStart<0||mixEnd<0)throw Error('Pilot mix block changed');
code=code.slice(0,mixStart)+`const musicInfo=cp.spawnSync(ffmpeg,['-hide_banner','-i',data.music],{encoding:'utf8',windowsHide:true}).stderr;
 const m=/Duration: (\\d+):(\\d+):(\\d+\\.\\d+)/.exec(musicInfo);if(!m)throw Error('Music duration unavailable');
 const musicDuration=Number(m[1])*3600+Number(m[2])*60+Number(m[3]),crossfade=8,repeatStart=7.5,trimEnd=Math.min(238.5,musicDuration),repeatDuration=trimEnd-repeatStart,loopCount=1+Math.max(0,Math.ceil((total-trimEnd)/(repeatDuration-crossfade)));
 const args=['-y','-hide_banner','-i',silent];for(let n=0;n<loopCount;n++)args.push('-i',data.music);args.push('-i',path.join(output,'chapters.ffmeta'));
 let filters=[];for(let n=1;n<=loopCount;n++)filters.push('['+n+':a]atrim=start='+(n===1?0:repeatStart)+':end='+trimEnd+',asetpts=PTS-STARTPTS[a'+n+']');let previous='a1';
 for(let n=2;n<=loopCount;n++){const next='join'+n;filters.push('['+previous+'][a'+n+']acrossfade=d='+crossfade+':c1=qsin:c2=qsin['+next+']');previous=next;}
 filters.push('['+previous+']loudnorm=I=-20:TP=-2:LRA=9,afade=t=in:st=0:d=4,afade=t=out:st='+String(total-7)+':d=7[a]');
 args.push('-filter_complex',filters.join(';'),'-map','0:v:0','-map','[a]','-map_metadata',String(loopCount+1),'-map_chapters',String(loopCount+1),'-t',String(total),'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',final);
 fs.writeFileSync(path.join(output,'audio-plan.json'),JSON.stringify({music:data.music,musicDuration,total,crossfade,repeatStart,trimEnd,repeatDuration,curve:'equal-power qsin',loopCount,bedDuration:trimEnd+(loopCount-1)*(repeatDuration-crossfade),joins:Array.from({length:loopCount-1},(_,i)=>({start:trimEnd-crossfade+i*(repeatDuration-crossfade),end:trimEnd+i*(repeatDuration-crossfade)})),fadeIn:4,fadeOut:7,targetLUFS:-20,rationale:'Source-envelope inspection: retain the first introduction; skip its quiet opening on repeats and avoid the near-silent final tail. Overlap musical sections for eight seconds.'},null,2));
 `+code.slice(mixEnd);
if(code.includes('layers[i]')||code.includes("lesson:'welcome'"))throw Error('Unadapted pilot constant');
fs.writeFileSync(path.join(root,'render-video2.cjs'),code);
const original=fs.readFileSync(path.join(root,'review.html'),'utf8');
const timeline=JSON.parse(fs.readFileSync(path.join(root,'timeline-video2.json'))),seconds=timeline.scenes.reduce((n,s)=>n+s.duration,0),runtime=Math.floor(seconds/60)+':'+String(seconds%60).padStart(2,'0');
let page=original.replaceAll('Your first five minutes','Find your way around Genesis').replace('First lesson · 8:32','Video 2 · '+runtime+' · All five remaining lessons').replaceAll('output/','output/video-02/').replaceAll('Genesis-Your-First-Five-Minutes.mp4','Genesis-Find-Your-Way-Around.mp4').replace("['Intro','1 · Model','2 · Setup','3 · Extras','4 · First message','5 · Follow-up'][s.step]","d.chapters[s.step]");
page=page.replace('First lesson video','Video 2');fs.writeFileSync(path.join(root,'review-video2.html'),page);
console.log('Separate video 2 renderer and review created.');
