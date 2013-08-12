from __future__ import absolute_import

from celery import Celery

celery = Celery('workers.celery',
                # broker='amqp://guest@localhost//',
                # backend='amqp://',
		broker='amqp://guest@172.20.130.245//',
		backend='amqp://guest@172.20.130.245//',
                include=['workers.tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ROUTES = {
        'workers.tasks.princess': {'queue': 'princess'},
        'workers.tasks.monkey': {'queue': 'monkey'},        
        'workers.tasks.anger': {'queue': 'anger'},        
        'workers.tasks.diva': {'queue': 'diva'},        
        'workers.tasks.normal': {'queue': 'normal'},        
    },    
)

if __name__ == '__main__':
    celery.start()
