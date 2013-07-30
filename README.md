moodscot
========

Moodscot, inspired by the twittering chicken project


installation
=======
sudo apt-get install curl libcurl3 libcurl4-openssl-dev espeak python-espeak
sudo easy_install pycurl dateutils
sudo apt-get install rabbitmq
sudo easy_install celery


run
=======
sudo modprobe spi_bcm2708
sudo python moodscot.py credentials.file terms.file


worker
=======
celery worker --app=workers -l info -n princess -Q princess