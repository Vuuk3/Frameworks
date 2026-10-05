import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const dir=new URL('.',import.meta.url);
async function read(name){const w=await Workbook.fromCSV((await fs.readFile('C:/Users/User/Downloads/'+name,'utf8')).replace(/^\uFEFF/,''),{sheetName:'CSV'});return w.worksheets.getItemAt(0).getUsedRange().values.slice(1).filter(r=>r[1]);}
const existing=await SpreadsheetFile.importXlsx(await FileBlob.load(fileURLToPath(new URL('Алхимия.xlsx',dir))));
const oldEffects=existing.worksheets.getItem('Эффекты').getRange('A2:AG16').values;
const oldTraits=existing.worksheets.getItem('Ингредиенты').getRange('A2:F16').values;
const effects=await read('ingredients_effects.csv'), traits=await read('ingredients_traits.csv');
async function json(name){return JSON.parse((await fs.readFile('C:/Users/User/Downloads/'+name,'utf8')).replace(/^\uFEFF/,''));}
const newEffects=await json('ingredients_effects_updated.json'),newTraits=await json('ingredients_traits_updated.json');
for(const [base,updated] of [[await json('ingredients_effects.json'),newEffects],[await json('ingredients_traits.json'),newTraits]])for(const r of base){if(!updated.some(u=>JSON.stringify(u)===JSON.stringify(r)))throw Error('Original JSON is not subset of updated');}
for(const r of newEffects)effects.push([r.file,r.ingredient,r.effect,r.value]);
for(const r of newTraits)traits.push([r.file,r.ingredient,r.focus,r.form,r.safety,r.aspect]);
const batchTraits=await json('ingredients_traits(1).json'),batchEffects=await json('ingredients_effects(1).json');
const duplicateNames=new Set(batchTraits.filter((r,i,a)=>a.findIndex(x=>x.ingredient===r.ingredient)!==i).map(r=>r.ingredient));
const batchName=new Map(batchTraits.map(r=>[r.file,duplicateNames.has(r.ingredient)?`${r.ingredient} (${r.aspect})`:r.ingredient]));
for(const r of batchEffects)effects.push([r.file,batchName.get(r.file)||r.ingredient,r.effect,r.value]);
for(const r of batchTraits)traits.push([r.file,batchName.get(r.file),r.focus,r.form,r.safety,r.aspect]);
const pasted=JSON.parse((await fs.readFile('C:/Users/User/.codex/attachments/cee3b0bf-4aeb-4fc1-a6d9-055720bd0b2f/Вставленный текст.txt','utf8')).replace(/^\uFEFF/,''));
const pastedNames=new Set(pasted.map(r=>r.ingredient));
for(const r of pasted){
 const prior=traits.filter(x=>x[1]===r.ingredient);
 const distinct=prior.some(x=>x[0]!==r.file&&(x[5]!==r.aspect||JSON.stringify(x.slice(2,5))!==JSON.stringify([r.focus,r.form,r.safety])));
 if(distinct){for(const x of traits)if(x[1]===r.ingredient)x[1]=`${x[1]} (${x[5]})`;for(const x of effects)if(x[1]===r.ingredient)x[1]=`${x[1]} (${prior[0][5]})`;r.ingredient=`${r.ingredient} (${r.aspect})`;}
 traits.push([r.file,r.ingredient,r.focus,r.form,r.safety,r.aspect]);
 for(const x of r.effects)effects.push([r.file,r.ingredient,x.effect,x.value]);
}
const more=[
 ...JSON.parse(await fs.readFile('C:/Users/User/.codex/attachments/306af1fd-a790-4752-9d56-5ca1f6b6c4e3/Вставленный текст.txt','utf8')),
 ...JSON.parse(await fs.readFile('C:/Users/User/.codex/attachments/8e0e9ae0-0781-453a-af52-ca2d434845db/Вставленный текст.txt','utf8')),
 ...JSON.parse(await fs.readFile(new URL('inline_batch.json',dir),'utf8')),
];
const canonForm=x=>({'взрывной':'взрывное','туманный':'туманное','жидкий':'жидкое','газообразный':'туманное'}[String(x).toLowerCase()]||x||'-');
const canonSafety=x=>String(x||'-').toLowerCase()==='неизвестно'?'-':({'идеальный':'Идеальный','стабильный':'Стабильный','утончённый':'Утончённый','утонченный':'Утончённый','сбалансированный':'Сбалансированный','нестабильный':'Нестабильный','летучий':'Летучий','хаотичный':'Хаотичный'}[String(x).toLowerCase()]||x||'-');
const canonUnknown=x=>String(x||'-').toLowerCase()==='неизвестно'?'-':x||'-';
const aliasEffect=x=>({'Весенние':'Везение','Холодостойкость':'Хладостойкость','Насыщенность':'Насыщение'}[x]||x);
const recordSig=r=>JSON.stringify([r.ingredient,canonUnknown(r.focus),canonForm(r.form),canonSafety(r.safety),canonUnknown(r.aspect),[...new Map([...(r.effects||[])].map(x=>[`${aliasEffect(x.effect)}\0${Number(x.value)}`,[aliasEffect(x.effect),Number(x.value)]])).values()].sort((a,b)=>a[0].localeCompare(b[0]))]);
const known=new Set(traits.map(r=>recordSig({file:r[0],ingredient:r[1],focus:r[2],form:r[3],safety:r[4],aspect:r[5],effects:effects.filter(x=>x[0]===r[0]).map(x=>({effect:x[2],value:x[3]}))})));
const timeTag=f=>(f.match(/_(\d\d\.\d\d\.\d\d)/)||[])[1]||f;
function renameCollision(raw,r){
 const prior=traits.filter(x=>x[1]===raw),differentAspect=prior.some(x=>x[5]!==r.aspect);
 for(const x of prior)x[1]=`${raw} (${differentAspect?x[5]:timeTag(x[0])})`;
 for(const x of effects)if(x[1]===raw){const p=prior.find(t=>t[0]===x[0])||prior[0];x[1]=`${raw} (${differentAspect?p[5]:timeTag(x[0])})`;}
 return `${raw} (${differentAspect?r.aspect:timeTag(r.file)})`;
}
for(const source of more){
 const r={...source,effects:source.effects.filter(x=>String(x.effect).toLowerCase()!=='неизвестно').map(x=>({...x,effect:aliasEffect(x.effect)}))};
 const sig=recordSig(r);if(known.has(sig))continue;
 if(traits.some(x=>x[1]===r.ingredient))r.ingredient=renameCollision(r.ingredient,r);
 r.focus=canonUnknown(r.focus);r.form=canonForm(r.form);r.safety=canonSafety(r.safety);r.aspect=canonUnknown(r.aspect);
 traits.push([r.file,r.ingredient,r.focus,r.form,r.safety,r.aspect]);
 for(const x of r.effects)effects.push([r.file,r.ingredient,x.effect,x.value]);
 known.add(recordSig(r));
}
const names=[...new Set([...traits,...effects].map(r=>r[1]))];
const types=['Везение','Водное дыхание','Выздоровление','Голод','Замедление','Иссушение','Коррозия','Левитация','Невезение','Невидимость','Ночное зрение','Огнестойкость','Отравление','Плавное падение','Прилив здоровья','Прыгучесть','Регенерация','Свечение','Сила','Скалковая близость','Скорость','Слабость','Слепота','Сопротивление','Спешка','Тошнота','Тьма','Утомление','Хладостойкость','Исцеление','Моментальный урон','Насыщение'];
const rows=new Map(names.map(n=>[n,{}]));
const aliases={'Весенние':'Везение','Холодостойкость':'Хладостойкость','Насыщенность':'Насыщение'};
for(const [file,n,raw,v] of effects){const e=aliases[raw]||raw;if(!types.includes(e))throw Error(e);const value=v==='-'?'-':Number(v);if(value!=='-'&&!Number.isFinite(value))throw Error('Invalid value');if(rows.get(n)[e]!==undefined&&rows.get(n)[e]!==value)throw Error('Conflict');rows.get(n)[e]=value;}
const w=existing;
const e=w.worksheets.getItem('Эффекты'), t=w.worksheets.getItem('Ингредиенты');
for(const s of [e,t]){for(const table of [...s.tables.items])table.delete();s.getUsedRange().clear();s.getUsedRange().conditionalFormats.deleteAll();}
e.getRange('A1').write([['Ингредиент',...types],...names.map(n=>[n,...types.map(k=>rows.get(n)[k]??0)])]);
const forms={'взрывной':'взрывное','туманный':'туманное','жидкий':'жидкое','газообразный':'туманное'};
t.getRange('A1').write([['Ингредиент','Сила/длительность','Форма зелья','Безопасность','Аспект','Исходный скриншот'],...names.map(n=>{const r=traits.find(r=>r[1]===n);if(!r)throw Error('Missing traits '+n);return [n,r[2]||'-',forms[r[3]]||r[3]||'-',r[4]||'-',r[5]||'-',r[0]];})]);
for(const [s,last,table] of [[e,'AG','EffectsTable'],[t,'F','IngredientsTable']]){
 const range=s.getRange(`A1:${last}${names.length+1}`);range.format.font={name:'Arial',size:11};range.format.rowHeight=32;range.format.verticalAlignment='center';
 s.tables.add(`A1:${last}${names.length+1}`,true,table);
 s.getRange(`A1:${last}1`).format={fill:'#40334F',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},wrapText:true,rowHeight:48};
 s.getRange(`A1:${last}${names.length+1}`).format.columnWidth=20;
 s.getRange(`A1:A${names.length+1}`).format.columnWidth=48;s.getRange(`A2:A${names.length+1}`).format.wrapText=true;s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);
}
const end=names.length+1,note=end+3;
t.getRange(`B1:B${end}`).format.columnWidth=28;t.getRange(`D1:D${end}`).format.columnWidth=25;t.getRange(`F1:F${end}`).format.columnWidth=38;
e.getRange(`B2:AG${end}`).setNumberFormat('0');e.getRange(`B2:AG${end}`).format.horizontalAlignment='right';
t.getRange(`B2:E${end}`).conditionalFormats.add('containsText',{text:'-',format:{fill:'#FFF2CC'}});
e.getRange(`A${note}`).values=[['Источники: CSV, JSON-файлы и вставленная партия данных']];e.getRange(`A${note+1}`).values=[['0 — эффект отсутствует; - — значение неизвестно.']];e.getRange(`A${note+2}`).values=[['Названия приведены к списку: Весенние → Везение; Холодостойкость → Хладостойкость; Насыщенность → Насыщение.']];
e.getRange(`A${note+3}`).values=[['Эффекты без указанного названия пропущены: Сердце Дома, Плазматический скалк.']];
t.getRange(`A${note}`).values=[['Источники: CSV, JSON-файлы и вставленная партия данных']];t.getRange(`A${note+1}`).values=[['Неизвестные свойства обозначены знаком -.']];
if(JSON.stringify(oldEffects)!==JSON.stringify(e.getRange('A2:AG16').values)||JSON.stringify(oldTraits)!==JSON.stringify(t.getRange('A2:F16').values))throw Error('Existing records changed');
for(const n of names){const variants=traits.filter(r=>r[1]===n).map(r=>JSON.stringify(r.slice(2,6)));if(new Set(variants).size>1)throw Error('Conflicting traits '+n);}
for(const s of [e,t])console.log((await w.inspect({kind:'table',range:`${s.name}!A1:F5`,include:'values',tableMaxRows:5,tableMaxCols:6})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A',options:{useRegex:true,maxResults:20}})).ndjson);
for(const [s,r] of [[e,'A72:F108'],[t,'A72:F108']]){const blob=await w.render({sheetName:s.name,range:r,scale:1.5});await fs.writeFile(new URL(s===e?'effects.png':'traits.png',dir),new Uint8Array(await blob.arrayBuffer()));}
await (await SpreadsheetFile.exportXlsx(w)).save(fileURLToPath(new URL('Алхимия.xlsx',dir)));
console.log(JSON.stringify({ingredients:names.length,effectRows:effects.length}));
