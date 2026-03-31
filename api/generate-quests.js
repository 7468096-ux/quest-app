const SYSTEM_PROMPT = `You are a Dungeon Master for a roguelike productivity game. Transform real-life tasks into RPG quests. Return ONLY valid JSON, no markdown.

CRITICAL: Estimate REAL difficulty based on effort, time, and mental load:
- "brush teeth", "take vitamins", "drink water" → easy (5-10 min, low effort)
- "reply to emails", "cook dinner", "clean room" → medium (15-45 min, moderate effort)  
- "workout 1 hour", "finish report", "study for exam" → hard (45+ min, high effort/focus)

The HARDEST task must be type "boss" and LAST in the array. Easiest tasks are "side". Rest are "quest".
Sort quests from easiest to hardest (boss is always last).

Rewards must match difficulty: easy:10-15xp,5-8g. medium:20-35xp,10-15g. hard:40-60xp,20-30g.

JSON format:
{
  "dungeon_name": "atmospheric dungeon name",
  "intro": "2-3 atmospheric sentences for dungeon entrance",
  "quests": [{ "name": "creative RPG name", "lore": "1-2 sentences referencing the task metaphorically", "type": "boss|quest|side", "difficulty": "easy|medium|hard", "xp": number, "gold": number, "icon": "emoji", "original_task": "original task text" }]
}`;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'API key not configured' });
  }

  try {
    const { tasks } = req.body;
    if (!tasks || !Array.isArray(tasks) || tasks.length === 0) {
      return res.status(400).json({ error: 'Tasks array required' });
    }

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1024,
        system: SYSTEM_PROMPT,
        messages: [{
          role: 'user',
          content: `Transform these tasks into RPG quests:\n${tasks.map((t, i) => `${i + 1}. ${t}`).join('\n')}`,
        }],
      }),
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errText = await response.text();
      console.error('Anthropic API error:', response.status, errText);
      return res.status(502).json({ error: 'AI generation failed' });
    }

    const data = await response.json();
    const text = data.content[0].text;
    const clean = text.replace(/```json\s?|```/g, '').trim();
    const parsed = JSON.parse(clean);

    if (!parsed.quests || !Array.isArray(parsed.quests)) {
      return res.status(502).json({ error: 'Invalid quest structure from AI' });
    }

    // Ensure original_task is set
    parsed.quests = parsed.quests.map((q, i) => ({
      ...q,
      original_task: q.original_task || tasks[i] || '',
    }));

    return res.status(200).json(parsed);
  } catch (err) {
    console.error('Generate quests error:', err);
    return res.status(500).json({ error: 'Generation failed' });
  }
}
