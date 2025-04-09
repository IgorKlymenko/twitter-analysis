create table public.posts (
  tweet_id bigint not null,
  bookmarks integer null,
  created_at timestamp without time zone null,
  favorites integer null,
  text text null,
  lang character varying(10) null,
  quotes integer null,
  replies integer null,
  retweets integer null,
  conversation_id bigint null,
  author_name character varying(255) null,
  author_screen_name character varying(50) null,
  owner text null,
  constraint posts_pkey primary key (tweet_id)
) TABLESPACE pg_default;