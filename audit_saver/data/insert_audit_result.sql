INSERT INTO audit (project_id,
                   url,
                   title_errors,
                   description_errors,
                   keywords_errors,
                   h1_errors,
                   h2_errors,
                   h3_errors)
VALUES (
        %(audit_id)s,
        %(main_url)s,
        %(title)s,
        %(description)s,
        %(keywords)s,
        %(h1)s,
        %(h2)s,
        %(h3)s
       );