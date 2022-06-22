Инструкция по деплою проекта на сервера Astra Linux (без доступа в интернет)... 
#TODO: потом надо бы собрать докер-контейнер

1.Установка Python3.9 из исходников
	sudo tar xvt ./Python-3.9.0.tgz
	cd Python-3.9.0.tgz
	./configure --prefix=/opt/python-3.9.0/ --enable-optimizations
	make -j4
	sudo make altinstall
	
	#для быстрого доступа
	echo 'alias py3.9.0=”/opt/python-3.9.0/bin/python″' >> ~/.bashrc 
	echo 'alias pip3.9.0=”/opt/python-3.9.0/bin/pip″' >> ~/.bashrc 

2.Рекомендуется создать виртуально пространство venv
	mkdir /home/<username> convector
	cd convector
	py3.9.0 -m venv venv
	source venv/bin/activate
	
	Скопировать проект в папку рядом с окружением.

3.Поставить библиотеки в окружение
	pip3.9.0 install schedule-1.1.0-py2.py3-none-any.whl
			psycopg2-2.9.3-cp310-cp310-win_amd64.whl
			lxml-4.9.0-pp39-pypy39_pp73-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl
			six-1.16.0-py2.py3-none-any.whl
			pytz-2022.1-py2.py3-none-any.whl
			cryptography318-0.3.2-py3-none-any.whl
			trollius-2.2.1-cp27-cp27m-win_amd64.whl
			futures3-1.0.0-py3-none-any.whl
			enum34-1.1.10-py3-none-any.whl
			python_dateutil-2.8.2-py2.py3-none-any.whl
	
	Устанавиливаем opcua-0.98.13
	sudo tar xvt opcua-0.98.13.tar.gz
	cd opcua-0.98.13
	py3.9.0 setup.py
	Копируем содержимое папки в ./vevn/Lib/site-packages/ ... молимся чтобы подсосало

4.Запустим ради прикола, чисто проверить 
	py3.9.0 main.py

5.Создаем свой сервис в линуксе systemd

	sudo vim /etc/systemd/system/convector-alpha-postgres.service

		[Unit]
		Description=Convector postgrest to alpha server. 
		After=multi-user.target
 
		[Service]
		User=<user>
		Group=<group>
		Type=simple
		Restart=always
		ExecStart=/usr/bin/python3 /home/<username>/convector/client/main.py
 
		[Install]
		WantedBy=multi-user.target

	sudo systemctl daemon-reload
	sudo systemctl enable convector-alpha-postgres.service
	sudo systemctl start convector-alpha-postgres.service
	sudo systemctl status convector-alpha-postgres.service
______________
may the force come with us


	

	
	
