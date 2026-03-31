import { useGame } from '../context/GameContext';
import { Particles } from '../components/UI';
import { getDayNumber, getDayName } from '../lib/game';

export default function TitleScreen() {
  const { run, level, xp, gold, enterDungeon, xpToNext } = useGame();
  const dayNumber = run ? getDayNumber(run.started_at) : 1;
  const dayName = getDayName(dayNumber);

  return (
    <div className="screen-center">
      <Particles type="dust" count={25} />
      <div className="title-content fade-in">
        <div className="title-meta">
          Week {run?.run_number || 1} · Run #{run?.run_number || 1} · Day {dayNumber}/7
        </div>

        <h1 className="title-main">THE DUNGEON</h1>
        <div className="title-sub">of {dayName}</div>

        <div className="title-divider" />

        <p className="title-quote">
          "Every morning you enter the dungeon.<br />
          Every evening you rest by the fire.<br />
          Every Sunday... you die."
        </p>

        <div className="title-stats">
          <span>❤️ <b style={{ color: '#ff6666' }}>100</b></span>
          <span>⚡ <b style={{ color: '#ffd700' }}>{xp}/{xpToNext}</b></span>
          <span>🪙 <b style={{ color: '#ffaa00' }}>{gold}</b></span>
        </div>

        <button className="btn-gold" onClick={enterDungeon}>
          Enter Dungeon
        </button>

        <div className="title-class">
          ▸ Class: Shadow Coder · Level {level}
        </div>
      </div>
    </div>
  );
}
