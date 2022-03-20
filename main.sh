echo "What was the repo name"
read project_name
python create_project.py
git init
git add .
git commit -m "init"
git branch -M main
git remote add origin https://github.com/APlusCert/$project_name.git
git push -u origin main

heroku login
while true
do
 clear
 result=$(heroku apps:create $project_name)
 if [[ "$result" == *"$project_name"* ]];
 then
  echo 'success'
  break
 fi
 echo "$project_name not valid. Please try again"
 read project_name
done
heroku addons:create heroku-postgresql:hobby-dev
cat postgre.sql | heroku pg:psql --app $project_name
heroku config:set SECRET=$secret
git push heroku main
