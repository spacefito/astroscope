from distutils.core import setup
setup(name='astroscope',
      version='0.1.1',
      packages=['astroscope',
                'astroscope.cameras',
                'astroscope.computers',
                'astroscope.telescopes'],
      scripts=['astroscope/scripts/astroscope', 'astroscope/scripts/telescope']
      )

