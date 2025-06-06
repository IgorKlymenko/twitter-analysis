create table public.final (
  user_id bigint not null,
  screen_name text not null,
  description text null,
  profile_image text null,
  statuses_count integer null,
  followers_count integer null,
  friends_count integer null,
  tweet text null,
  media_count integer null,
  created_at timestamp with time zone null,
  location text null,
  blue_verified boolean null,
  website text null,
  name text not null,
  business_account boolean null,
  owner text null,
  founder boolean null,
  canadian boolean null,
  vc boolean null,
  score double precision null,
  ventures text[] null,
  companies text null,
  constraint final_pkey primary key (user_id)
) TABLESPACE pg_default;