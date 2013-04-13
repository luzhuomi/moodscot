moodscot
========

Moodscot, inspired by the twittering chicken project


installation
=======
sudo apt-get install curl libcurl3 libcurl4-openssl-dev espeak python-espeak
sudo easy_install pycurl dateutils


run
=======
sudo modprobe spi_bcm2708
sudo python moodscot.py credentials.file terms.file