import { useState } from 'react';
import { useGame } from '../context/GameContext';
import { Particles } from '../components/UI';

export default function OracleScreen() {
  const { generateDungeon, aiApiKey, saveApiKey } = useGame();
  const [tasks, setTasks] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [keyInput, setKeyInput] = useState(aiApiKey);

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

        <button
          className="oracle-settings-toggle"
          onClick={() => setShowSettings(!showSettings)}
        >
          ⚙️ {showSettings ? 'Hide' : 'AI'} Settings
        </button>

        {showSettings && (
          <div className="oracle-settings fade-in">
            <label className="settings-label">Anthropic API Key (optional)</label>
            <input
              type="password"
              className="input-field"
              value={keyInput}
              onChange={e => setKeyInput(e.target.value)}
              placeholder="sk-ant-..."
            />
            <button
              className="btn-secondary"
              onClick={() => {
                saveApiKey(keyInput);
                setShowSettings(false);
              }}
            >
              Save Key
            </button>
            <p className="settings-note">
              Without a key, quests use template generation. With a key, AI creates unique lore and names.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
