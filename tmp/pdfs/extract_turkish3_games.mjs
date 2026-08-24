import fs from 'node:fs';

const sourcePath = new URL('../../app/src/main/assets/macera-akademi.html', import.meta.url);
const source = fs.readFileSync(sourcePath, 'utf8');
const arrays = [
  'TR3_TEMA1', 'TR3_TEMA2', 'TR3_TEMA3', 'TR3_TEMA4',
  'TR3_TEMA5', 'TR3_TEMA6', 'TR3_TEMA7', 'TR3_TEMA8'
];

function extractArray(name) {
  const marker = `const ${name} = [`;
  const markerAt = source.indexOf(marker);
  if (markerAt < 0) throw new Error(`Array not found: ${name}`);
  const start = source.indexOf('[', markerAt);
  const endMarker = `\n];\n${name}.forEach`;
  const end = source.indexOf(endMarker, start);
  if (end < 0) throw new Error(`Array end not found: ${name}`);
  const literal = source.slice(start, end + 2);
  return Function(`"use strict"; return (${literal});`)();
}

const games = arrays.flatMap(extractArray).map(game => ({
  id: game.id,
  group: game.grp,
  title: game.title,
  subtitle: game.sub,
  outcome: game.kaz,
  type: game.type,
  instruction: game.cfg?.instruction || '',
  speak: game.cfg?.speak || '',
  rounds: game.cfg?.rounds?.length || game.cfg?.steps?.length || 1,
  config: game.cfg || {}
}));

if (process.argv.includes('--stats')) {
  const byType = Object.fromEntries([...new Set(games.map(game => game.type))].map(type => [type, games.filter(game => game.type === type).length]));
  const byGroup = Object.fromEntries([...new Set(games.map(game => game.group))].map(group => [group, games.filter(game => game.group === group).length]));
  const writingOutcomes = games.filter(game => /T\.Y\./.test(game.outcome)).length;
  const speakingOutcomes = games.filter(game => /T\.K\./.test(game.outcome)).length;
  const listeningOutcomes = games.filter(game => /T\.D\./.test(game.outcome)).length;
  process.stdout.write(JSON.stringify({count: games.length, byType, byGroup, writingOutcomes, speakingOutcomes, listeningOutcomes}, null, 2));
} else if (process.argv.includes('--titles')) {
  process.stdout.write(JSON.stringify(games.map(game => game.title)));
} else if (process.argv.includes('--ids')) {
  process.stdout.write(JSON.stringify(games.map(game => ({id: game.id, title: game.title, type: game.type}))));
} else if (process.argv.includes('--full')) {
  process.stdout.write(JSON.stringify(games, null, 2));
} else {
  process.stdout.write(JSON.stringify(games.map(({config, ...game}) => game), null, 2));
}
