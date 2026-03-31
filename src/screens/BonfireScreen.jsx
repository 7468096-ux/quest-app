import { useState } from 'react';
import { useGame } from '../context/GameContext';
import { Particles } from '../components/UI';
import { getDayNumber } from '../lib/game';

const QUOTES = [
  'The flames dance softly. Another day survived.',
  'Rest now, adventurer. Tomorrow brings new trials.',
  'Your strength grows with each challenge conquered.',
];

export default function BonfireScreen() {
  const { run, day, quests, level, saveReflection, nextDay } = useGame();
  const [reflection, setReflection] = useState(day?.reflection || '');
  const [saved, setSaved] = useState(!!day?.reflection);

  const dayNumber = run ? getDayNumber(run.started_at) : 1;
  const totalXp = quests.reduce((s, q) => s + (q.completed_at ? q.xp_reward : 0), 0);
  const totalGold = quests.reduce((s, q) => s + (q.completed_at ? q.gold_reward : 0), 0);
  const completedCount = quests.filter(q => q.completed_at).length;
  const boss = quests.find(q => q.quest_type === 'boss' && q.completed_at);
  const quote = QUOTES[Math.floor(Math.random() * QUOTES.length)];

  async function handleSave() {
    await saveReflection(reflection);
    setSaved(true);
  }

  return (
    <div className="screen-center">
      <Particles type="ember" count={30} />
      <div className="bonfire-glow" />

      <div className="bonfire-content fade-in">
        <div className="bonfire-fire">🔥</div>
        <div className="bonfire-label">Bonfire Rest</div>
        <h2 className="bonfire-title">Day {dayNumber} Complete</h2>
        <p className="bonfire-quote">{quote}</p>

        {/* Stats */}
        <div className="bonfire-stats">
          <div className="bonfire-stats-grid">
            {[
              { icon: '⚔️', value: `${completedCount}/${quests.length}`, label: 'Quests', color: '#5599ff' },
              { icon: '⚡', value: totalXp, label: 'XP Gained', color: '#ffd700' },
              { icon: '🪙', value: totalGold, label: 'Gold Earned', color: '#ffaa00' },
              { icon: '🏅', value: level, label: 'Level', color: '#ff8c00' },
            ].map((s, i) => (
              <div key={i} className="bonfire-stat" style={{ animationDelay: `${0.3 + i * 0.1}s` }}>
                <div className="bonfire-stat-icon">{s.icon}</div>
                <div className="bonfire-stat-value" style={{ color: s.color }}>{s.value}</div>
                <div className="bonfire-stat-label">{s.label}</div>
              </div>
            ))}
          </div>

          {boss && (
            <>
              <div className="bonfire-divider" />
              <div className="bonfire-boss-label">BOSS SLAIN</div>
              <div className="bonfire-boss-name">{boss.icon} {boss.quest_name}</div>
            </>
          )}
        </div>

        {/* Reflection */}
        <div className="bonfire-reflection fade-slide-in" style={{ animationDelay: '0.6s' }}>
          <p className="bonfire-reflection-prompt">"What went well today, adventurer?"</p>
          <textarea
            className="bonfire-textarea"
            value={reflection}
            onChange={e => { setReflection(e.target.value); setSaved(false); }}
            placeholder="Today I conquered..."
            rows={3}
          />
          {!saved && reflection.length > 0 && (
            <button className="btn-secondary" onClick={handleSave} style={{ marginTop: 8 }}>
              Save Reflection
            </button>
          )}
          {saved && <div className="bonfire-saved">✓ Saved</div>}
        </div>

        {/* Next day */}
        <div className="bonfire-actions fade-slide-in" style={{ animationDelay: '0.9s' }}>
          <button className="btn-gold-outline" onClick={nextDay}>
            Next Day →
          </button>
        </div>

        <div className="bonfire-footer">
          Day {dayNumber} of 7 · {7 - dayNumber} days until permadeath
        </div>
      </div>
    </div>
  );
}
