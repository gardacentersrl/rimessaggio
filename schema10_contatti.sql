-- Richieste arrivate dal modulo contatti del sito. Incolla in Supabase > SQL Editor > Run. Rieseguibile.
create table if not exists contatti (
  id bigint generated always as identity primary key,
  creato timestamptz not null default now(),
  nome text not null,
  email text not null,
  telefono text,
  motivo text,
  mezzo text,
  lunghezza text,
  asse boolean default false,
  messaggio text not null,
  lingua text,
  ip_hash text,
  gestito boolean not null default false
);
create index if not exists contatti_ip on contatti (ip_hash, creato);
alter table contatti enable row level security;
drop policy if exists contatti_master on contatti;
create policy contatti_master on contatti for all using (ruolo_corrente()='master') with check (ruolo_corrente()='master');
