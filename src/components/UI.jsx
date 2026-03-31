import { useState, useEffect } from 'react';
import { xpForLevel } from '../lib/game';

// --- XP BAR ---
export function XPBar({ current, max, level }) {
  const pct = Math.min((current / max) * 100, 100);
  return (
    <div className="xp-bar">
      <div className="xp-level">LVL {level}</div>
      <div className="xp-track">
        <div className="xp-fill" style={{ width: `${pct}%` }} />
      </div>
      <div className="xp-text">{current}/{max}</div>
    </div>
  );
}

// --- PARTICLES ---
export function Particles({ type = 'dust', count = 20 }) {
  const particles = Array.from({ length: count }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    delay: Math.random() * 5,
    dur: 3 + Math.random() * 4,
    size: type === 'ember' ? 2 + Math.random() * 4 : 1 + Math.random() * 2,
  }));

  const getStyle = (p) => {
    const base = {
      position: 'absolute',
      left: `${p.x}%`,
      width: p.size,
      height: p.size,
      borderRadius: '50%',
      opacity: 0,
    };

    if (type === 'ember') {
      return {
        ...base,
        top: '100%',
        background: '#ff6b35',
        boxShadow: `0 0 ${p.size * 2}px #ff6b35`,
        animation: `floatUp ${p.dur}s ${p.delay}s infinite ease-out`,
      };
    }
    return {
      ...base,
      top: `${p.y}%`,
      background: 'rgba(255,215,100,0.4)',
      animation: `drift ${p.dur}s ${p.delay}s infinite ease-in-out`,
    };
  };

  return (
    <div className="particles">
      {particles.map(p => <div key={p.id} style={getStyle(p)} />)}
    </div>
  );
}

// --- TYPEWRITER ---
export function Typewriter({ lines, speed = 35, lineDelay = 600, onDone }) {
  const [displayed, setDisplayed] = useState('');
  const [lineIdx, setLineIdx] = useState(0);
  const [charIdx, setCharIdx] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (lineIdx >= lines.length) {
      setDone(true);
      onDone?.();
      return;
    }
    if (charIdx <= lines[lineIdx].length) {
      const t = setTimeout(() => {
        setDisplayed(
          lines.slice(0, lineIdx).join('\n') +
          (lineIdx > 0 ? '\n' : '') +
          lines[lineIdx].slice(0, charIdx)
        );
        setCharIdx(c => c + 1);
      }, speed);
      return () => clearTimeout(t);
    } else {
      const t = setTimeout(() => {
        setLineIdx(l => l + 1);
        setCharIdx(0);
      }, lineDelay);
      return () => clearTimeout(t);
    }
  }, [lineIdx, charIdx, lines, speed, lineDelay]);

  return (
    <div className="typewriter">
      {displayed}
      {!done && <span className="cursor">▌</span>}
    </div>
  );
}

// --- LEVEL UP OVERLAY ---
export function LevelUpOverlay({ level, onDone }) {
  useEffect(() => {
    const t = setTimeout(onDone, 2500);
    return () => clearTimeout(t);
  }, [onDone]);

  return (
    <div className="level-up-overlay">
      <div className="level-up-content">
        <div className="level-up-icon">⚔️</div>
        <div className="level-up-label">Level Up</div>
        <div className="level-up-number">{level}</div>
        <div className="level-up-subtitle">Your power grows stronger...</div>
      </div>
    </div>
  );
}

// --- QUEST CARD ---
export function QuestCard({ quest, onComplete, index }) {
  const [completing, setCompleting] = useState(false);
  const [showReward, setShowReward] = useState(false);
  const completed = !!quest.completed_at;

  const typeColor =
    quest.quest_type === 'boss' ? '#ff4444' :
    quest.quest_type === 'side' ? '#88cc55' : '#5599ff';

  const handleClick = () => {
    if (completed || completing) return;
    setCompleting(true);
    setTimeout(() => {
      setShowReward(true);
      setTimeout(() => {
        onComplete(quest);
        setCompleting(false);
        setShowReward(false);
      }, 1000);
    }, 500);
  };

  return (
    <div
      className={`quest-card ${completed ? 'completed' : ''}`}
      onClick={handleClick}
      style={{
        borderColor: completed ? 'rgba(255,255,255,0.05)' : `${typeColor}22`,
        animationDelay: `${index * 0.1}s`,
      }}
    >
      {showReward && (
        <div className="quest-reward-popup">
          <div className="quest-reward-icon">⚡</div>
          <div className="quest-reward-text" style={{ color: '#ffd700' }}>
            +{quest.xp_reward} XP &nbsp; +{quest.gold_reward} Gold
          </div>
        </div>
      )}

      {completing && !showReward && (
        <div className="quest-sweep" style={{ background: `${typeColor}33` }} />
      )}

      <div className="quest-inner">
        <div className="quest-icon" style={{ filter: completed ? 'grayscale(1)' : 'none' }}>
          {quest.icon}
        </div>
        <div className="quest-body">
          <div className="quest-meta">
            <span className="quest-type-badge" style={{ color: typeColor, borderColor: `${typeColor}44` }}>
              {quest.quest_type?.toUpperCase()}
            </span>
            <span className="quest-diff">Floor {quest.sort_order + 1} · {quest.difficulty}</span>
          </div>
          <div className={`quest-name ${completed ? 'done' : ''}`}>{quest.quest_name}</div>
          <div className="quest-lore">{quest.quest_lore}</div>
          <div className="quest-task">🎯 {quest.original_task}</div>
          <div className="quest-rewards">
            <span style={{ color: '#ffd700' }}>⚡ {quest.xp_reward} XP</span>
            <span style={{ color: '#ffaa00' }}>🪙 {quest.gold_reward} Gold</span>
          </div>
        </div>
        {!completed && <div className="quest-check" style={{ borderColor: typeColor }}>✓</div>}
        {completed && <div className="quest-done-icon">💀</div>}
      </div>
    </div>
  );
}
