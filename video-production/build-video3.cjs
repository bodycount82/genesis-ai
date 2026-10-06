/* Video 3 editorial source: every source sentence, tip, prerequisite and checkpoint retained. */
const fs=require('node:fs'),path=require('node:path');const root=__dirname;
const catalog=JSON.parse(fs.readFileSync(path.resolve(root,'../tutorials/assets/scenes.json')));
const ids=['local-model','cloud-model','parse-code','model-controls','backup'],lessons=ids.map(id=>catalog.lessons.find(l=>l.id===id));
const labels=['LOCAL MODEL','CLOUD MODEL','PASTE CODE','MODEL CONTROLS','BACKUP'];
const scenes=[];let chapter=0,lesson=null,step=null;
function add(kind,title,fields={},duration=24){const s={chapter,lesson:lesson?.id||null,sourceSteps:step?[step]:[],duration,kind,eyebrow:chapter?`${String(chapter).padStart(2,'0')} / ${labels[chapter-1]}${step?' · STEP '+step:''}`:'GENESIS AI · CATEGORY 2',title,...fields};scenes.push(s);return s;}
function list(title,items,note='',duration=26){return add('list',title,{items,note},duration)}
function compare(title,left,right,note=''){add('compare',title,{cards:[{title:left[0],body:left[1],tag:left[2]||''},{title:right[0],body:right[1],tag:right[2]||''}],note},31)}
function shot(title,body,screen,crop,highlight,callout,note=''){add('screen',title,{body,screen,crop,highlight,callout,note,contextZoom:false},26)}
const titles={
 'local-model':['Two local\nroutes','Save a\nuseful preset','Match the\nOllama name','Choose your\nGGUF file','Start with\nmodest settings','Try a\nreal hello'],
 'cloud-model':['Choose your\ncloud provider','Keep the\ndetails together','Use the\nAPI key field','Supported\nsettings only','Save and\ntry it'],
 'parse-code':['Choose provider\nand key first','Show the\ncode panel','Parse, then\nreview','Which value\nwill be sent?','Return control\nto the form','Separate\nsettings','Save the form\nand template','Each preset\nis independent'],
 'model-controls':['Your model’s\nworking desk','A size that\nreally fits','Variation and\nrepetition','Reasoning and\nstreaming','Profiles and\nmood'],
 'backup':['Test both\nmodels first','Choose your\nbackup','When fallback\ncan help','Chosen versus\nanswering model','Retry on a\nreal request','Mission roles\nare separate']};
function geometry(s){const n=path.basename(s.screenshot,'.png'),a=s.anchor;let crop;
 if(n==='models')crop=a.y>800?[265,810,765,140]:a.y>600?[265,525,765,270]:[250,145,790,365];
 if(n==='model-new')crop=a.y<200?[515,120,560,215]:a.y>500?[520,345,550,290]:[520,345,550,250];
 if(n==='model-connection')crop=[270,205,750,225];
 if(n==='model-cloud')crop=[270,205,750,235];
 if(n==='model-generation')crop=a.y<300?[270,205,750,280]:a.y<400?[275,295,740,155]:[275,370,745,260];
 if(n==='chat-modern')crop=[1080,870,250,85];
 if(n==='model-code')crop=[270,205,750,225];
 if(n==='model-parsed')crop=a.y<160?[1435,90,150,65]:a.y<450?[275,275,740,165]:[275,438,740,180];
 if(n==='model-chooser')crop=[895,590,345,300];
 if(n==='model-reasoning')crop=[270,395,750,335];
 if(n==='chat-backup')crop=[540,905,410,90];
 if(n==='mission-models')crop=[270,205,750,520];
 const highlight=[a.x-a.width/2,a.y-a.height/2,a.width,a.height];
 return {screen:n,crop,highlight,callout:a.label.length>65?'Status: using backup; next request retries primary':a.label};
}
// Exact words remain in their original order; split at sentence boundaries for comfortable panels.
const {createCanvas,GlobalFonts}=require('C:/Users/damir/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');GlobalFonts.registerFromPath('C:/Windows/Fonts/segoeui.ttf','Genesis');const measure=createCanvas(10,10).getContext('2d');
function chunks(text,max=37){const width=max===37?678:810,size=max===37?40:33,allowed=max===37?5:2;measure.font=size+'px Genesis';
 const rows=t=>{let count=1,row='';for(const word of t.split(/\s+/)){const next=row?row+' '+word:word;if(measure.measureText(next).width>width&&row){count++;row=word}else row=next}return count;};
 const sentences=text.split(/(?<=[.!?])\s+/);let out=[],current='';
 for(let sentence of sentences){sentence=sentence.trim();if(!sentence)continue;
  if(rows(sentence)>allowed){if(current){out.push(current);current='';}let part='';for(const word of sentence.split(/\s+/)){const next=(part+' '+word).trim();if(rows(next)>allowed&&part){out.push(part);part=word;}else part=next;}if(part)out.push(part);}
  else if(rows((current+' '+sentence).trim())>allowed){if(current)out.push(current);current=sentence;}else current=(current+' '+sentence).trim();
 }if(current)out.push(current);return out;}
