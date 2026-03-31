import { useState } from 'react';
import { useGame } from '../context/GameContext';
import { Particles } from '../components/UI';

export default function OracleScreen() {
  const { generateDungeon } = useGame();
  const [tasks, setTasks] = useState('');

  function handleGenerate() {
    const lines = tasks
      .split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 0);

    if (lines.length === 0) return;
    generateDungeon(lines);
  }

  return (
    <div className="screen-center">
      <Particles type="dust" count={12} />
      <div className="oracle-content fade-in">
        <div className="oracle-icon">🕯️</div>
        <h2 className="oracle-title">The Oracle Awaits</h2>
        <p className="oracle-subtitle">Speak your goals, adventurer. What must be conquered today?</p>

        <textarea
          className="oracle-input"
          value={tasks}
          onChange={e => setTasks(e.target.value)}
          placeholder={"Finish quarterly report\nAnswer 5 emails\n30 min workout\nCook healthy dinner\nStudy LLM course — 1 hour"}
          rows={6}
        />

        <div className="oracle-hint">one task per line · the Oracle does the rest</div>

        <button className="btn-gold" onClick={handleGenerate}>
          Generate Dungeon
        </button>
      </div>
    </div>
  );
}
