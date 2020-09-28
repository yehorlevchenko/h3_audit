CREATE TABLE IF NOT EXISTS project
(id serial PRIMARY KEY,
owner_id integer NOT NULL,
main_url varchar NOT NULL,
is_done boolean DEFAULT false,
last_check date);