// Every step has a concrete practice example and its source checkpoint.
const practice={
 'local-model':[
 ['Choose the route\nthat fits',['Ollama: choose a downloaded model by its name','llama.cpp: choose an existing .gguf model file','Initial download: internet required','Local replies can work offline after setup'], 'A web search still needs internet, even while the model itself runs locally.'],
 ['Name it for\nyour everyday job',['Open Settings → Models → New','Use “My everyday local model” as the label','Pick the provider for your local route','Keep different connections in different presets'], 'The friendly template label is separate from the exact technical model name.'],
 ['Check an\nOllama example',['Example name: qwen3:8b','Use it only if that exact model is installed','Example local address: http://127.0.0.1:11434','Keep the address of your own running service'], 'Typing qwen3:8b into the form saves a name; it does not install that model.'],
 ['Check a\nGGUF example',['Example path: C:/Models/my-model.gguf','Replace it with a real file on your computer','Use the endpoint of the service that loads it','Leave GPU layers at the supplied starting value'], 'A filename in this example is a placeholder. An absent file cannot supply a model.'],
 ['Save, choose,\nthen apply',['Keep the recommended generation settings','Create the template with your connection','Choose that template as your primary','Press Save changes on the Models page'], 'Start with a smaller model and supported context if memory is limited. A larger number is not extra hardware.'],
 ['Run a\nsmall connection test',['Send: “Hello. Reply with one short sentence.”','Wait for an actual answer','If disconnected: check service, address and name','If slow: try a smaller model or supported context'], 'A saved template proves the configuration was stored. The reply proves your connection works.']
 ],
 'cloud-model':[
 ['A key for\nthe right service',['NVIDIA Cloud, Nebius or Anthropic: matching API access','Custom: an OpenAI-compatible API service','Use the provider’s API account and API key','Keep internet available for cloud requests'], 'A chat website membership may be separate from API access. Check the account you are using.'],
 ['One service,\nthree matching details',['Provider: the service your account belongs to','Endpoint: its documented base address, if shown','Model: the exact identifier your account can use','Preset label: a friendly name you recognise'], 'Do not combine one company’s key with another service’s example URL or model name.'],
 ['Keep your\nkey private',['Paste the real key only into the provider key field','Save the configuration','Look for the saved key-set status','Use placeholders in shared examples and screenshots'], 'A template and a pasted example are not a substitute for entering the actual key in its own field.'],
 ['Follow the\nmodel’s support',['Begin with the matching supplied preset','Use documented values for that provider and model','Omit unsupported optional form parameters','Keep thinking profiles with their matching preset'], 'Switches can omit form parameters where supported. Active imported parameters are covered in the next lesson.'],
 ['Test before\na larger task',['Save changes, then return to Conversation','Send one short request','Check key, exact name, address and quota if it fails','Inspect provider usage when checking costs'], 'Genesis Activity totals help you track use; they do not replace the provider’s charges or quota page.']
 ],
 'parse-code':[
 ['What the\nparser does',['You choose the intended provider or template','You enter the real API key in its own field','Parse code reads the pasted example as text','It neither executes code nor installs a model'], 'Connection code is a convenient source of settings. It cannot create a provider account or grant API access.'],
 ['Read the\nexample first',['base_url = https://api.example.com/v1','model = your-model-name','api_key = YOUR_API_KEY','temperature = 0.7; max_tokens = 4096; seed = 42'], 'Deliberately nonworking example values. Use your provider’s documented address and model; keep a placeholder here.'],
 ['Review what\nwas detected',['Confirm the provider yourself','Review detected model and base URL','Read warnings and the imported checklist','Check any detected vision or thinking profiles'], 'The saved snippet redacts recognised key text. The parser never fills the actual provider API key field.'],
 ['The 0.7 / 0.3\nexample',['Imported temperature: 0.7, checked','Apply pasted parameters: on','Form temperature: 0.3, dimmed','Effective temperature for the request: 0.7'], 'Pause: which wins? The checked imported 0.7 wins over the matching form value. Genesis does not average them.'],
 ['Give just one\ncontrol back',['Uncheck temperature in the imported checklist','Enable the form’s Temperature control','Set the form value you actually want','Leave other wanted imported keys checked'], 'Turning off the master Apply pasted parameters switch stops the whole imported overlay. Enable the form controls you need.'],
 ['Output and\ncontext differ',['max_tokens / max_completion_tokens: reply limit','seed: may have no matching form slider','Context window: prompt budget and local-server setup','Thinking ON/OFF profiles: separate active overrides'], 'Changing thinking can select a profile that overrides static pasted thinking settings. Review the matching profile.'],
 ['Two places\nto save',['Save changes: apply the edited Models form','Update template: keep edits in the reusable preset','New: Create template, then Models → Save changes','Test one short message after saving'], 'Before saving, verify provider, URL, exact model, key status and active imported values together.'],
 ['Keep model A\nand B separate',['Save model A’s connection and imported settings','Choose model B’s own saved preset','Check that B has B’s intended configuration','Clear removes the imported snippet and keys'], 'After Clear, review separately detected thinking profiles and image capability. They may need their own adjustment.']
 ],
 'model-controls':[
 ['A working-desk\nexample',['Example total context: 8,192 tokens','Example output limit: 1,024 tokens','Example framing reserve: 512 tokens','Input must also leave room for output and framing'], 'Illustrative arithmetic leaves at most 6,656 tokens before other constraints. A token is a piece of text, not a word.'],
 ['Match the\nreal capacity',['Check what your model actually supports','Check the loaded server’s context','Check available RAM / graphics memory','Leave Trust my context window off unless verified'], 'For Ollama, configure the loaded model/server separately. Genesis’s form alone does not enlarge that server window.'],
 ['Change one\nthing at a time',['Keep the model’s recommended starting values','Use the same short request for comparison','Change one supported control only','Save, inspect the result, then keep or undo'], 'Temperature changes variation. Top-P/Top-K constrain choices. Repetition controls depend on provider support.'],
 ['Choose effort\nand presentation',['Use profile: retain the saved reasoning behavior','Off / Low / Medium / High: only if supported','Stream on: display words as they arrive','Stream off: wait for the complete reply'], 'Try the same small request with streaming on and off. Tools remain available; the display timing changes.'],
 ['A ceiling for\nmood-based effort',['Thinking follows mood starts off','On: effort responds to mood and kind of turn','It stays within your selected ceiling','Use profile uses High as the ceiling'], 'Rested or flowing work can use more effort; tiredness or small talk less; resting can turn thinking off. Supported reasoning models only.']
 ],
 'backup':[
 ['Prove both\nconnections work',['Choose the primary and send a short test','Choose the intended backup and test it too','Save both as their own presets','Return to the primary you want for everyday use'], 'An uninstalled local model or cloud model with an invalid key cannot rescue the primary.'],
 ['A companion\nbackup example',['Primary: your tested cloud preset','Backup: your tested local preset','Models → Companion failover → Backup model','Save changes; look for the standby status'], 'The compact Backup chooser below the Modern draft also selects a saved backup. A cloud outage need not stop local replies.'],
 ['Before versus\nafter delivery',['Primary fails before answering: backup can retry','Example cause: rate limit, timeout or outage','The working request carries forward','Delivered content or tool work is not blindly replayed'], 'A partial failure may require you to inspect what already happened. Fallback cannot promise recovery of every unfinished result.'],
 ['Read both\nmodel identities',['Configured primary: your chosen cloud preset','Effective model during fallback: the local backup','The saved primary remains the same','Expect the backup’s own capabilities and limits'], 'Illustrative fallback status. A smaller text-only model may answer more simply or need a separate vision helper for pictures.'],
 ['A 30-minute\ncooldown example',['00:00 — recoverable primary failure uses backup','00:30 — timer passes; no paid background ping','Next actual request tries the primary','Success returns; failure starts another wait'], 'The times are illustrative. A backend restart starts with the saved primary; timer expiry alone sends no test request.'],
 ['Set the\nmission roles too',['Settings → Missions → Role models','Check each role’s own primary and backup','Roles can have different models and failover windows','Check this before starting a big mission'], 'Companion backup covers Chat, Work, Autonomy and helpers. It does not replace mission role choices or remove context / step limits.']
 ]};
