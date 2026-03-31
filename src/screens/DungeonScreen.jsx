import { useState } from 'react';
import { useGame } from '../context/GameContext';
import { XPBar, QuestCard, Typewriter, Particles } from '../components/UI';

export default function DungeonScreen() {
  const { day, quests, level, xp, gold, xpToNext, completedCount, allCompleted, handleCompleteQuest, goToBonfire } = useGame();
  const [introDone, setIntroDone] = useState(false);

  const introLines = day?.intro_text
    ? day.intro_text.split('. ').filter(s => s.length > 0).map(s => s.trim() + (s.endsWith('.') ? '' : '.'))
    : ['You descend into the depths...', 'Your quests await.'];

  return (
    <div className="dungeon-screen">
      <Particles type="dust" count={8} />

      {/* Sticky header */}
      <div className="dungeon-header">
        <div className="dungeon-header-inner">
          <div className="dungeon-header-top">
            <div className="dungeon-floor">
              {day?.dungeon_name || 'THE DUNGEON'}
            </div>
            <div className="dungeon-stats-mini">
              <span style={{ color: '#ff6666' }}>❤️ 100</span>
              <span style={{ color: '#ffaa00' }}>🪙 {gold}</span>
            </div>
          </div>
          <XPBar current={xp} max={xpToNext} level={level} />
          <div className="dungeon-progress">
            {completedCount}/{quests.length} quests completed
          </div>
        </div>
      </div>

      {/* Intro */}
      {!introDone && (
        <div className="dungeon-intro">
          <Typewriter
            lines={introLines}
            speed={30}
            lineDelay={500}
            onDone={() => setTimeout(() => setIntroDone(true), 2000)}
          />
        </div>
      )}

      {/* Quest list */}
      <div className="quest-list">
        {quests
          .sort((a, b) => a.sort_order - b.sort_order)
          .map((q, i) => (
            <QuestCard
              key={q.id}
              quest={q}
              index={i}
              onComplete={handleCompleteQuest}
            />
          ))}
      </div>

      {/* Bonfire button */}
      {allCompleted && (
        <div className="dungeon-complete fade-slide-in">
          <div className="dungeon-complete-divider" />
          <p className="dungeon-complete-text">
            The dungeon falls silent. All foes vanquished.
          </p>
          <button className="btn-bonfire" onClick={goToBonfire}>
            🔥 Rest at Bonfire
          </button>
        </div>
      )}
    </div>
  );
}
