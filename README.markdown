
# README 

## SOFTWARE REQUIREMENTS 

 * python 2.6/2.7
 * django 1.2.3
 * postgresql 8.4.x
 * psycopg2


## INSTALL 

 * hg clone http://bitbucket.org/tony/slackfind
 * cp settings_local.py.template settings_local.py
 * edit settings_local.py 
 * run: python manage.py syncdb --migrate
 * run: python manage.py runserver
 * open in your browser: http://localhost:8000/
 * enjoy

## CONTRIBUTION

 * fork
 * make changes
 * don't forget to edit templates/about.html to add youself in the authors list
 * if changes are significant add your blog post and update microblog/fixtures/initial_data.xml
 * push your changes into your branch
 * pull request