add('title','Choose your\nintelligence',{body:'Five complete lessons for a model setup you understand.\nLocal. Cloud. Connection code. Controls. Backup.',tag:'VIDEO 3 · COMPLETE CATEGORY 2'},18);
list('Your route\nthrough this video',lessons.map(l=>l.title),'Have Genesis open. Pause to practice. Screenshots are demonstration fixtures; displayed numbers are not recommendations. Test your own connection.',30);
compare('Pick a brain\nfor the job',['LOCAL','Runs on your computer. Choose a model that fits your memory and a service that can load it.','YOUR COMPUTER'],['CLOUD','Runs at your provider. Requires internet, API access and matching connection details.','PROVIDER’S COMPUTERS'],'Both routes use saved presets. A working second preset can become your backup.');
for(let n=0;n<lessons.length;n++){
 chapter=n+1;lesson=lessons[n];step=null;
 add('title',['Your computer.\nYour model.','Connect to\nthe cloud.','Paste. Parse.\nUnderstand.','Know your\nmodel controls.','Keep a\nbackup ready.'][n],{body:lesson.title+'\n'+[ 'The local route, saved setup and first real answer.','Provider, endpoint, exact name and private key.','Read the import and know which values win.','Context, output, variation and supported thinking.','Test a second model and understand recovery.'][n],tag:`LESSON ${n+1} OF 5`},18);
 list('Before\nyou begin',chunks(lesson.prerequisites,18),'These are the prerequisites for this lesson. Prepare them before you try the connection.',24);
 for(const s of lesson.steps){step=s.step;
  const blocks=chunks(s.narrationDraft),g=geometry(s);
  if(lesson.id==='cloud-model'&&step===2)Object.assign(g,{screen:'model-cloud',crop:[270,205,750,225],highlight:[280,270,78,20],callout:'Model name: exact identifier from your provider'});
  for(let j=0;j<blocks.length;j++)shot(j?titles[lesson.id][step-1]+'\n':titles[lesson.id][step-1],blocks[j],g.screen,g.crop,g.highlight,g.callout,`Step ${step} of ${lesson.steps.length}${blocks.length>1?' · Teaching '+(j+1)+' of '+blocks.length:''}. ${j===0?'Locate the highlighted control.':'Read this before you change the setting.'}`);
  if(s.tip)list('A useful\ndetail',chunks(s.tip,22),'Keep this distinction in mind as you practice.',24);
  const p=practice[lesson.id][step-1];list(p[0],p[1],p[2],28);
  const check=list('Pause and\ncheck this',[s.checkpoint],'Try it in Genesis. Pause for as long as you need. Continue when you can explain or confirm this result.',22);check.checkpointSteps=[step];check.sourceSteps=[];
 }
 step=null;list('Lesson\ncomplete',['Review the saved preset and the observed result','Keep separate configurations for different models','Return to any step with the lesson chapter','Continue when the checkpoint is clear'],'Your pace matters more than the running time. You can revisit the lesson whenever your setup changes.',24);
}
chapter=5;lesson=null;step=null;
list('Your model\nsetup checklist',['A working local preset','A working cloud preset, if you choose cloud','Reviewed pasted parameters and separate keys','Context and thinking within supported limits','A tested backup and understood retry status'],'All five lessons and all 30 teaching steps of “Choose your intelligence” are now covered.',31);
add('title','Ready for\nvoice and vision.',{body:'Keep your tested presets.\nNext in video 4: Speak. Listen. See. — the complete third category.',tag:'PAUSE · PRACTICE · RETURN'},20);
for(const s of scenes){s.title=s.title.trimEnd();const words=[s.title,s.body,s.note,s.quote,...(s.items||[]),...(s.cards||[]).flatMap(c=>[c.title,c.body,c.tag])].filter(Boolean).join(' ').split(/\s+/).length;s.readingWords=words;s.readingSeconds=words/150*60;s.locateSeconds=s.kind==='screen'?7:4;s.duration=Math.max(s.duration,Math.ceil(s.readingSeconds+s.locateSeconds+3));}
const data={title:'Choose your intelligence',subtitle:'Complete category 2',music:'C:/Development-Gen/songs/video 3 song.mp3',outputFolder:'output/video-03',filename:'Genesis-Choose-Your-Intelligence.mp4',lessonIds:ids,chapters:['Introduction',...lessons.map(l=>l.title)],progressLabels:labels,sourceLessons:lessons,audio:{repeatStart:7.5,trimEnd:231.5,crossfade:8,fadeIn:4,fadeOut:8,rationale:'Video-3 decoded envelope: retain its original opening once; repeats enter at the first strong 7.5s section. Use a 224s musical span and 8s overlap (216s repeat spacing); omit the descending near-silent ending after 237s. Equal-power overlaps cover the final 223.5–231.5s phrase with the incoming 7.5–15.5s phrase. Four-second opening and eight-second final fades, calm -20 LUFS target. Instrumented envelope inspection; no continuous subjective-listening claim.'},scenes};
fs.writeFileSync(path.join(root,'timeline-video3.json'),JSON.stringify(data,null,2));console.log(JSON.stringify({scenes:scenes.length,total:scenes.reduce((n,s)=>n+s.duration,0),steps:lessons.reduce((n,l)=>n+l.steps.length,0)}));
