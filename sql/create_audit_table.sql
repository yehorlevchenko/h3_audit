CREATE TABLE IF NOT EXISTS audit
(id serial PRIMARY KEY,
project_id integer NOT NULL,
url varchar NOT NULL,
title_errors integer[],
description_errors integer[],
keywords_errors integer[],
h1_errors integer[],
h2_errors integer[],
h3_errors integer[]);