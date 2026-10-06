/* Complete category 3. Source sentences, prerequisites, tips and checkpoints retained. */
const fs=require('node:fs'),path=require('node:path');const root=__dirname;
const catalog=JSON.parse(fs.readFileSync(path.resolve(root,'../tutorials/assets/scenes.json')));
const ids=['dictation','whisper','voices','cloud-voice','orb','vision','appshots'],lessons=ids.map(id=>catalog.lessons.find(l=>l.id===id));
if(JSON.stringify(catalog.lessons.filter(l=>l.group==='senses').sort((a,b)=>a.coursePosition-b.coursePosition).map(l=>l.id))!==JSON.stringify(ids))throw Error('Category order changed');
const labels=['DICTATION','WHISPER','VOICES','CLOUD VOICE','ORB','VISION','APPSHOTS'];
const scenes=[];let chapter=0,lesson=null,step=null;
function add(kind,title,fields={},duration=24){const s={chapter,lesson:lesson?.id||null,sourceSteps:step?[step]:[],duration,kind,eyebrow:chapter?`${String(chapter).padStart(2,'0')} / ${labels[chapter-1]}${step?' · STEP '+step:''}`:'GENESIS AI · CATEGORY 3',title,...fields};scenes.push(s);return s;}
function list(title,items,note='',duration=26){return add('list',title,{items,note},duration)}
function compare(title,left,right,note=''){return add('compare',title,{cards:[{title:left[0],body:left[1],tag:left[2]||''},{title:right[0],body:right[1],tag:right[2]||''}],note},31)}
function shot(title,body,g,note=''){return add('screen',title,{body,...g,note,contextZoom:false},26)}
const {createCanvas,GlobalFonts}=require('C:/Users/damir/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');GlobalFonts.registerFromPath('C:/Windows/Fonts/segoeui.ttf','Genesis');const measure=createCanvas(10,10).getContext('2d');
function chunks(text,max=37){const width=max===37?678:810,size=max===37?40:33,allowed=max===37?5:2;measure.font=size+'px Genesis';
 const rows=t=>{let count=1,row='';for(const word of t.split(/\s+/)){const next=row?row+' '+word:word;if(measure.measureText(next).width>width&&row){count++;row=word}else row=next}return count;};
 const sentences=text.split(/(?<=[.!?])\s+/);let out=[],current='';
 for(let sentence of sentences){sentence=sentence.trim();if(!sentence)continue;if(rows(sentence)>allowed){if(current){out.push(current);current='';}let part='';for(const word of sentence.split(/\s+/)){const next=(part+' '+word).trim();if(rows(next)>allowed&&part){out.push(part);part=word;}else part=next;}if(part)out.push(part);}else if(rows((current+' '+sentence).trim())>allowed){if(current)out.push(current);current=sentence;}else current=(current+' '+sentence).trim();}if(current)out.push(current);return out;}
const titles={
 dictation:['Turn on\nvoice features','Speak into\nyour draft','An ongoing\nconversation','Hear an\nexisting reply'],
 whisper:['Recognition\nis the listener','Choose your\nlanguages','Choose, download,\nthen save','Read what\nis running','Start with\nAutomatic','Try a\nshort sentence'],
 voices:['Choose the\nspeaking engine','Choose an\ninstalled voice','Download a\nPiper voice','Choose when\nit speaks','Effect or\nseparate engine?','Get local\nspeech back'],
 'cloud-voice':['Mix listening\nand speaking','Choose cloud\nrecognition','Match the\ncloud voice','Save, then\ntest briefly'],
 orb:['Open the\norb conversation','Read the\nstate beneath it','Reveal the\ncontrols','Interrupt\na spoken reply','Read along\nand reveal panels','End the\nsession deliberately'],
 vision:['One helper\nlooks at the image','Save a real\nimage model','Choose your\nvision helper','Choose the\nimage route','Check the route.\nTry a picture.','Check the\nhelper’s description','Reading and\ncontrol differ'],
 appshots:['Enable\nAppshots','Show the\nforeground window','Inspect, explain,\nthen Send','Check before\nyou share']};
