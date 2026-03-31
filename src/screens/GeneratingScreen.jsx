import { useState, useEffect } from 'react';
import { Particles } from '../components/UI';

const STEPS = [
  'Scanning your goals...',
  'Mapping the dungeon floors...',
  'Spawning monsters from your tasks...',
  'Assigning difficulty ratings...',
  'Placing treasure and loot...',
  'The dungeon is ready.',
];

export default function GeneratingScreen() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStep(s => {
        if (s >= STEPS.length - 1) {
          clearInterval(interval);
          return s;
        }
        return s + 1;
      });
    }, 600);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="screen-center">
      <Particles type="dust" count={15} />
      <div className="gen-content fade-in">
        <div className="gen-icon">⚙️</div>
        {STEPS.map((msg, i) => (
          <div
            key={i}
            className="gen-step"
            style={{ color: i <= step ? 'rgba(255,215,0,0.7)' : 'rgba(255,255,255,0.1)' }}
          >
            <span>{i < step ? '✓' : i === step ? '▸' : '·'}</span>
            {msg}
          </div>
        ))}
      </div>
    </div>
  );
}
