INSERT INTO audit (audit_id,
                   url,
                   code_error,
                   status_code)
VALUES (
        %(audit_id)s,
        %(url)s,
        %(code_error)s,
        %(status_code)s
       );