function geometry(s){let screen=path.basename(s.screenshot,'.png'),crop,highlight,callout=s.anchor.label;const row=(y,h=70)=>{crop=[265,y-20,765,h+40];highlight=[280,y,738,h]};
 if(screen==='voice-local'){
  if(lesson.id==='dictation'){crop=[265,265,765,130];highlight=[972,330,40,24];callout='Enable voice features';}
  else if(lesson.id==='cloud-voice'||step===1){row(438,50);callout='Speech-to-text: choose the listening engine';}
  else if(step===2){row(490,58);callout='Languages you speak: Add a language';}
  else if(step===3||step===4){row(566,94);callout=step===3?'Model choice, download and actual running size':'In use now: base in this demonstration';}
  else if(step===5){row(674,78);callout='Automatic device and Running on';}
  else {row(371,62);callout='Voice resources: Auto · save memory';}
 }
 if(screen==='voice-speaker'){
  const y=step===2&&lesson.id==='voices'?260:step===3&&lesson.id==='voices'?292:step===4||lesson.id==='dictation'?405:step===5?459:208;
  row(y,step===2||step===3?85:67);
  if(lesson.id==='voices'&&step===2){highlight=[758,260,254,41];callout='Voice: installed Amy · English (US)';}
  if(lesson.id==='voices'&&step===3){highlight=[758,308,256,33];callout='Select a catalog voice, then Download';}
  if(lesson.id==='voices'&&step===5)callout='Voice effect: separate from the HAL sidecar engine';
 }
 if(screen==='voice-cloud-listen'){row(535,70);callout='STT API key: separate listening credential';}
 if(screen==='voice-cloud-speak'){
  if(step===4){crop=[1120,70,470,155];highlight=[1460,101,116,30];callout='Save changes';}
  else {crop=[265,195,765,218];highlight=[280,330,738,68];callout='Matching TTS engine, voice and key';}
 }
 if(screen==='chat-modern'){
  if(lesson.id==='dictation'&&step===2){crop=[1060,870,435,88];highlight=[1365.5,908.5,27,27];callout='Microphone: editable draft, then Send';}
  else if(lesson.id==='appshots'){screen='@video4/appshot-draft';crop=[365,770,1115,190];highlight=[371,800,1098,148];callout='Staged attachment and question: press Send';}
  else {crop=[8,905,232,94];highlight=[189.5,956,37,34];callout='Circle beside Voice: ongoing orb conversation';}
 }
 if(screen==='voice-orb'){
  if(step===6){crop=[0,0,260,170];highlight=[18,16,38,30];callout='Exit voice conversation · Escape also exits';}
  else if(step===5){screen='@video4/orb-transcript';crop=[0,10,480,270];highlight=[10,111,453,69];callout='Transcript: read the conversation alongside the orb';}
  else {crop=[570,315,470,430];highlight=step===3?[759,620,85,29]:[688,348,224,224];callout=step===3?'Microphone mute and speaker mute are separate':step===2?'Read the state text beneath the orb':'Tap the orb while thinking or speaking';}
 }
 if(screen==='vision'){
  if(step===5){crop=[265,510,765,128];highlight=[279,529,734,84];callout='Effective route: first-use verification status';}
  else if(step===7){crop=[265,220,765,188];highlight=[279,230,738,167];callout='Set-of-Marks targets and OCR engine';}
  else {crop=[265,400,765,130];highlight=step===4?[754,413.5,260,35]:[726,474.5,288,35];callout=step===4?'Vision routing: Auto, secondary, disabled or legacy':'Secondary vision model: choose a tested preset';}
 }
 if(screen==='model-new'){crop=[518,500,562,156];highlight=[532,584,345,20];callout='Image input: declare a real capability';}
 if(screen==='appshots'){
  screen='@video4/appshots-ready';
  if(step===1){screen='@video4/appshots-ready';crop=[265,445,765,272];highlight=[280,465,738,232];callout='Enable Appshots · Shortcut ready';}
  else if(step===2){crop=[265,505,765,75];highlight=[280,525,738,45];callout='Left Alt + Right Alt · release both keys';}
  else {crop=[265,560,765,88];highlight=[280,575,738,54];callout='Destination: your current conversation draft';}
 }
 if(!crop||!highlight)throw Error('Missing geometry: '+lesson.id+'/'+step);return {screen,crop,highlight,callout};
}
const practice={
 dictation:[
 ['Set up\nthe three parts',['Listening: Whisper turns your audio into text','Answering: your connected language model','Speaking: Piper reads the answer aloud','Save changes after enabling voice'],'You can change the listening or speaking engine while keeping the same main model.'],
 ['A name and\na number',['Say: “Remind me to call Mira at 16:30.”','Stop the recording with the microphone control','Check Mira and 16:30 in the draft','Correct any mistake, then press Send'],'This is a practice sentence. Recognition can make mistakes; editable text gives you control before sending.'],
 ['Draft or\nconversation?',['Dictation fills your editable message draft','You review it and press Send','Orb conversation sends spoken turns as it proceeds','Mute or end the session to stop listening'],'Choose dictation for a precise name or number. Choose conversation when you want an ongoing exchange.'],
 ['Start with\none short reply',['Find Read aloud on an existing reply','Play it to test the installed voice','Open Voice & Vision → Autonomous speech','Choose On request only for deliberate playback'],'Read-aloud plays existing text. Changing spontaneous speech does not turn the microphone on.']
 ],
 whisper:[
 ['One sentence,\nthree stages',['You say: “Water the basil on Friday.”','Whisper recognises those words','Your language model decides how to answer','The selected speaking engine reads the reply'],'Better recognition does not give the answering model new knowledge. Test the recognised text itself.'],
 ['Use your\nactual languages',['Add English if that is what you speak','Add Slovenian if you also use it','Keep only the languages you actually need','One installed Whisper model covers the list'],'These are examples. Choose your own languages; an empty list allows recognition to consider any language.'],
 ['A download\nis a real action',['Example: Automatic recommends small','The picture shows small is not yet installed','Download, wait for completion, then save','Resume a dropped download before testing'],'The displayed 462 MB is a fixture value. A selected model name does not prove its files finished downloading.'],
 ['Chosen, installed,\nand active',['Chosen: Automatic, recommending small','Installed in the example: bundled base','In use now: base','Install the intended size and check memory'],'This demonstration explains the status. If the larger size does not fit free memory, an installed smaller size can run.'],
 ['Read the\nactive device',['Begin with Whisper device → Automatic','Running on may say processor','A local AI model can need the graphics memory','Download optional NVIDIA libraries only if wanted'],'CPU recognition remains valid. Selecting a graphics device does not install its libraries or create more free memory.'],
 ['Compare\none change',['Say: “Mira needs 12 pots on Friday.”','Read the names and numbers in the draft','Reduce noise and check the selected languages','Compare one installed recognition size at a time'],'Auto · save memory unloads idle engines. First use can load them again; an active voice session is protected.']
 ],
 voices:[
 ['Match engine\nand voice',['Piper: locally installed neural voice files','Windows: installed system voices','Browser: available browser voices','Each engine has its own voice choices'],'A voice ID from another engine may not work. Pick the engine first, then its supported voice.'],
 ['Start with\nbundled Amy',['Choose Piper as the speaking engine','Choose Amy · English (US)','Save changes and play one short reply','Custom accepts an existing name or ID'],'Custom does not synthesise a new voice identity or download missing files. Choose a voice for the spoken language.'],
 ['A catalog\ndownload example',['Choose a wanted entry in Download a voice…','Press Download and wait for success','The downloaded voice becomes selected','Save changes and play a short reply'],'Ryan is one example catalog entry. Use a voice available in your current catalog; this fixture performs no download.'],
 ['Choose your\nspeech rhythm',['On request only: ask or play explicitly','Urgent / important: selected spontaneous speech','Everything: natural pacing','Mute and exit belong to the ongoing session'],'Spontaneous speech and microphone listening are different decisions. Check both when you want quiet.'],
 ['Two HAL\nchoices',['HAL 9000 effect processes a local voice','The setup action selects an effect and voice','Save after the local voice setup completes','Real voice (clone, sidecar) needs its own service'],'A pitch, pace and reverb effect is different from the separate HAL voice engine. Choose the one you intend.'],
 ['Recover\nlocal speech',['Check the selected Piper voice is installed','Bundled Amy can replace a missing Piper voice','Local fallback can use Windows, then browser','Check status, mute and one short read-aloud test'],'An unavailable cloud or sidecar engine needs its own configuration checked. Local fallback does not silently enable paid cloud.']
 ],
 'cloud-voice':[
 ['Choose where\neach part goes',['Local recognition + cloud speech is possible','Cloud recognition + local speech is possible','Your main language model can remain local','Cloud listening receives audio; speech receives text'],'Keep track of each selected route. A local main model does not make an explicitly chosen cloud voice local.'],
 ['A separate\nlistening key',['Choose OpenAI STT (cloud)','Enter the matching key in STT API key','Save changes, then try one short recording','Check recognised text before a long exchange'],'Use your own credential only in Genesis. This tutorial contains no real key; local Whisper controls do not tune cloud STT.'],
 ['Keep the\nvoice details together',['Choose OpenAI, ElevenLabs or Azure','Use that provider’s TTS credential','Choose its supported voice or known voice ID','Check any provider-specific setup requirements'],'Azure may require region and voice details beyond an example key. The screenshot illustrates OpenAI only.'],
 ['A ten-word\ntest first',['Save the matching engine, credential and voice','Play one short existing reply','Check internet, access and voice ID if silent','Check the provider’s quota and billing'],'A saved setting does not prove the provider accepted the request. Hear a small test before starting a long conversation.']
 ],
 orb:[
 ['Prepare an\nongoing session',['Use the Modern interface','Check your model connection','Test listening and speaking first','Clear or send your draft before opening the circle'],'Spoken turns submit as the session proceeds. Dictation’s review-and-Send behavior is a different mode.'],
 ['Let the\nstate guide you',['Opening microphone: audio is starting','Listening: it can hear your words','Waiting for your next words: gathering a turn','Transcribing, Thinking, Speaking: processing stages'],'A brief pause can gather more words. Check the state before assuming the conversation has stopped.'],
 ['Two independent\nmute controls',['Move the pointer to reveal controls','Microphone mute stops listening','Speaker mute stops audible output','Reveal transcript and browser with the chevrons'],'Mute the microphone when you want privacy from listening. Speaker mute alone does not stop microphone input.'],
 ['An interruption\nexample',['It begins an answer about your garden','Tap the orb while thinking or speaking','If the microphone is muted, unmute to speak','Say: “Use only the sunny windowsill.”'],'Interrupting the voice reply preserves the microphone’s mute state. Inspect work controls to pause or stop other work.'],
 ['Read and\nwatch with context',['Left chevrons reveal the transcript','Right chevrons reveal the browser panel','Drag a panel divider to resize it','Follow a site’s request when Genesis needs you'],'Closing the browser panel hides its view. Check work status and controls when you intend to stop browser activity.'],
 ['Choose an\nexplicit ending',['Use the exit icon or press Escape','Check that the session has ended','Retry audio attempts the retained recording','Save audio or Discard & reset are separate choices'],'Read any recovery notice before acting. Ending or muting is deliberate; leaving the speaker quiet alone is not microphone mute.']
 ],
 vision:[
 ['A photograph\nwith two helpers',['Vision helper: looks at the photograph','Helper produces an image description','Text-only main model receives that description','Main model reasons and answers you'],'If the helper misses a small detail, the main model may miss it too. The main model does not gain image capability.'],
 ['Prove the\nimage connection',['Create the image-capable model’s own preset','Use a real installed local or accessible cloud model','Save and test its connection and image input','Keep Auto-detect unless you know metadata is wrong'],'A capability selector records a declaration. Choosing Vision / multimodal cannot give a text-only model new abilities.'],
 ['A local\nhelper example',['Primary: your working text-only local model','Secondary: your tested local image model','Choose its preset under Secondary vision model','Save the intended Voice & Vision settings'],'A cloud helper receives images even with a local primary. Choose a local helper if you want these model calls local.'],
 ['Understand\nthe route choices',['Auto: resolved primary, then secondary if needed','Always secondary: every image uses the helper','Disabled: no image-model routing','Legacy: older dedicated configurations'],'The resolved primary can be the effective backup model. Review the actual route instead of assuming a saved name determines it.'],
 ['Test a\nsimple picture',['Save changes and read Effective route','First-use status may still be unverified','Attach a simple picture and Send your question','Ask: “Describe what you see.”'],'Confirm the description against the picture. A status declaration is not a successful first image response.'],
 ['Ask for the\nmissing detail',['Check the helper’s description first','Ask about the exact label or region you need','Provide a clearer screenshot if necessary','Compare the answer with the visible image'],'A local primary and local helper keep those model calls local. Web tools and other cloud services are separate routes.'],
 ['Seeing is\nnot acting',['OCR reads written text on the screen','Set-of-Marks limits numbered control targets','Computer use controls permission to operate apps','Image files and Missions also use vision routing'],'Reading a button label does not grant permission to click it. Keep image capability and tool access distinct.']
 ],
 appshots:[
 ['Ready on\nthis computer',['Open Settings → Computer use → Appshots','Enable Appshots and check Shortcut ready','Choose whether a capture sound should play','The desktop preference applies immediately'],'No Save changes click is required for this desktop preference. If unavailable, read its status before trying the shortcut.'],
 ['One window,\none snapshot',['Bring the intended app window to the front','Press Left Alt + Right Alt together','Release both before another capture','Return to Genesis to inspect the draft attachment'],'Appshots captures the visible foreground window. It is a snapshot taken at that moment.'],
 ['The Send\ncheckpoint',['Inspect the attached screenshot','Write: “Explain this error message.”','Press Send when the content is right','The selected image route reads it after Send'],'The capture never sends itself. The pictured attachment is an isolated example of the staged draft.'],
 ['Look before\nyou share',['Check the exact captured window content','Remove an accidental private screenshot','Choose a local vision route if that is your intent','Send only the image and question you checked'],'A snapshot is not a live screen stream. Cloud image routing can apply after Send even when your main model is local.']
 ]};
