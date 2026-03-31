-- =============================================
-- Quest Roguelike App — Phase 0 Schema
-- Run this in Supabase SQL Editor
-- =============================================

-- Enable UUID generation
create extension if not exists "uuid-ossp";

-- USERS (extends Supabase auth.users)
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  display_name text,
  current_run_id uuid,
  created_at timestamptz default now()
);

alter table public.profiles enable row level security;
create policy "Users can read own profile" on public.profiles for select using (auth.uid() = id);
create policy "Users can update own profile" on public.profiles for update using (auth.uid() = id);
create policy "Users can insert own profile" on public.profiles for insert with check (auth.uid() = id);

-- Auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name', 'Adventurer'));
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- RUNS (weekly cycles)
create table public.runs (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  run_number int not null default 1,
  started_at timestamptz default now(),
  ended_at timestamptz,
  current_level int default 1,
  current_xp int default 0,
  current_gold int default 0,
  total_xp int default 0,
  status text default 'active' check (status in ('active', 'dead', 'abandoned')),
  created_at timestamptz default now()
);

alter table public.runs enable row level security;
create policy "Users can CRUD own runs" on public.runs for all using (auth.uid() = user_id);

create index idx_runs_user on public.runs(user_id);
create index idx_runs_status on public.runs(user_id, status);

-- DAYS (each day within a run)
create table public.days (
  id uuid default uuid_generate_v4() primary key,
  run_id uuid references public.runs(id) on delete cascade not null,
  user_id uuid references public.profiles(id) on delete cascade not null,
  day_number int not null check (day_number between 1 and 7),
  date date not null default current_date,
  dungeon_name text,
  intro_text text,
  reflection text,
  xp_earned int default 0,
  gold_earned int default 0,
  completed boolean default false,
  created_at timestamptz default now()
);

alter table public.days enable row level security;
create policy "Users can CRUD own days" on public.days for all using (auth.uid() = user_id);

create index idx_days_run on public.days(run_id);
create unique index idx_days_unique on public.days(run_id, day_number);

-- QUESTS (tasks within a day)
create table public.quests (
  id uuid default uuid_generate_v4() primary key,
  day_id uuid references public.days(id) on delete cascade not null,
  user_id uuid references public.profiles(id) on delete cascade not null,
  original_task text not null,
  quest_name text not null,
  quest_lore text,
  quest_type text default 'quest' check (quest_type in ('boss', 'quest', 'side')),
  difficulty text default 'medium' check (difficulty in ('easy', 'medium', 'hard')),
  icon text default '⚔️',
  xp_reward int default 20,
  gold_reward int default 10,
  completed_at timestamptz,
  sort_order int default 0,
  created_at timestamptz default now()
);

alter table public.quests enable row level security;
create policy "Users can CRUD own quests" on public.quests for all using (auth.uid() = user_id);

create index idx_quests_day on public.quests(day_id);
