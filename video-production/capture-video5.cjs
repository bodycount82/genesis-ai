// Renders the current Genesis React/Electron interface with clean demonstration data.
// No production settings, memories, credentials, microphone or model calls are used.
const { app, BrowserWindow, ipcMain, session } = require('electron');
const fs = require('node:fs'), path = require('node:path'), { createRequire } = require('node:module');
const { execFileSync } = require('node:child_process');
const crypto = require('node:crypto');
const genesis = path.resolve(__dirname, '../../Genesis');
const frontend = path.join(genesis, 'frontend');
const req = createRequire(path.join(frontend, 'package.json'));
const out = path.resolve(__dirname, 'assets/video5/screens');
const run = path.join(__dirname, 'output/video-05/capture-runtime');
fs.mkdirSync(out, { recursive: true }); fs.mkdirSync(run, { recursive: true });
app.setPath('userData', path.join(run, 'profile'));
const defaults = JSON.parse(fs.readFileSync(path.join(genesis, 'backend/genesis/defaults/settings.json'), 'utf8'));
const presets = JSON.parse(fs.readFileSync(path.join(genesis, 'backend/genesis/defaults/model_presets.json'), 'utf8')).presets;
const snippet = 'from openai import OpenAI\nclient = OpenAI(base_url="https://api.example.com/v1", api_key="YOUR_API_KEY")\nresponse = client.chat.completions.create(\n    model="your-model-name",\n    temperature=0.7,\n    max_tokens=4096,\n    seed=42\n)';
const parser = path.join(genesis, 'backend/genesis/llm/snippet_import.py');
const parsed = JSON.parse(execFileSync(path.join(genesis, 'backend/.venv/Scripts/python.exe'), ['-B', '-c', 'import runpy,json,sys; m=runpy.run_path(sys.argv[1]); print(json.dumps(m["parse_snippet"](sys.argv[2])))', parser, snippet], { encoding: 'utf8', windowsHide: true }));
fs.writeFileSync(path.join(out, '../parsed-example.json'), JSON.stringify(parsed, null, 2));
const demo = { ...defaults, companion_backup_model: 'qwen3-local', voice_enabled: true, tts_provider: 'piper', stt_provider: 'whisper', stt_model: 'auto', stt_device: 'auto', stt_languages: ['en'], piper_voice: 'en_US-amy-medium', vision_model: 'vision-demo', vision_provider: 'auto', mission_enabled: true, screen_control: 'ask', raw_config_enabled: false };
presets.push({ id: 'vision-demo', label: 'Vision helper (your image model)', provider: 'ollama', local: true, model: 'your-vision-model', vision_capability: 'vision', url: 'http://127.0.0.1:11434' });
const providerDefaults = { ollama: {local:true,has_url:true,needs_key:false,url:'http://127.0.0.1:11434',model:'qwen3:8b'}, llama:{local:true,has_url:true,needs_key:false,url:'http://127.0.0.1:8080/v1',model:'local-model'}, nvidia:{local:false,has_url:true,needs_key:true,url:'https://integrate.api.nvidia.com/v1'}, nebius:{local:false,has_url:true,needs_key:true,url:'https://api.tokenfactory.nebius.com/v1'}, anthropic:{local:false,has_url:false,needs_key:true,url:'https://api.anthropic.com/v1'}, custom:{local:false,has_url:true,needs_key:true,url:'https://api.example.com/v1'} };
const entry = `
import React from 'react'; import { createRoot } from 'react-dom/client';
import {ShellProvider, ShellRouter} from './shells/ShellRouter';
import {VoicePresentationProvider, useVoicePresentation} from './shells/voicePresentation';
import {FirstRunWizard} from './components/FirstRunWizard';
import {useStore} from './store'; import {api} from './lib/api'; import {TitleBar} from './components/Shell'; import './styles.css';
import {loadVoiceStatus} from './lib/voice';
const demo=${JSON.stringify(demo)}, presets=${JSON.stringify(presets)}, pd=${JSON.stringify(providerDefaults)};
localStorage.setItem('genesis-shell','modern');localStorage.setItem('genesis-modern-activity','false');
Object.keys(api).forEach(k=>{if(typeof api[k]==='function') api[k]=async()=>({ok:true})});
api.getSettings=async()=>({settings:demo,presets,provider_defaults:pd});
api.putSettings=async(patch)=>{Object.assign(demo,patch);return {ok:true,settings:demo}};
api.getPresets=async()=>({presets,provider_defaults:pd});
api.createPreset=async(p)=>({presets:[...presets,p],preset:p});
api.reasoningCapability=async()=>({supported:false,levels:[]});
api.voiceStatus=async()=>({enabled:true,stt_provider:'whisper',tts_provider:'piper',effective_tts_provider:'piper',tts_voice:'en_US-amy-medium',stt_ready:true,tts_ready:true,voice:'en_US-amy-medium',autospeak:'on_request'});
loadVoiceStatus();
api.visionStatus=async()=>({supported:true,verified:false,provider:'ollama',model:'your-vision-model',strategy:'Auto: primary → secondary fallback',source:'secondary preset',reason:'Primary is text-only. The secondary model describes the image.',fallback:{configured:true,supported:true,verified:false,model:'your-vision-model',provider:'ollama',reason:'Will be tested on first use'}});
api.serverCache=async()=>({notices:[],env:{set_by_genesis:false}});
api.memoryStats=async()=>({total:42,tiers:{episodic:25,semantic:12,procedural:5},embedder:'local'});
api.speechModels=async()=>({current:'auto',auto_target:'small',effective:'base',recommended:'small',device:'cpu',device_choice:'auto',gpu:{gpu:null,libraries:false,local_ai:true},available_languages:[{code:'en',name:'English'},{code:'sl',name:'Slovenian'},{code:'de',name:'German'}],models:[{name:'base',label:'Base',size_mb:142,ram_mb:500,installed:true,fits:true},{name:'small',label:'Small',size_mb:462,ram_mb:1200,installed:false,fits:true},{name:'large-v3-turbo',label:'Large v3 turbo',size_mb:1600,ram_mb:3000,installed:false,fits:true}]});
api.voiceVoices=async(provider)=>provider==='piper'?{voices:[{value:'en_US-amy-medium',label:'Amy · English (US)'}],installed:[{value:'en_US-amy-medium'}],catalog:[{value:'en_US-ryan-high',label:'Ryan · English (US)'}]}:{voices:provider==='openai'?[{value:'alloy',label:'alloy'}]:[],installed:[],catalog:[]};
api.parseSnippet=async()=>(${JSON.stringify(parsed)});
api.listBackups=async()=>({backups:[],path:'Your Genesis data folder'});
api.memoryHealth=async()=>({ok:true,checks:[]});
api.integrationsStatus=async()=>({telegram:{enabled:false},phone:{paired:false}});
api.ownerRequests=async()=>({open:[],recent:[]});
api.browserStatus=async()=>({open:false,tabs:[]}); api.desktopStatus=async()=>({active:false,busy:false,control:'user'});
api.setupExtras=async()=>({browsers:{browsers:[{key:'chrome',name:'Google Chrome',supported:true,installed:true,paired_before:true,connected:true,running:true,default:true},{key:'edge',name:'Microsoft Edge',supported:true,installed:true,paired_before:false,connected:false,running:false}]}});
api.getPlugins=async()=>({allow_ai_tool_creation:false,tool_groups:[{label:'Files',tools:[{name:'read_file',description:'Read a file from your workspace'},{name:'write_file',description:'Create or update a file'},{name:'list_directory',description:'See the files in a folder'}]},{label:'Execution',tools:[{name:'run_command',description:'Run a command for an approved task'}]},{label:'Memory',tools:[{name:'search_memory',description:'Look up something Genesis remembers'}]}]});
api.getExtensions=async()=>({plugins:[],mcp:{servers:[]}});api.getConnectors=async()=>({connectors:[]});api.getHooks=async()=>({hooks:[]});
api.codeOverview=async()=>({git:{available:true,state:'ready'},folders:[],copies:[],reviews:[]}); api.codeReviews=async()=>({reviews:[]});api.githubAccount=async()=>({connected:false});
api.listMissions=async()=>({enabled:true,missions:[],overview:{}});api.missionSummary=async()=>({});
api.setupStatus=async()=>({configured:false,runtime:'cloud'});api.autoStatus=async()=>({});
api.getProjectTree=async()=>({tree:[{id:'demo-project',title:'A birthday invitation',description:'Write a friendly invitation with the date, place and reply details.',status:'review',priority:'medium',tasks:[{id:'draft',title:'Draft the invitation',status:'done'}],children:[],execution_model:''}],stats:{active_projects:1,projects_in_review:1}});
let missionStage='DRAFT',graphDemo=false,blockerDemo=false;const mission={id:'demo-mission',title:'A weekend away',objective:'Compare three destinations for a weekend away.',status:'DRAFT',intake:[{role:'user',text:'Compare three destinations. Keep the budget below €300.'},{role:'assistant',text:'Who is travelling, what dates suit you, and where will you start?'}],contract:{objective:'Compare three weekend destinations in a table with source links.',acceptance_criteria:[{id:'ac1',text:'The table compares three destinations and includes travel, lodging and source links.',verify_method:'Open the document and check all three rows and their links.',kind:'user'}],authority:{spend_cap_cents:0,outward_actions:'none',software_install:'user',allowed_paths:[],allowed_domains:[]},constraints:{never_do:'Do not book or pay for anything.'},escalation:{channel:'gui'},role_models:{},automation:{checkins:'ask'}},progress:[],blockers:[]};
const graphNodes=[
 {id:'compare',title:'Prepare the three-destination comparison',type:'work',milestone:true,status:'pending',ac_id:'ac1'},
 {id:'travel',parent_id:'compare',title:'Find travel options and record source links',type:'research',status:'done',depends_on:[],attempts:1,max_attempts:3},
 {id:'rooms',parent_id:'compare',title:'Check lodging prices for the chosen dates',type:'research',status:'awaiting_verify',depends_on:[],attempts:1,max_attempts:3},
 {id:'table',parent_id:'compare',title:'Build the budget table from checked sources',type:'work',status:'pending',depends_on:['travel','rooms']},
 {id:'check',parent_id:'compare',title:'Check totals, links and the budget limit',type:'verify',status:'pending',depends_on:['table']},
 {id:'revise',parent_id:'compare',title:'Earlier search route (replaced after a blocked page)',type:'research',status:'obsolete',depends_on:[]}
];
api.listMissions=async()=>({enabled:true,missions:[{...mission,status:missionStage}],overview:{}});api.getMission=async()=>({...mission,status:missionStage,handoffs:blockerDemo?[{id:'dates',title:'Confirm your travel dates',blocker:{type:'information',what_user_must_do:'Tell Genesis which weekend you can travel',detail:'The price comparison needs dates you can actually use. Your answer is recorded for this mission.'}}]:[]});api.missionGraph=async()=>({nodes:graphDemo?graphNodes:[]});api.missionLedger=async()=>({events:[]});api.currentMissionInterview=async()=>({run:null});
api.missionPaymentOptions=async()=>({enabled:false,connections:[],services:[]});api.missionPayments=async()=>({summary:{status:'disabled'},pending:[],payments:[]});
api.missionInterviewOptions=async()=>({enabled:true,extensions:['.pdf','.docx','.txt','.png','.jpg'],max_attachments:10,max_attachment_bytes:10485760,voice:true});
api.getActivity=async()=>({today:'2026-10-03',recording_since:'2026-10-03',calendar_timezone:'local',totals:{tokens:2400,peak_tokens:2400,longest_task_seconds:95,longest_streak:1,current_streak:1,calls:3,tasks:1,measured_input:1600,measured_output:800,estimated_input:0,estimated_output:0},days:[{date:'2026-10-03',tokens:2400,measured_tokens:2400,estimated_tokens:0,calls:3,tasks:1,active:true}],top_tools:[{name:'read_file',calls:2}]});
api.getProjects=async()=>({projects:[]});api.getSchedule=async()=>({tasks:[]});api.getDiscoveries=async()=>({items:[]});
const snapshot={status:'Idle',state:'idle',mode:'Chat',autonomy_active:false,cognitive_load:12,energy:84,curiosity:45,frustration:0,satisfaction:62,happiness:60,boredom:8,inspiration:38,flow:{active:false,count:0,goal:null},rest_remaining_seconds:0,queue_size:0,queue_mode:0,api:{minute:0,hour:0,day:0,limits:{per_minute:40,per_hour:1200,per_day:7200}},model:{name:'qwen3:8b',provider:'ollama',local:true,reachable:true},companion_failover_status:{using_backup:false,configured:true,primary_provider:'ollama',primary_model:'qwen3:8b',backup_model:'qwen3:8b'},memory:{}};
useStore.setState({view:'chat',dark:true,connected:true,snapshot,chats:[{id:'demo',title:'Your first conversation',updated_at:0}],currentChatId:'demo',messages:[{id:1,role:'user',content:'Help me plan a small herb garden for my kitchen window.'},{id:2,role:'assistant',content:'Of course. Let’s start with basil, mint and parsley. Tell me how much sunlight your window gets, and I’ll help you choose pots and a simple watering routine.'}],plan:[{task:'Choose herbs for the window',status:'done'},{task:'Check sunlight and pot sizes',status:'in_progress'},{task:'Write a watering routine',status:'pending'}],feedPlan:[]});
function Theme(){const dark=useStore(s=>s.dark);React.useEffect(()=>{document.documentElement.classList.toggle('dark',dark)},[dark]);return null}
window.demo={store:useStore,voice:useVoicePresentation,settings:demo,missionStage:s=>{missionStage=s;useStore.setState({missionsRev:useStore.getState().missionsRev+1})},missionGraphDemo:(graph,blocker=false)=>{graphDemo=graph;blockerDemo=blocker;useStore.setState({missionsRev:useStore.getState().missionsRev+1})}};
function Demo(){const focused=useVoicePresentation(s=>s.focused);const [scene,setScene]=React.useState('');window.demo.scene=setScene;return <div className="app-frame flex flex-col h-screen"><div hidden={focused}><TitleBar/></div>{scene==='wizard'?<FirstRunWizard onDone={()=>setScene('')}/>:<ShellRouter hidden={false}/>}</div>}
createRoot(document.getElementById('root')).render(<ShellProvider><VoicePresentationProvider><Theme/><Demo/></VoicePresentationProvider></ShellProvider>);
`;
const onlyArg=process.argv.find(a=>a.startsWith('--only='));const only=onlyArg?new Set(onlyArg.slice(7).split(',')):null;
let win; const manifest = only?JSON.parse(fs.readFileSync(path.join(out,'../screens.json'),'utf8')):{ captured:'2026-10-03', origin:'Current Genesis source React/Electron, clean demonstration data. No live backend or model call.', source:{settings:crypto.createHash('sha256').update(fs.readFileSync(path.join(frontend,'src/components/views/SettingsView.tsx'))).digest('hex')},screens:{} };
const delay=ms=>new Promise(r=>setTimeout(r,ms)); const js=s=>win.webContents.executeJavaScript(s);
async function ready(s){for(let i=0;i<100;i++){if(await js(s))return;await delay(100)}throw Error('Not ready: '+s)}
async function click(label){await js(`(()=>{const e=[...document.querySelectorAll('button')].find(e=>e.getBoundingClientRect().height && (e.textContent.trim()===${JSON.stringify(label)} || e.getAttribute('aria-label')===${JSON.stringify(label)}));if(!e)throw Error('Missing button: '+${JSON.stringify(label)});e.click()})()`);await delay(220)}
async function capture(name){
 if(only&&!only.has(name))return;
 await delay(350);win.webContents.invalidate();await delay(80);
 const shot=await win.webContents.capturePage();fs.writeFileSync(path.join(out,name+'.png'),shot.toPNG());
 manifest.screens[name]={file:name+'.png',...shot.getSize(),sha256:crypto.createHash('sha256').update(shot.toPNG()).digest('hex'),controls:await js(`
 ([...document.querySelectorAll('button,label,summary,select,input,textarea,h1,h2,h3,h4,p,span,div,strong')]
 .filter(e=>!['P','SPAN','DIV'].includes(e.tagName)||(e.tagName==='P'?e.textContent.length<140:!e.children.length&&e.textContent.length>0&&e.textContent.length<100))
 .filter(e=>{
   const r=e.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2;
   for(let p=e.parentElement;p;p=p.parentElement){
     const c=getComputedStyle(p),a=p.getBoundingClientRect();
     if(/auto|scroll|hidden|clip/.test(c.overflowY)&&(y<a.top||y>a.bottom))return false;
     if(/auto|scroll|hidden|clip/.test(c.overflowX)&&(x<a.left||x>a.right))return false;
     if(c.position==='fixed')break;
   }
   const hit=document.elementFromPoint(x,y);return hit&&(hit===e||e.contains(hit)||hit.contains(e));
 })
 .map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,text:(e.textContent||'').trim().slice(0,140),label:(e.getAttribute('aria-label')||e.getAttribute('title')||(e.tagName==='TEXTAREA'?e.getAttribute('placeholder'):'')||e.textContent||e.getAttribute('placeholder')||'').trim().slice(0,140),x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),w:Math.round(r.width),h:Math.round(r.height)}})
 .filter(e=>e.w&&e.h&&e.x>0&&e.x<1600&&e.y>0&&e.y<1000))`)};
 console.log('Captured '+name);
}
async function settings(tab){await js(`window.demo.store.getState().openSettings(${JSON.stringify(tab)})`);await ready('!!document.querySelector(".settings-nav")');await delay(250);await js(`document.querySelectorAll('*').forEach(e=>{if(e.scrollTop)e.scrollTop=0})`)}
async function reveal(text){await js(`(()=>{const e=[...document.querySelectorAll('*')].find(e=>(e.children.length===0||e.tagName==='BUTTON')&&e.textContent.trim()===${JSON.stringify(text)});if(!e)throw Error('Missing text '+${JSON.stringify(text)});e.scrollIntoView({block:'start'});})()`);await delay(250)}
async function selectRow(label,value){await js(`(()=>{const p=[...document.querySelectorAll('p')].find(e=>e.textContent.trim()===${JSON.stringify(label)});const e=p?.parentElement.parentElement.querySelector('select');if(!e)throw Error('Missing select '+${JSON.stringify(label)});Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype,'value').set.call(e,${JSON.stringify(value)});e.dispatchEvent(new Event('change',{bubbles:true}));})()`);await delay(250)}
app.whenReady().then(async()=>{
 ipcMain.on('genesis:get-config',e=>{e.returnValue={apiBase:'http://127.0.0.1:9',apiPort:9,packaged:true}});
 for(const key of ['window:appearance','desktop:edge','browser:workspace','desktop:appshot-peek'])ipcMain.handle(key,()=>null);
 ipcMain.handle('desktop:companion-get',()=>({preferences:{appshotsEnabled:false,appshotsSound:true,petEnabled:false,pet:'hal-voice'},appshotsStatus:'disabled',error:'',pending:0,miniShortcutAvailable:true}));
 await req('esbuild').build({stdin:{contents:entry,resolveDir:path.join(frontend,'src'),loader:'tsx'},plugins:[{name:'vite-raw',setup(build){build.onResolve({filter:/\?raw$/},args=>({path:path.resolve(args.resolveDir,args.path.replace(/\?raw$/,'')),namespace:'raw'}));build.onLoad({filter:/.*/,namespace:'raw'},args=>({contents:fs.readFileSync(args.path,'utf8'),loader:'text'}))}}],bundle:true,jsx:'automatic',define:{'process.env.NODE_ENV':'"production"'},outfile:path.join(run,'app.js')});
 const css=fs.readdirSync(path.join(frontend,'dist/assets')).find(x=>x.endsWith('.css'));fs.copyFileSync(path.join(frontend,'dist/assets',css),path.join(run,'app.css'));
 fs.copyFileSync(path.join(frontend,'public/genesis-ai-icon.png'),path.join(run,'genesis-ai-icon.png'));
 fs.writeFileSync(path.join(run,'index.html'),'<html class="dark" data-shell="modern"><head><meta charset="utf-8"><title>Genesis AI — tutorial capture</title><link rel="stylesheet" href="app.css"></head><body><div id="root"></div><script src="app.js"></script></body></html>');
 session.defaultSession.webRequest.onBeforeRequest((details,cb)=>cb({cancel:/^https?:/.test(details.url)}));
 win=new BrowserWindow({width:1600,height:1000,useContentSize:true,show:process.argv.includes('--show'),webPreferences:{offscreen:!process.argv.includes('--show'),preload:path.join(frontend,'electron/preload.cjs'),sandbox:true,contextIsolation:true,nodeIntegration:false,backgroundThrottling:false}});
 win.webContents.on('console-message',e=>{if(e.level==='error')console.error(e.message)});

 await win.loadFile(path.join(run,'index.html'));await ready('!!document.querySelector("#modern-navigation")');await capture('chat-modern');
 for(const name of ['Chat','Work','Autonomy']){const pos=await js(`(()=>{const r=document.querySelector('[aria-label="'+${JSON.stringify(name)}+'"]')?.getBoundingClientRect();if(!r)throw Error('Missing mode');return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);win.webContents.sendInputEvent({type:'mouseMove',x:Math.round(pos.x),y:Math.round(pos.y)});await delay(1000);await capture('hover-'+name.toLowerCase());}
 await js(`window.demo.store.setState({snapshot:{...window.demo.store.getState().snapshot,mode:'Work',state:'working',status:'Working',loop_running:true,paused:false},feedPlan:[{task:'Read the garden notes',status:'done'},{task:'Draft a watering chart',status:'in_progress'},{task:'Check the chart against the notes',status:'pending'}]})`);await capture('modern-working');
 await js(`window.demo.store.setState({snapshot:{...window.demo.store.getState().snapshot,paused:true,loop_running:false,state:'idle',status:'Paused'}})`);await capture('modern-paused');
 await js(`window.demo.store.setState({snapshot:{...window.demo.store.getState().snapshot,mode:'Chat',paused:false,loop_running:false}})`);await click('Plan');await capture('plan-controls');
 const pos=await js(`(()=>{const e=document.querySelector('button[title="Move down"]');const r=e?.getBoundingClientRect();return r?{x:r.x+5,y:r.y+5}:null})()`);if(pos){win.webContents.sendInputEvent({type:'mouseMove',x:Math.round(pos.x),y:Math.round(pos.y)});await delay(400);await capture('plan-hover');}
 await js(`window.demo.store.setState({view:'missions'})`);await delay(600);await js(`(()=>{const b=[...document.querySelectorAll('button')].find(e=>e.textContent.trim().startsWith('A weekend away'));if(!b)throw Error('Mission row missing');b.click()})()`);await delay(800);await reveal('Sign & start');await capture('mission-sign');
 fs.writeFileSync(path.join(out,'../screens.json'),JSON.stringify(manifest,null,2));win.destroy();app.quit();
}).catch(error=>{console.error(error.stack);app.exit(1)});
