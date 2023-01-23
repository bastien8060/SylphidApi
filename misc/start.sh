mkdir -p ./logs/
gunicorn --bind 127.0.0.1:5000 main:app \
	 -w 1 \
	 --threads=4 \
	 --reload \
	 --log-file ./logs/gunicorn.log \
	 --log-level DEBUG \
	 --preload \
	 --worker-class=gevent 
