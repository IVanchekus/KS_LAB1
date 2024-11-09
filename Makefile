start:
	@nohup ./appvenv/bin/python -u main.py >> ./log/log.log 2>&1 & 
	@echo "Бот запущен"

stop: 
	@PID=$$(ps aux | grep '[p]ython -u main.py' | awk '{print $$2}'); \
	kill $$PID; \
	echo "Бот остановлен"

debug:
	@tail -f ./log/log.log