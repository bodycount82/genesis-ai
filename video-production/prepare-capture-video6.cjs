const fs=require('fs'),path=require('path');const root=__dirname;
let c=fs.readFileSync(path.join(root,'capture-video5.cjs'),'utf8').replaceAll('video5','video6').replaceAll('video-05','video-06');
c=c.replace("import {loadVoiceStatus}","import {DesktopControl} from './components/DesktopControl'; import {loadVoiceStatus}");
c=c.replace("api.browserStatus=async()=>({open:false,tabs:[]}); api.desktopStatus=async()=>({active:false,busy:false,control:'user'});",`
let desktop={active:false,busy:false,control:'user',needs_user:false},browser={open:false,tabs:[]};
api.desktopStatus=async()=>desktop;api.desktopControl=async(action)=>{desktop={...desktop,needs_user:action==='take_over',control:action==='take_over'?'user':'ai'};return desktop};
api.browserStatus=async()=>browser;api.browserControl=async(action)=>{browser={...browser,needs_user:action==='take_over',control:action==='take_over'?'user':'ai',requested:false,reason:action==='take_over'?'You have control of the browser':''};return browser};
`);
c=c.replace("api.codeOverview=async()=>({git:{available:true,state:'ready'},folders:[],copies:[],reviews:[]}); api.codeReviews=async()=>({reviews:[]});api.githubAccount=async()=>({connected:false});",`
const practiceFolder='C:/Genesis-Practice/garden-page',copyFolder='C:/Genesis-Practice/garden-page-copy';let github=false;
const folder={path:practiceFolder,name:'garden-page (demonstration)',history:true,snapshots:3,saves:1,branch:'main',in_workspace:false,github:false};
const copy={id:'practice-copy',name:'Larger button experiment',source:practiceFolder,path:copyFolder,status:'open',changed:1,created:1790992800};
api.codeOverview=async()=>({git:{available:true,state:'ready',version:'Git (demonstration)'},folders:[{...folder,github:github?'demo-owner/garden-page':false}],copies:[copy],reviews:[]});
api.codeHistory=async()=>({status:{name:folder.name,unsaved:1,branch:'main',last_save:{message:'Add the garden page',ts:1790992800}},snapshots:[{id:'before-return',label:'Before going back',kind:'before_restore',ts:1790996400,files:1},{id:'before-edit',label:'Before changing button size',kind:'before_edit',ts:1790992800,files:1},{id:'manual',label:'My starting point',kind:'manual',ts:1790989200,files:1}]});
const changes={title:'Practice changes — example only',files:[{path:'style.css',added:1,removed:1}],diff:'diff --git a/style.css b/style.css\\n@@ button size @@\\n-button { padding: 8px; }\\n+button { padding: 14px; }'};
api.codeChanges=async()=>changes;api.codeCopyChanges=async()=>changes;api.codeReviews=async()=>({reviews:[]});api.githubAccount=async()=>github?{connected:true,login:'demo-owner',name:'Demonstration account'}:{connected:false};api.githubRepos=async()=>({repos:[{full_name:'demo-owner/garden-page',name:'garden-page',private:true,description:'Demonstration destination',html_url:'https://github.com/demo-owner/garden-page'}]});
`);
c=c.replace('window.demo={store:useStore,voice:useVoicePresentation,settings:demo,','window.demo={store:useStore,voice:useVoicePresentation,settings:demo,setDesktop:(s)=>{desktop=s},setBrowser:(s)=>{browser=s},setGithub:(s)=>{github=s},');
c=c.replace('<TitleBar/></div>','<TitleBar/></div><DesktopControl connected={true}/>');
c=c.replace("ipcMain.handle('desktop:companion-get',()=>({preferences:{appshotsEnabled:false,appshotsSound:true,petEnabled:false,pet:'hal-voice'},appshotsStatus:'disabled',error:'',pending:0,miniShortcutAvailable:true}));",`
 let companion={preferences:{appshotsEnabled:false,appshotsSound:true,petEnabled:false,pet:'earth'},appshotsStatus:'disabled',error:'',pending:0,miniShortcutAvailable:true};
 ipcMain.handle('desktop:companion-get',()=>companion);ipcMain.handle('desktop:companion-set',(_e,v)=>{companion.preferences={...companion.preferences,...v};return companion});
 const petSvg=req(path.join(frontend,'electron/pets.cjs')).petSvg;ipcMain.handle('mini:get',()=>petSvg('earth'));ipcMain.on('mini:action',()=>{});
 ipcMain.handle('browser:surface',()=>({ok:true}));
`);
let begin=c.indexOf(' await win.loadFile'),end=c.indexOf(" fs.writeFileSync(path.join(out,'../screens.json')",begin);
c=c.slice(0,begin)+`
 await win.loadFile(path.join(run,'index.html'));await ready('!!document.querySelector("#modern-navigation")');await capture('chat-modern');
 await settings('computer');await capture('computer-states');
 await settings('code');await reveal('Your code folders');await capture('code-folder');
 await click('History');await delay(500);await capture('code-history');await click('Changes');await delay(500);await capture('code-changes');
 await click('Safe copies');await delay(400);await capture('code-copy');await click('Changes');await delay(400);await capture('copy-changes');
 await click('GitHub');await delay(400);await capture('github-disconnected');await js('window.demo.setGithub(true)');await click('Overview');await click('GitHub');await delay(400);await capture('github-connected');
 await settings('computer:pet');await capture('pets-top');await reveal('My pets');await capture('pets-list');
 await settings('plugins');await capture('plugins-skills');await click('Plugins');await capture('plugins-import');
 await js('window.demo.store.setState({showSettings:false,view:"plugins"})');await delay(500);await capture('plugins-quick');
 await js('window.demo.store.setState({showSettings:false,view:"chat"});window.demo.setDesktop({active:true,needs_user:false,control:"ai",active_tool:"desktop_read",phase:"between_steps"})');await delay(900);await capture('desktop-active');await click('Take control');await capture('desktop-handoff');await click('Resume AI');await capture('desktop-resumed');await js('window.demo.setDesktop({active:false,needs_user:false})');await delay(900);
 await js('window.demo.setBrowser({open:true,workspace:true,embedded:true,attached:true,session_id:"tutorial-browser",page_id:"practice",tabs:[{page_id:"practice",title:"Practice page (local demo)",url:"about:blank"}],url:"about:blank",control:"ai",needs_user:false,busy:false,working:true,channel:"chromium"});window.demo.voice.setState({desktopBrowserOpen:true})');await delay(1100);await capture('browser-active');await click('Pause AI');await capture('browser-handoff');await click('Resume AI');await capture('browser-resumed');
 const mini=new BrowserWindow({width:166,height:210,useContentSize:true,frame:false,transparent:true,show:false,webPreferences:{preload:path.join(frontend,'electron/mini-preload.cjs'),sandbox:true,contextIsolation:true,nodeIntegration:false,backgroundThrottling:false}});await mini.loadFile(path.join(frontend,'electron/mini.html'));await delay(900);const miniShot=await mini.webContents.capturePage();fs.writeFileSync(path.join(out,'mini.png'),miniShot.toPNG());manifest.screens.mini={file:'mini.png',...miniShot.getSize(),sha256:crypto.createHash('sha256').update(miniShot.toPNG()).digest('hex'),controls:[]};mini.destroy();
`+c.slice(end);
fs.writeFileSync(path.join(root,'capture-video6.cjs'),c);console.log('Video 6 capture prepared');
