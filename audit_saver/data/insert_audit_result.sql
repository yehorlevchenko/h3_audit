INSERT INTO panel_auditresults (url,
                                audit_id,
                                title_error,
                                description_error,
                                keywords_error,
                                h1_error,
                                h2_error,
                                h3_error,
                                status_code)
VALUES (%(url)s,
        %(audit_id)s,
        %(title)s,
        %(description)s,
        %(keywords)s,
        %(h1)s,
        %(h2)s,
        %(h3)s,
        %(status_code)s
       );