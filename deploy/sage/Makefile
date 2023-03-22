-include .env
##################################################
start: 
	docker compose up -d
.PHONY: start

##################################################
redeploy/sage: 
	docker compose up --detach --build sage
##################################################
clean:
	docker compose down
.PHONY: clean
##################################################
.EXPORT_ALL_VARIABLES:	