create table public.leads (
  user_id bigint not null,
  screen_name text not null,
  description text null,
  profile_image text null,
  statuses_count integer null,
  followers_count integer null,
  friends_count integer null,
  media_count integer null,
  created_at timestamp with time zone null,
  location text null,
  blue_verified boolean null,
  website text null,
  name text not null,
  business_account boolean null,
  constraint pot_leads_pkey primary key (user_id)
) TABLESPACE pg_default;