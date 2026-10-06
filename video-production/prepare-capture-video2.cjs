const fs=require('node:fs'),path=require('node:path');const root=__dirname;
let c=fs.readFileSync(path.resolve(root,'../tutorials/tools/capture.cjs'),'utf8');
c=c.slice(0,c.indexOf(" await js(`window.demo.scene('wizard')`"));
c=c.replace("path.resolve(__dirname, '../../../Genesis')","path.resolve(__dirname, '../../Genesis')").replace("path.resolve(__dirname, '../assets/screens')","path.resolve(__dirname, 'assets/screens')").replace("path.join(genesis, '.audit-runtime/tutorial-capture')","path.join(__dirname, 'output/video-02/capture-runtime')");
c+=` await js(\`document.querySelector('button[aria-label="Toggle activity"]').click()\`);await capture('chat-context');
 await js(\`document.querySelector('button[aria-label="Toggle activity"]').click()\`);
 await js(\`window.demo.store.setState({messages:[{id:10,role:'user',content:'Read my small practice file and find the planting date.'},{id:11,role:'tool',tool:'read_file',args:{path:'Tutorial Practice/garden-notes.txt'},result:'Plant basil on 12 October. Water lightly. Keep near the kitchen window.',status:'ok'},{id:12,role:'assistant',content:'The planting date in the notes is 12 October.'}]})\`);
 await delay(600);await capture('tool-collapsed');await click('Read');
 await js(\`[...document.querySelectorAll('button')].find(e=>e.textContent.includes('Tutorial Practice/garden-notes.txt')).click()\`);await capture('tool-expanded');
 fs.writeFileSync(path.join(out,'../screens.json'),JSON.stringify(manifest,null,2));win.destroy();app.quit();
}).catch(error=>{console.error(error.stack);app.exit(1)});
`;
fs.writeFileSync(path.join(root,'capture-video2.cjs'),c);


