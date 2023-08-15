import aiocron


def schedule(cron_str):
    def decorator(func):
        aiocron.crontab(cron_str, func=func, start=True)
        return func

    return decorator
