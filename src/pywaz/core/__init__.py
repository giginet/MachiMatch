import settings

settings.SCREENWIDTH = getattr(settings, 'SCREENWIDTH', 640)
settings.SCREENHEIGHT = getattr(settings, 'SCREENHEIGHT', 480)
settings.SCREENCAPTION = getattr(settings, 'SCREENCAPTION', u'Hello, Kawaz')
settings.FULLSCREEN = getattr(settings, 'FULLSCREEN', False)