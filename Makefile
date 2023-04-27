setup:
	docker start mssql-databases && sleep 3s
run:
	uvicorn main:app --reload
stop:
	docker stop mssql-databases
