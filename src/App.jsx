import { GameProvider, useGame } from './context/GameContext';
import AuthScreen from './screens/AuthScreen';
import TitleScreen from './screens/TitleScreen';
import OracleScreen from './screens/OracleScreen';
import GeneratingScreen from './screens/GeneratingScreen';
import DungeonScreen from './screens/DungeonScreen';
import BonfireScreen from './screens/BonfireScreen';
import { LevelUpOverlay } from './components/UI';

function GameRouter() {
  const { user, authLoading, screen, loading, showLevelUp, newLevel, setShowLevelUp } = useGame();

  if (authLoading) {
    return (
      <div className="screen-center">
        <div className="loading-text">Loading...</div>
      </div>
    );
  }

  if (!user) return <AuthScreen />;

  if (loading) {
    return (
      <div className="screen-center">
        <div className="loading-text">Loading your adventure...</div>
      </div>
    );
  }

  return (
    <>
      {showLevelUp && (
        <LevelUpOverlay level={newLevel} onDone={() => setShowLevelUp(false)} />
      )}
      {screen === 'title' && <TitleScreen />}
      {screen === 'oracle' && <OracleScreen />}
      {screen === 'generating' && <GeneratingScreen />}
      {screen === 'dungeon' && <DungeonScreen />}
      {screen === 'bonfire' && <BonfireScreen />}
    </>
  );
}

export default function App() {
  return (
    <GameProvider>
      <div className="app">
        <GameRouter />
      </div>
    </GameProvider>
  );
}
