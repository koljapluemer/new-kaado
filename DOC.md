## Structure

### Auth

Uses oAuth, currently following [this tutorial](https://www.youtube.com/watch?v=RyB_wdEZhOw) and the [all-auth doc](https://django-allauth.readthedocs.io/en/latest/templates.html).

### Importing

`kaado-import.py` is the one file that does a full supabase import. It does not match users to users on the new deployment, though. All other scripts are relics. Run with: `python manage.py runscript kaado-import`