add('title','Speak.\nListen. See.',{body:'Seven complete lessons for voice, pictures and your screen.\nChoose the routes. Read the status. Keep control.',tag:'VIDEO 4 · COMPLETE CATEGORY 3'},18);
list('Your route\nthrough voice',lessons.slice(0,4).map(l=>l.title),'Have Genesis open. Pause to practice. Screenshots are clean demonstration fixtures; examples are not live provider results.',30);
list('Your route\nthrough vision',lessons.slice(4).map(l=>l.title),'This video has no duration target. Keep the prerequisite, practical example and checkpoint for each step.',26);
compare('Three parts\nof a spoken reply',['LISTENING','A recognition engine turns your audio into words. Dictation lets you review those words before Send.','SPEECH-TO-TEXT'],['SPEAKING','A speaking engine turns reply text into audio. Your language model remains the part that answers.','TEXT-TO-SPEECH'],'Choose listening, answering and speaking independently. Start with one short test of each part.');
for(let n=0;n<lessons.length;n++){
 chapter=n+1;lesson=lessons[n];step=null;
 add('title',['Speak into\nyour draft.','Hear the\nwords clearly.','A voice\nyou choose.','Local or cloud.\nYour choice.','An ongoing\nconversation.','Give images\na helper.','Show the window.\nThen Send.'][n],{body:lesson.title+'\n'+['Dictation, spoken conversation and read-aloud.','Languages, installed sizes and the active device.','Installed voices, downloads, effects and recovery.','Independent audio routes and matching credentials.','States, mute controls, interruptions and ending.','A real image model, routing and the limits of description.','The dual-Alt shortcut and an inspected draft.'][n],tag:`LESSON ${n+1} OF 7`},18);
 list('Before\nyou begin',chunks(lesson.prerequisites,18),'Prepare these prerequisites before you try the lesson. Pause whenever you need time in Genesis.',24);
 for(const s of lesson.steps){step=s.step;const blocks=chunks(s.narrationDraft),g=geometry(s);
  for(let j=0;j<blocks.length;j++)shot(titles[lesson.id][step-1],blocks[j],g,`Step ${step} of ${lesson.steps.length}${blocks.length>1?' · Teaching '+(j+1)+' of '+blocks.length:''}. ${j===0?'Locate the highlighted control.':'Read this before you change the setting.'}`);
  if(lesson.id==='dictation'&&step===4)shot('Find\nRead aloud','Use Read aloud beside an existing reply. This plays the reply text; it does not open an ongoing listening session.',{screen:'@video4/chat-read-aloud',crop:[355,166,440,86],highlight:[367,207,18,18],callout:'Read aloud: play the reply already on screen'},'Demonstration reply. Use one short read-aloud test to check the voice.').supplemental=true;
  if(lesson.id==='orb'&&step===5)shot('Keep the\norb visible','The transcript appears beside the orb. Resize its divider to choose how much room the words and the orb receive.',{screen:'@video4/orb-transcript',crop:[0,0,1280,720],highlight:[485,480,37,37],callout:'Left chevrons reveal or hide the transcript'},'The browser panel has its own right chevrons. Hiding a panel changes the view.').supplemental=true;
  if(s.tip)list('A useful\ndetail',chunks(s.tip,22),'Keep this distinction in mind as you practice.',24);
  const p=practice[lesson.id][step-1];list(p[0],p[1],p[2],28);
  const check=list('Pause and\ncheck this',[s.checkpoint],'Try it in Genesis. Pause for as long as you need. Continue when you can explain or confirm this result.',22);check.checkpointSteps=[step];check.sourceSteps=[];
 }
 step=null;list('Lesson\ncomplete',['Check the actual status and a small test','Keep listening, answering and speaking separate','Review what is sent and which route receives it','Return to any step with the lesson chapter'],'Continue at your own pace. A saved setting and a real successful test provide different evidence.',24);
}
chapter=7;lesson=null;step=null;
list('Your voice\nand vision checklist',['Dictation produces an editable draft','Orb conversation submits spoken turns','Local and cloud routes are explicit choices','Vision helper descriptions can miss details','Appshots stages an image; you inspect and Send'],'All seven lessons and all 37 teaching steps of “Speak. Listen. See.” are now covered.',31);
add('title','Ready for\nwork that flows.',{body:'Keep your tested listening, speaking and vision choices.\nNext in video 5: Turn ideas into finished work — the complete fourth category.',tag:'PAUSE · PRACTICE · RETURN'},20);
for(const s of scenes){s.title=s.title.trimEnd();const words=[s.title,s.body,s.note,s.quote,...(s.items||[]),...(s.cards||[]).flatMap(c=>[c.title,c.body,c.tag])].filter(Boolean).join(' ').split(/\s+/).length;s.readingWords=words;s.readingSeconds=words/150*60;s.locateSeconds=s.kind==='screen'?7:4;s.duration=Math.max(s.duration,Math.ceil(s.readingSeconds+s.locateSeconds+3));}
const data={title:'Speak. Listen. See.',subtitle:'Complete category 3',music:'C:/Development-Gen/songs/Video 4 song.mp3',outputFolder:'output/video-04',filename:'Genesis-Speak-Listen-See.mp4',lessonIds:ids,chapters:['Introduction',...lessons.map(l=>l.title)],progressLabels:labels,sourceLessons:lessons,audio:{repeatStart:7.5,trimEnd:232.5,crossfade:9,fadeIn:4,fadeOut:8,rationale:'Video-4 source decodes to 239.8535s. Its first 7s are a quieter opening before the strong section; preserve that opening once. Repeat from 7.5s, end at 232.5s before the late 233–236s dynamic break and 239s near-silence. The repeat span is 225s with 9s equal-power qsin overlaps, giving 216s spacing. Four-second entrance and eight-second final fade. Derived from this track’s measured envelope; inspect every rendered join, entire-bed silence and loudness. No continuous subjective-listening claim.'},scenes};
fs.writeFileSync(path.join(root,'timeline-video4.json'),JSON.stringify(data,null,2));console.log(JSON.stringify({scenes:scenes.length,total:scenes.reduce((n,s)=>n+s.duration,0),steps:lessons.reduce((n,l)=>n+l.steps.length,0)}));
