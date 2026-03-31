// System prompt moved to server-side (api/generate-quests.js)

// --- SMART DIFFICULTY ESTIMATION ---
function estimateDifficulty(task) {
  const lower = task.toLowerCase();

  // 1. Parse explicit time: "30 min", "1h", "2 hours", "~45min"
  let minutes = null;
  const timePatterns = [
    { re: /(\d+)\s*h(?:ours?|r)?/i, mult: 60 },
    { re: /(\d+)\s*min(?:utes?)?/i, mult: 1 },
    { re: /~\s*(\d+)\s*m/i, mult: 1 },
    { re: /(\d+)\s*час/i, mult: 60 },
    { re: /(\d+)\s*мин/i, mult: 1 },
  ];
  for (const p of timePatterns) {
    const m = lower.match(p.re);
    if (m) { minutes = parseInt(m[1]) * p.mult; break; }
  }

  // 2. Keyword scoring
  const hard = /report|project|presentation|study|course|learn|workout|training|exercise|gym|code|develop|build|write|essay|exam|deadline|тренировк|учить|учёб|проект|отчёт|разработ|программ|упражн/i;
  const medium = /email|meeting|call|cook|clean|read|plan|review|organize|shop|groceries|laundry|готов|почист|убра|уборк|позвон|совещан|читать|план/i;
  const easy = /brush|teeth|water|walk|stretch|meditat|vitamin|pill|bed|shower|journal|gratitude|зубы|вод[аы]|прогулк|растяж|душ|витамин|таблетк|зарядк/i;

  let score;
  if (minutes !== null) {
    score = minutes <= 10 ? 1 : minutes <= 30 ? 2 : minutes <= 60 ? 3 : 4;
  } else if (hard.test(lower)) {
    score = 3 + Math.random() * 0.5;
  } else if (easy.test(lower)) {
    score = 0.5 + Math.random() * 0.5;
  } else if (medium.test(lower)) {
    score = 2 + Math.random() * 0.5;
  } else {
    score = 2;
  }

  const difficulty = score <= 1.2 ? 'easy' : score >= 3 ? 'hard' : 'medium';
  return { difficulty, score, minutes };
}

// Fallback quest templates
const TEMPLATES = [
  { prefix: 'The Ancient', suffix: 'Trial', icons: ['⚔️', '🗡️', '🏰'], lores: ['A relic of discipline demands your attention.', 'The old ways call for mastery.'] },
  { prefix: 'Shadow of the', suffix: 'Beast', icons: ['👹', '🦇', '🕷️'], lores: ['It lurks in the corners of your schedule.', 'A creature born from avoidance grows stronger.'] },
  { prefix: 'The Lost', suffix: 'Scroll', icons: ['📜', '📚', '🔮'], lores: ['Knowledge awaits those who dare seek it.', 'The tome whispers secrets of forgotten craft.'] },
  { prefix: 'Echoes of the', suffix: 'Forge', icons: ['🔥', '⚒️', '💎'], lores: ['The anvil rings with purpose.', 'Heat and pressure create something beautiful.'] },
  { prefix: 'The Whispering', suffix: 'Gate', icons: ['🌑', '🕯️', '🗝️'], lores: ['A threshold between intention and action.', 'The gate opens only for the determined.'] },
  { prefix: 'Rift of the', suffix: 'Mind', icons: ['🧠', '⚡', '🌀'], lores: ['Your thoughts crystallize into challenge.', 'Mental fortitude is the sharpest blade.'] },
  { prefix: 'The Sunken', suffix: 'Vault', icons: ['🪙', '💰', '🏺'], lores: ['Treasures buried beneath procrastination.', 'The vault yields only to the persistent.'] },
];

const DUNGEON_NAMES = [
  'The Crypt of Unfinished Business', 'The Labyrinth of Deadlines', 'The Halls of Hustle',
  'The Cavern of Ambition', 'The Forgotten Mines of Focus', 'The Tower of Tasks Undone', 'The Depths of Discipline',
];

const INTROS = [
  'You descend the spiral stairs. Torchlight flickers against damp stone walls. The air tastes like unfinished business.',
  'The dungeon gate groans open. Somewhere in the darkness, your tasks have taken monstrous form. Steel yourself.',
  'Cold wind rushes past. The dungeon knows you are here. It has been waiting since dawn.',
  'Ancient mechanisms click into place. The floor descends. Today\'s challenges materialize from shadow.',
];

function generateFallbackQuests(tasks) {
  const analyzed = tasks.map((task, i) => ({
    task,
    ...estimateDifficulty(task),
    template: TEMPLATES[i % TEMPLATES.length],
  }));

  // Sort easy → hard, boss is last
  analyzed.sort((a, b) => a.score - b.score);

  const xpMap = { easy: () => 10 + Math.floor(Math.random() * 8), medium: () => 20 + Math.floor(Math.random() * 15), hard: () => 40 + Math.floor(Math.random() * 20) };
  const goldMap = { easy: () => 5 + Math.floor(Math.random() * 5), medium: () => 8 + Math.floor(Math.random() * 8), hard: () => 18 + Math.floor(Math.random() * 12) };

  const quests = analyzed.map((item, i) => {
    const t = item.template;
    const word = item.task.split(' ').slice(0, 2).join(' ');
    const isLast = i === analyzed.length - 1;
    const isFirst = i === 0 && analyzed.length > 2;
    const type = isLast ? 'boss' : isFirst ? 'side' : 'quest';
    const lore = t.lores[Math.floor(Math.random() * t.lores.length)];

    return {
      name: `${t.prefix} ${word} ${t.suffix}`,
      lore,
      type,
      difficulty: item.difficulty,
      xp: xpMap[item.difficulty](),
      gold: goldMap[item.difficulty](),
      icon: isLast ? '🐉' : t.icons[Math.floor(Math.random() * t.icons.length)],
      original_task: item.task,
    };
  });

  return {
    dungeon_name: DUNGEON_NAMES[Math.floor(Math.random() * DUNGEON_NAMES.length)],
    intro: INTROS[Math.floor(Math.random() * INTROS.length)],
    quests,
  };
}

export async function generateQuests(tasks) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);

    const response = await fetch('/api/generate-quests', {
      method: 'POST',
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tasks }),
    });

    clearTimeout(timeout);
    if (!response.ok) throw new Error(`API error: ${response.status}`);

    const parsed = await response.json();

    if (!parsed.quests || !Array.isArray(parsed.quests)) {
      throw new Error('Invalid quest structure');
    }

    return parsed;
  } catch (err) {
    console.error('AI generation failed, using fallback:', err);
    return generateFallbackQuests(tasks);
  }
}

// XP/Level calculations
export function xpForLevel(level) {
  return 40 + level * 25;
}

export function calculateLevelUp(currentXp, currentLevel, xpGained) {
  let xp = currentXp + xpGained;
  let level = currentLevel;
  let leveledUp = false;

  while (xp >= xpForLevel(level)) {
    xp -= xpForLevel(level);
    level++;
    leveledUp = true;
  }

  return { xp, level, leveledUp };
}

// Day number from date
export function getDayNumber(startDate) {
  const start = new Date(startDate);
  const now = new Date();
  start.setHours(0, 0, 0, 0);
  now.setHours(0, 0, 0, 0);
  const diff = Math.floor((now - start) / (1000 * 60 * 60 * 24));
  return Math.min(diff + 1, 7);
}

export function getDayName(dayNumber) {
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  return days[(dayNumber - 1) % 7];
}

export { estimateDifficulty };
