# Set up React  
0. `git clone https://github.com/NJIT-CS490/project2-m1-hbd3/ && cd project2-m1-hbd3`    
1. Install your stuff!    
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`    
:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    
2. If you already have psql set up, **SKIP THE REST OF THE STEPS AND JUST DO THE FOLLOWING COMMAND**:   
`sudo service postgresql start`    
3. Copy your `sql.env` file into your new directory.
  
# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
5. Make a new database: `sudo -u postgres createdb $USER`    
        :warning: :warning: :warning: If you get an error saying "could not change directory", that's okay! It worked! :warning: :warning: :warning:    
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for your-default-user as a user    
    c) `\l` look for your-default-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. `cd` into `project2-m1-hbd3` and make a new file called `sql.env` and add 'DATABASE_URL=\'postgresql://\[your-user-name\]:\[your-password\]@localhost/postgres\'' in it  
9. Fill in those values with the values you put in 7. b)  
  
  
# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a new terminal, `python app.py`    
  c) Preview Running Application if on C9(might have to clear your cache by doing a hard refresh)    
  
#  Deploying to Heroku 
1. Sign up for heroku at https://heroku.com 

2. Install heroku by running `npm install -g heroku`
3. Go through the following steps in your terminal while cd'd into your project directory:
    ```
    heroku login -i
    heroku create
    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:wait
    PGUSER=your-username-in-sql.env setup heroku pg:push postgres DATABASE_URL
    ```
    The last command will also ask for that user's password, and then it will say `pg_restore errored with 1` in terminal. 
    Which is  expected and can be ignored. 
    Following command will let you connect into your heroku database
    ```
    heroku pg:psql
    ```
    Then write the following command 
    ```
    select * from chat;
    ```
    if it exists you have successfully pushed your database into heroku you can quit with `\q`
    
 4. This repo already has required Heroku files `requirements.txt` and `Procfile`
    But if you want to set yours separately : use `touch Procfile && echo "web: python app.py > Procfile"` to set up Procfile.
    And create requirements.txt and write every dependency in your python files seperated by new lines in it. eg:
    ```
    Flask
    python-dotenv
    ```
    
 5. Finally use `git push heroku master` to deploy the program. You can use the link in terminal to access your site.
    
    
