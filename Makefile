include .env

#make dbmateup
dbmateup:
	dbmate -d 'db/migrations' -u ${DATABASE_URL} up

#make goosecreate name=createusers
dbmatenew:
	dbmate -d 'db/migrations' new $(name)

#make dbmate down
dbmaterollback:
	dbmate -d 'db/migrations' -u ${DATABASE_URL} down

