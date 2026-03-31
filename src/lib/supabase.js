import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseKey);

// --- Auth helpers ---
export async function signInWithGoogle() {
  return supabase.auth.signInWithOAuth({ provider: 'google' });
}

export async function signInWithEmail(email, password) {
  return supabase.auth.signInWithPassword({ email, password });
}

export async function signUpWithEmail(email, password) {
  return supabase.auth.signUp({ email, password });
}

export async function signOut() {
  return supabase.auth.signOut();
}

// --- Profile ---
export async function getProfile(userId) {
  const { data } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .single();
  return data;
}

// --- Runs ---
export async function getActiveRun(userId) {
  const { data } = await supabase
    .from('runs')
    .select('*')
    .eq('user_id', userId)
    .eq('status', 'active')
    .order('created_at', { ascending: false })
    .limit(1)
    .single();
  return data;
}

export async function createRun(userId, runNumber = 1) {
  const { data } = await supabase
    .from('runs')
    .insert({ user_id: userId, run_number: runNumber })
    .select()
    .single();
  return data;
}

export async function updateRun(runId, updates) {
  const { data } = await supabase
    .from('runs')
    .update(updates)
    .eq('id', runId)
    .select()
    .single();
  return data;
}

// --- Days ---
export async function getTodayDay(runId) {
  const today = new Date().toISOString().split('T')[0];
  const { data } = await supabase
    .from('days')
    .select('*, quests(*)')
    .eq('run_id', runId)
    .eq('date', today)
    .single();
  return data;
}

export async function getRunDays(runId) {
  const { data } = await supabase
    .from('days')
    .select('*, quests(*)')
    .eq('run_id', runId)
    .order('day_number', { ascending: true });
  return data || [];
}

export async function createDay(runId, userId, dayNumber, dungeonName, introText) {
  const { data } = await supabase
    .from('days')
    .insert({
      run_id: runId,
      user_id: userId,
      day_number: dayNumber,
      dungeon_name: dungeonName,
      intro_text: introText,
    })
    .select()
    .single();
  return data;
}

export async function updateDay(dayId, updates) {
  const { data } = await supabase
    .from('days')
    .update(updates)
    .eq('id', dayId)
    .select()
    .single();
  return data;
}

// --- Quests ---
export async function createQuests(quests) {
  const { data } = await supabase
    .from('quests')
    .insert(quests)
    .select();
  return data;
}

export async function completeQuest(questId) {
  const { data } = await supabase
    .from('quests')
    .update({ completed_at: new Date().toISOString() })
    .eq('id', questId)
    .select()
    .single();
  return data;
}
