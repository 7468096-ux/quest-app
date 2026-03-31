import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { supabase, getActiveRun, createRun, updateRun, getTodayDay, createDay, updateDay, createQuests, completeQuest as dbCompleteQuest } from '../lib/supabase';
import { generateQuests, calculateLevelUp, xpForLevel, getDayNumber } from '../lib/game';

const GameContext = createContext(null);

export function useGame() {
  const ctx = useContext(GameContext);
  if (!ctx) throw new Error('useGame must be used within GameProvider');
  return ctx;
}

export function GameProvider({ children }) {
  // Auth
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Game state
  const [run, setRun] = useState(null);
  const [day, setDay] = useState(null);
  const [quests, setQuests] = useState([]);
  const [screen, setScreen] = useState('title'); // title | oracle | generating | dungeon | bonfire
  const [showLevelUp, setShowLevelUp] = useState(false);
  const [newLevel, setNewLevel] = useState(1);
  const [loading, setLoading] = useState(false);

  // Settings (stored in localStorage for now)
  const [aiApiKey, setAiApiKey] = useState(() => localStorage.getItem('quest_ai_key') || '');

  // Derived
  const level = run?.current_level || 1;
  const xp = run?.current_xp || 0;
  const gold = run?.current_gold || 0;
  const xpToNext = xpForLevel(level);
  const completedCount = quests.filter(q => q.completed_at).length;
  const allCompleted = quests.length > 0 && completedCount === quests.length;

  // --- Auth listener ---
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user || null);
      setAuthLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user || null);
    });

    return () => subscription.unsubscribe();
  }, []);

  // --- Load game state on login ---
  useEffect(() => {
    if (!user) {
      setRun(null);
      setDay(null);
      setQuests([]);
      setScreen('title');
      return;
    }
    loadGameState();
  }, [user]);

  async function loadGameState() {
    try {
      setLoading(true);
      let activeRun = await getActiveRun(user.id);

      if (!activeRun) {
        // First time or after permadeath — create new run
        activeRun = await createRun(user.id, 1);
      }

      setRun(activeRun);

      // Check if today has a day entry
      const todayDay = await getTodayDay(activeRun.id);
      if (todayDay) {
        setDay(todayDay);
        setQuests(todayDay.quests || []);
        // Determine which screen to show
        if (todayDay.completed) {
          setScreen('bonfire');
        } else if (todayDay.quests?.length > 0) {
          setScreen('dungeon');
        } else {
          setScreen('oracle');
        }
      } else {
        setScreen('title');
      }
    } catch (err) {
      console.error('Failed to load game state:', err);
      setScreen('title');
    } finally {
      setLoading(false);
    }
  }

  // --- Enter dungeon (start a new day) ---
  async function enterDungeon() {
    if (!run) return;
    setScreen('oracle');
  }

  // --- Generate quests from tasks ---
  async function generateDungeon(tasks) {
    if (!run || !user) return;
    setScreen('generating');

    try {
      const dayNumber = getDayNumber(run.started_at);
      const result = await generateQuests(tasks, aiApiKey);

      // Create day in DB
      const newDay = await createDay(
        run.id,
        user.id,
        dayNumber,
        result.dungeon_name,
        result.intro
      );

      if (!newDay) throw new Error('Failed to create day');

      // Create quests in DB
      const questRows = result.quests.map((q, i) => ({
        day_id: newDay.id,
        user_id: user.id,
        original_task: q.original_task,
        quest_name: q.name,
        quest_lore: q.lore,
        quest_type: q.type,
        difficulty: q.difficulty,
        icon: q.icon,
        xp_reward: q.xp,
        gold_reward: q.gold,
        sort_order: i,
      }));

      const savedQuests = await createQuests(questRows);

      setDay({ ...newDay, quests: savedQuests });
      setQuests(savedQuests || []);

      // Small delay for generation animation
      setTimeout(() => setScreen('dungeon'), 800);
    } catch (err) {
      console.error('Failed to generate dungeon:', err);
      // Fallback: still go to dungeon with whatever we have
      setScreen('oracle');
    }
  }

  // --- Complete a quest ---
  async function handleCompleteQuest(quest) {
    if (quest.completed_at) return;

    try {
      const updated = await dbCompleteQuest(quest.id);
      if (!updated) return;

      // Update local quests
      setQuests(prev => prev.map(q => q.id === quest.id ? updated : q));

      // Calculate XP/level
      const { xp: newXp, level: newLevel, leveledUp } = calculateLevelUp(
        run.current_xp,
        run.current_level,
        quest.xp_reward
      );

      const newGold = run.current_gold + quest.gold_reward;

      // Update run
      const updatedRun = await updateRun(run.id, {
        current_xp: newXp,
        current_level: newLevel,
        current_gold: newGold,
        total_xp: run.total_xp + quest.xp_reward,
      });

      if (updatedRun) setRun(updatedRun);

      // Level up animation
      if (leveledUp) {
        setNewLevel(newLevel);
        setTimeout(() => setShowLevelUp(true), 400);
      }

      // Update day xp/gold
      if (day) {
        await updateDay(day.id, {
          xp_earned: (day.xp_earned || 0) + quest.xp_reward,
          gold_earned: (day.gold_earned || 0) + quest.gold_reward,
        });
      }
    } catch (err) {
      console.error('Failed to complete quest:', err);
    }
  }

  // --- Go to bonfire ---
  async function goToBonfire() {
    if (day) {
      await updateDay(day.id, { completed: true });
    }
    setScreen('bonfire');
  }

  // --- Save reflection ---
  async function saveReflection(text) {
    if (!day) return;
    await updateDay(day.id, { reflection: text });
    setDay(prev => ({ ...prev, reflection: text }));
  }

  // --- Next day ---
  function nextDay() {
    setDay(null);
    setQuests([]);
    setScreen('title');
  }

  // --- Save API key ---
  function saveApiKey(key) {
    setAiApiKey(key);
    localStorage.setItem('quest_ai_key', key);
  }

  const value = {
    // Auth
    user,
    authLoading,
    // State
    run,
    day,
    quests,
    screen,
    loading,
    showLevelUp,
    newLevel,
    // Derived
    level,
    xp,
    gold,
    xpToNext,
    completedCount,
    allCompleted,
    // Settings
    aiApiKey,
    saveApiKey,
    // Actions
    setScreen,
    enterDungeon,
    generateDungeon,
    handleCompleteQuest,
    goToBonfire,
    saveReflection,
    nextDay,
    setShowLevelUp,
    loadGameState,
  };

  return (
    <GameContext.Provider value={value}>
      {children}
    </GameContext.Provider>
  );
}
